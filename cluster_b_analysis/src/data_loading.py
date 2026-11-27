"""Read and validate the Stage 1 inputs used for matched comparisons."""

import csv
import json
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_FIELDS = (
    "observation_id", "architecture", "configuration_id", "block_id", "role",
    "backbone", "judge", "score", "score_as_printed", "pdf_page", "source_row",
    "source_column", "metric_definition", "failure_mode", "hallucination_measurement",
    "sample_size", "independent_runs", "sd", "se", "ci_lower", "ci_upper",
    "limitations", "source_details",
)
OUTCOME_FIELDS = ("benchmark", "benchmark_version", "split", "task", "metric", "unit")


@dataclass(frozen=True)
class MatchedPair:
    comparison: dict[str, str]
    left: dict[str, str]
    right: dict[str, str]
    protocol_block: str
    cohort: str


def read_csv(path, required_fields):
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = set(required_fields).difference(reader.fieldnames or ())
        if missing:
            raise ValueError(f"{path.name} is missing columns {sorted(missing)}")
        for row in reader:
            if None in row or None in row.values():
                raise ValueError(f"Malformed row in {path.name} at line {reader.line_num}")
            yield row


def read_score(value):
    """A blank score is unknown. Malformed and non-finite numbers are invalid."""
    if value is None or value == "":
        return None
    try:
        number = Decimal(str(value).replace(",", ""))
    except InvalidOperation as exc:
        raise ValueError(f"Invalid numerical score {value!r}") from exc
    if not number.is_finite():
        raise ValueError(f"Non-finite numerical score {value!r}")
    return number


def load_matched_pairs(data_dir=ROOT / "data"):
    """Join strict candidates by ID and preserve Stage 1 cohort assignments."""
    data_dir = Path(data_dir)
    observations = {}
    required = (*SOURCE_FIELDS, *OUTCOME_FIELDS, "paper_id", "table_id", "direction",
                "verification", "provenance", "synthesis_exclude")
    for row in read_csv(data_dir / "validated_results.csv", required):
        obs_id = row["observation_id"]
        if not obs_id or obs_id in observations:
            raise ValueError(f"Blank or duplicate observation ID {obs_id!r}")
        read_score(row["score"])
        observations[obs_id] = row

    block_fields = ("paper_id", "benchmark", "block_id", "table_id", "cohort_group")
    block_index = set()
    for row in read_csv(data_dir / "comparison_blocks.csv", (*block_fields, "metrics")):
        key = tuple(row[field] for field in block_fields)
        if not all(key) or any((*key, metric) in block_index for metric in row["metrics"].split("; ")):
            raise ValueError(f"Invalid or duplicate block record {key}")
        block_index.update((*key, metric) for metric in row["metrics"].split("; "))

    join_fields = ("block", "configuration", "architecture", "backbone", "judge", "benchmark_version")
    required = ("comparison_level", "status", "reason", "evidence_type", "benchmark",
                "split", "task", "metric", "unit",
                *(f"{side}_{field}" for side in ("left", "right")
                  for field in ("observation", *join_fields)))
    seen = set()
    for comparison in read_csv(data_dir / "comparability.csv", required):
        if (comparison["comparison_level"], comparison["status"]) != ("within_block", "Directly comparable"):
            continue
        a, b = (comparison[f"{side}_observation"] for side in ("left", "right"))
        pair_key = frozenset((a, b))
        if not a or not b or a == b or pair_key in seen:
            raise ValueError(f"Invalid or duplicate direct pair {a!r}, {b!r}")
        seen.add(pair_key)
        if a not in observations or b not in observations:
            raise ValueError(f"Direct pair {a}, {b} refers to a missing validated observation")
        left, right = observations[a], observations[b]
        if not all((row["verification"], row["provenance"], row["synthesis_exclude"])
                   == ("verified", "original", "no") for row in (left, right)):
            continue

        for side, row in (("left", left), ("right", right)):
            for field in join_fields:
                obs_field = f"{field}_id" if field in {"block", "configuration"} else field
                if comparison[f"{side}_{field}"] != row[obs_field]:
                    raise ValueError(f"{side} {field} disagrees with observation for {a}, {b}")
        shared = ("benchmark", "split", "task", "metric", "unit")
        if (any(left[k] != right[k] for k in ("paper_id", "table_id", "direction", "benchmark_version"))
                or any(left[k] != comparison[k] or right[k] != comparison[k] for k in shared)
                or left["direction"] not in {"higher", "lower"} or not comparison["evidence_type"]
                or any(read_score(row["score"]) is None for row in (left, right))):
            raise ValueError(f"Inconsistent direct comparison for {a}, {b}")

        left_details, right_details = (json.loads(row["source_details"] or "{}") for row in (left, right))
        paper, benchmark, table = (left[k] for k in ("paper_id", "benchmark", "table_id"))
        block = left["block_id"]
        if block != right["block_id"]:
            block = left_details.get("comparison_family") or right_details.get("comparison_family")
        cohort = str(left_details.get("independent_group") or f"{paper}:{benchmark}")
        if (paper, benchmark, block, table, cohort, left["metric"]) not in block_index:
            raise ValueError(f"No Stage 1 block record for {a}, {b}")
        yield MatchedPair(comparison, left, right, block, cohort)
