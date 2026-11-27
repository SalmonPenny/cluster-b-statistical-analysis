"""Build the Stage 1 evidence tables from raw CSV or reviewed extraction JSON."""
import argparse
from collections import defaultdict
import csv
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import re

import pymupdf


ROOT = Path(__file__).resolve().parents[1]
FIELDS = """observation_id paper_id paper_title publication_id pdf_filename publication_version
source_url pdf_page table_id source_row source_column architecture architecture_version
rq2_category mechanisms backbone role judge judging_protocol retrieval_budget memory_budget
context_budget block_id configuration_id benchmark benchmark_version split task metric
metric_definition direction score score_as_printed unit normalized_score normalized_unit sample_size independent_runs sd se
ci_lower ci_upper failure_mode hallucination_measurement provenance original_source verification
duplicate_of discrepancy synthesis_exclude comparability_status limitations source_details""".split()
COMPARISON_FIELDS = """comparison_level status benchmark split task metric unit left_block
right_block left_benchmark_version right_benchmark_version left_configuration right_configuration left_architecture right_architecture
left_observation right_observation left_backbone right_backbone left_judge right_judge
evidence_type reason""".split()
VERSIONS = {
    "membook": "Findings of EMNLP 2026, proceedings version",
    "rmm": "ACL 2025 Long Papers, proceedings version",
    "mragent": "arXiv:2606.06036v1",
    "telemem": "arXiv:2601.06037v4",
    "longmemeval": "arXiv:2410.10813v2 (ICLR 2025)",
    "locomo": "arXiv:2402.17753v1",
    "halumem": "arXiv:2511.03506v3",
    "memguard": "arXiv:2605.28009v2",
    "trustmem": "arXiv:2606.25161v1",
    "synthius_mem": "April 2026 local preprint",
    "sirin": "arXiv:2608.00033v1",
    "agent_native_memory": "arXiv:2606.24775v1",
    "memorybench": "arXiv:2510.17281v7",
    "locomo_plus": "arXiv:2602.10715v1",
    "realmem": "Findings of ACL 2026 (2026.findings-acl.703)",
    "biomem": "arXiv:2611.13426v1",
    "membench": "arXiv:2506.21605v1",
    "es_memeval": "arXiv:2602.01885v1",
    "root_memory": "arXiv:2606.23283v2",
    "twist": "arXiv:2609.28575v1",
    "locco": "Findings of ACL 2025 (2025.findings-acl.1014)",
    "memgpt": "arXiv:2310.08560v2",
    "memoryrewardbench": "arXiv:2601.11969v2",
    "oracle_agent": "arXiv:2607.13157v1",
}
ARCHITECTURES = {
    "mem0graph": "Mem0-Graph", "mem0": "Mem0", "amem": "A-Mem", "memgpt": "MemGPT",
    "langmem": "LangMem", "memoryos": "MemoryOS", "memobase": "Memobase",
    "supermemory": "Supermemory", "longcontextllm": "Long Context",
    "longcontext": "Long Context", "nohistory": "No History",
    "memorybank": "MemoryBank", "ldagent": "LD-Agent", "telemem": "TeleMem",
    "membook": "MemBook", "mragent": "MRAgent", "gam": "GAM", "moom": "MOOM",
    "rag": "RAG", "rmm": "RMM", "ragtop2": "RAG",
    "longcontextbaseline": "Long Context", "fullcontext": "Long Context", "memguard": "MemGuard", "trustmem": "TRUSTMEM",
    "synthiusmem": "Synthius-Mem", "simplemem": "SimpleMem", "lightmem": "LightMem",
    "zep": "Zep", "memos": "MemOS", "mirix": "MIRIX", "cognee": "Cognee",
}
CATEGORIES = {
    "MemBook": "2. Dedicated Memory Architecture",
    "MRAgent": "2. Dedicated Memory Architecture",
    "MemGPT": "2. Dedicated Memory Architecture",
    "Oracle Agent Memory": "2. Dedicated Memory Architecture",
    "RMM": "4. Memory Maintenance & Quality Management",
    "TeleMem": "Screening inclusion only; multimodal scope flag in RQ2",
    "Synthius-Mem": "2. Dedicated Memory Architecture",
    "MemGuard": "4. Memory Maintenance & Quality Management",
    "TRUSTMEM": "4. Memory Maintenance & Quality Management",
}
LONGMEMEVAL_MODES = {
    "singlesessionuser": "Within-session recall of user-provided information",
    "singlesessionassistant": "Within-session recall of assistant-provided information",
    "singlesessionpreference": "Retention and application of user preferences",
    "multisessionreasoning": "Cross-session evidence integration and reasoning",
    "temporalreasoning": "Temporal reasoning over dialogue and timestamps",
    "knowledgeupdate": "Recognition of updates and avoidance of outdated information",
    "overall": "Combined episodic memory question answering",
}
BENCHMARK_NAMES = {
    "longmemeval": "LongMemEval", "locomo": "LoCoMo", "halumem": "HaluMem",
    "msc": "MSC", "multisessionchat": "MSC", "zh4o": "ZH-4O",
    "memoryagentbench": "MemoryAgentBench", "perltqa": "PerLTQA",
    "locomoplus": "LoCoMo-Plus", "memorybench": "MemoryBench", "realmem": "RealMem",
    "membench": "MemBench", "esmemeval": "ES-MemEval", "imlogic": "IMLogic", "twist": "TWIST",
}


def key(value):
    return re.sub(r"[^a-z0-9]", "", value.casefold())


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path, fields, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fields)
        writer.writeheader()
        writer.writerows({field: row.get(field, "") for field in fields} for row in rows)


def format_cell(value):
    if value is None:
        return ""
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value).strip()


def category(architecture):
    if architecture in CATEGORIES:
        return CATEGORIES[architecture]
    for prefix, prefix_category in CATEGORIES.items():
        if architecture.startswith((prefix + " ", prefix + "*", prefix + " (")):
            return prefix_category
    return ""


def details(row):
    return json.loads(row["source_details"] or "{}")


def prepare(rows, manifest, page_counts):
    seen = set()
    for source in rows:
        row = {field: format_cell(source.get(field)) for field in FIELDS}
        extras = {"pdf_version", "pdf_file", "architecture_category", "score_normalized"}
        try:
            source_details = details(row)
        except json.JSONDecodeError:
            source_details = {"source_note": row["source_details"]}
        source_details.update({field: value for field, value in source.items()
                               if field not in FIELDS and field not in extras and value not in ("", None)})
        row["source_details"] = format_cell(source_details) if source_details else ""
        row["score_as_printed"] = row["score_as_printed"] or format_cell(source.get("original_score_label")) or row["score"]
        paper = manifest[row["paper_id"]]
        row["paper_title"] = paper["title"]
        row["pdf_filename"] = f'{row["paper_id"]}.pdf'
        row["publication_id"] = paper["acl_id"] or paper["arxiv_id"] or paper["doi"]
        row["publication_version"] = row["publication_version"] or format_cell(source.get("pdf_version")) or VERSIONS[row["paper_id"]]
        row["source_url"] = paper["source_url"]
        for field in ("table_id", "source_row", "source_column", "architecture", "benchmark",
                      "metric", "block_id", "configuration_id"):
            if not row[field]:
                raise ValueError(f"Missing {field} in {source}")
        if not 1 <= int(row["pdf_page"]) <= page_counts[row["paper_id"]]:
            raise ValueError(f"Invalid PDF page: {source}")
        row["architecture"] = ARCHITECTURES.get(key(row["architecture"]), row["architecture"])
        row["benchmark"] = BENCHMARK_NAMES.get(key(row["benchmark"]), row["benchmark"])
        row["rq2_category"] = category(row["architecture"])
        if row["paper_id"] == "membook" and row["benchmark"] == "LongMemEval":
            row["failure_mode"] = LONGMEMEVAL_MODES.get(key(row["task"]), row["failure_mode"])
        if row["verification"] not in {"verified", "unverified", "missing"}:
            raise ValueError(f"Unknown verification status: {source}")
        if row["provenance"] not in {"original", "imported", "unclear"}:
            raise ValueError(f"Unknown provenance: {source}")
        if row["direction"] not in {"higher", "lower", ""}:
            raise ValueError(f"Unknown metric direction: {source}")
        if row["provenance"] == "imported" and not row["original_source"]:
            raise ValueError(f"Imported result without source: {source}")
        if row["benchmark"] in {"HaluMem", "MSC"} and row["hallucination_measurement"] == "n/a":
            if row["role"] in {"baseline", "proposed", "ablation"} and row["metric"] not in {
                "LLM judge agreement rate", "Cohen’s kappa"
            }:
                row["hallucination_measurement"] = "proxy"
        row["synthesis_exclude"] = "yes" if (
            row["synthesis_exclude"].casefold() in {"true", "yes", "1"} or row["duplicate_of"]
        ) else "no"
        row["normalized_score"] = ""
        row["normalized_unit"] = ""
        if not row["score"]:
            if row["verification"] == "verified":
                raise ValueError(f"Empty verified score: {source}")
        else:
            score = float(row["score"].replace(",", ""))
            if not -float("inf") < score < float("inf"):
                raise ValueError(f"Non-finite score: {source}")
            if row["unit"] in {"percent", "proportion"}:
                scale = 100 if row["unit"] == "percent" else 1
                if 0 <= score <= scale:
                    row["normalized_score"] = format(score / scale, ".12g")
                    row["normalized_unit"] = "proportion"
                elif row["synthesis_exclude"] != "yes" or not row["discrepancy"]:
                    raise ValueError(f"Score outside declared unit range: {source}")
            elif row["unit"] == "thousands of tokens":
                row["normalized_score"] = format(score * 1000, ".12g")
                row["normalized_unit"] = "tokens"
        locator = [row[field] for field in (
            "paper_id", "pdf_page", "table_id", "source_row", "source_column"
        )]
        identity = sha256(json.dumps(locator, ensure_ascii=False).encode()).hexdigest()[:15]
        row["observation_id"] = f'{row["paper_id"]}-{identity}'
        if row["observation_id"] in seen:
            raise ValueError(f"Duplicate source locator: {locator}")
        seen.add(row["observation_id"])
        yield row


def eligible(row):
    return (row["verification"] == "verified" and row["score"] != ""
            and row["synthesis_exclude"] == "no")


def compare_pair(left, right):
    if not left["score"] or not right["score"] or any(
        row["verification"] != "verified" for row in (left, right)
    ):
        return "Missing", "missing evidence", "At least one numerical result is missing or unverified."
    pair = (left, right)
    if left["split"] != right["split"]:
        return "Incompatible", "different cohorts", "The full benchmark and sampled subset have different reported evaluation cohorts."
    if left["paper_id"] == "halumem" and left["table_id"] == "Table 4" and any(
        row["architecture"] == "Zep" for row in pair
    ):
        return "Incompatible", "different operation coverage", "The starred Zep row assesses only updated memories; its denominator differs from combined extraction and updating."
    if any(row["discrepancy"] == "conflicting_source_row_identity" for row in pair):
        return "Incompatible", "source identity conflict", "Attribution disagrees with the matching original source row."
    if any(row["provenance"] != "original" for row in pair):
        if all(row["judge"] for row in pair) and key(left["judge"]) != key(right["judge"]):
            return "Incompatible", "different judges", "The original comparator reports a different judgment protocol."
        return "Conditionally comparable", "published or uncertain baseline", "The source experiment for a baseline is separate or unresolved. Excluded from same-run graphs."
    repeated_anchor = (
        left["table_id"] == right["table_id"]
        and (left["paper_id"], left["table_id"]) in {
            ("rmm", "Table 2"), ("rmm", "Table 6"),
            ("membook", "Table 4a"), ("membook", "Table 4b"),
        }
        and sum(bool(row["duplicate_of"]) for row in pair) == 1
        and any(row["role"] == "ablation" for row in pair)
    )
    if (not eligible(left) or not eligible(right)) and not repeated_anchor:
        return "Incompatible", "excluded source cell", "At least one source cell is unresolved, derived, or repeats another cell."
    if left["direction"] not in {"higher", "lower"} or right["direction"] != left["direction"]:
        return "Incompatible", "descriptive value", "A shared metric orientation is unspecified."
    if left["unit"] != right["unit"]:
        return "Incompatible", "scale mismatch", "The reported units differ."
    paper = left["paper_id"]
    if any(details(row).get("pair_condition") for row in pair):
        reasons = sorted({details(row)["pair_condition"] for row in pair if details(row).get("pair_condition")})
        return "Conditionally comparable", "protocol qualification", " ".join(reasons)
    if any(row["discrepancy"] and row["discrepancy"] not in {"possible_fig7_overlap", "possible_fig9_overlap"} for row in pair):
        return "Conditionally comparable", "flagged contrast", "A source or protocol discrepancy limits interpretation. Check the source cell flags."
    if any("oracle" in key(row["architecture"]) or "oracle" in key(row["role"]) for row in pair):
        return "Conditionally comparable", "oracle control", "An evidence oracle uses additional information and is a diagnostic reference."
    if paper == "mragent" and any(any(mark in row["source_row"] for mark in ("*", "∗", "★")) or "for retrieval" in row["backbone"] for row in pair):
        return "Conditionally comparable", "mixed backbone", "MRAgent* uses Gemini to build memory and Claude to retrieve."
    if not left["backbone"] or not right["backbone"]:
        return "Conditionally comparable", "configuration incompletely documented", "A backbone is missing at the resolution of this contrast."
    if paper == "telemem" and left["block_id"] == "telemem-zh-4o-scaling":
        return "Directly comparable", "controlled scaling variant", "The size grid varies the named writer/reader sizes under a shared procedure. Model identities are unreported."
    if key(left["backbone"]) != key(right["backbone"]):
        return "Conditionally comparable", "different backbones", "The two configurations use different documented backbones."
    if any(row["judge"] for row in pair) and key(left["judge"]) != key(right["judge"]):
        return "Incompatible", "different judges", "The two observations use distinct judge settings."
    if paper == "membook" and left["benchmark"] == "HaluMem" and not any(row["role"] == "ablation" for row in pair):
        return "Conditionally comparable", "configuration incompletely documented", "Study implementation details for HaluMem comparison systems are incompletely specified."
    if paper == "membook" and left["benchmark"] == "LongMemEval" and not left["judge"]:
        return "Conditionally comparable", "judge underreported", "Systems share a reported backbone block. The LongMemEval judge is unspecified."
    if paper == "rmm":
        if re.search(r"Table\s+[2346]\b", left["table_id"], re.I):
            return "Directly comparable", "controlled variant", "Within the documented RMM component, LLM, or budget sweep, vary only the reported factors."
        if {row["architecture"] for row in pair} == {"RAG", "RMM"}:
            retrievers = [json.loads(row["source_details"] or "{}").get("retriever") for row in pair]
            if retrievers[0] and retrievers[0] == retrievers[1]:
                return "Directly comparable", "matched retriever pipeline contrast", "Same retriever family and QA protocol. The pipelines differ in storage, reranking and retrieval budget."
    if paper == "halumem" and left["task"] != "Question answering":
        return "Conditionally comparable", "system-specific memory operations", "The judge and split are shared, while write, update, and extraction implementations differ by system."
    if paper == "locomo" and left["metric"].startswith("Recall@"):
        units = [row["source_row"].partition(" / ")[0] for row in pair]
        if ("Summary" in units[0]) != ("Summary" in units[1]):
            return "Incompatible", "evidence granularity", "Recall uses different annotated units for summary and turn-level retrieval."
    if paper == "memgpt" and left["table_id"] == "Table 2":
        return ("Directly comparable", "matched backbone systems",
                "Shared DMR questions, reader and scoring procedure. Memory access and source evidence differ.")
    if paper == "agent_native_memory" and left["table_id"].startswith("Figure 9"):
        return "Directly comparable", "matched backbone systems", "Compare the evaluated systems under the same named answer backbone and metric. Other backbones reuse the workload."
    if "ablation" in left["role"].casefold() or "ablation" in right["role"].casefold():
        return "Directly comparable", "controlled variant", "Within the authors' ablation panel and fixed reported protocol."
    return "Directly comparable", "evaluated systems", "Same reported original comparison block, outcome and backbone; estimates compare complete evaluated systems."


def pair_record(left, right, level, status, kind, reason):
    return {
        "comparison_level": level, "status": status,
        **{field: left[field] for field in ("benchmark", "split", "task", "metric", "unit")},
        "left_block": left["block_id"], "right_block": right["block_id"],
        "left_benchmark_version": left["benchmark_version"], "right_benchmark_version": right["benchmark_version"],
        "left_configuration": left["configuration_id"], "right_configuration": right["configuration_id"],
        "left_architecture": left["architecture"], "right_architecture": right["architecture"],
        "left_observation": left["observation_id"], "right_observation": right["observation_id"],
        "left_backbone": left["backbone"], "right_backbone": right["backbone"],
        "left_judge": left["judge"], "right_judge": right["judge"],
        "evidence_type": kind, "reason": reason,
    }


def cross_protocol(left, right):
    benchmark = left["benchmark"]
    if benchmark == "RealMem" and {left["paper_id"], right["paper_id"]} == {"realmem", "biomem"}:
        return ("Incompatible", "Full RealMem and the BioMem medical subset have different question scope and scoring protocols. Shared labels do not establish item-level replication.")
    if benchmark == "LoCoMo":
        return ("Incompatible", "Cross-study LoCoMo scoring and item-set equivalence is unestablished. Documented panels vary by release, lexical or semantic scorer, backbone, or question set.")
    if benchmark == "HaluMem":
        if left["split"] and right["split"] and key(left["split"]) != key(right["split"]):
            return ("Incompatible", "The source panels identify different splits or different sampled cohorts.")
        if left["judge"] and right["judge"] and key(left["judge"]) != key(right["judge"]):
            return ("Incompatible", "The source panels use different judging models.")
        return ("Conditionally comparable", "Check run-level independence, cohort, label definitions and baseline origin before pooling.")
    if benchmark == "LongMemEval":
        if (left["benchmark_version"] and right["benchmark_version"]
                and key(left["benchmark_version"]) != key(right["benchmark_version"])):
            return ("Incompatible", "Documented benchmark variants differ; no item-level alignment or shared protocol has been established.")
        return ("Conditionally comparable",
                "Shared benchmark and labels identify candidates; pooling requires alignment of split, backbone, judge, task items and context. "
                "Known differences rule out treating this as a fixed-protocol comparison.")
    return ("Conditionally comparable", "Align the dataset release, split, judge and backbone before any cross-protocol comparison.")


def comparisons(rows):
    panels = defaultdict(list)
    protocols = defaultdict(dict)
    cross_study_panels = {
        ("membook", "Table 3", "Accuracy"), ("rmm", "Table 1", "Accuracy"),
        ("mragent", "Table 1", "LLM-Judge"), ("mragent", "Table 5", "LLM-Judge"),
        ("telemem", "Table 3", "LLM-Judge"),
    }
    for row in rows:
        family = details(row).get("comparison_family") or row["block_id"]
        cohort = row["split"]
        if (row["paper_id"], row["table_id"]) == ("memguard", "Table 7"):
            cohort = ""  # Compare the documented full split and sampled protocol explicitly.
        grain = (row["paper_id"], family, row["table_id"], row["benchmark"], cohort,
                 row["task"], row["metric"], row["unit"])
        panels[grain].append(row)
        panel = (row["paper_id"], row["table_id"], row["metric"])
        if ((panel in cross_study_panels or details(row).get("protocol_screen") is True)
                and eligible(row) and row["provenance"] == "original" and row["role"] in {"baseline", "proposed", "ablation"}):
            protocol = (row["block_id"], row["benchmark_version"], row["split"], row["backbone"], row["judge"])
            protocols[row["benchmark"]].setdefault(protocol, row)
    for panel in panels.values():
        for left, right in combinations(panel, 2):
            if left["configuration_id"] != right["configuration_id"]:
                yield pair_record(left, right, "within_block", *compare_pair(left, right))
    for variants in protocols.values():
        for left, right in combinations(variants.values(), 2):
            if left["paper_id"] == right["paper_id"]:
                continue
            status, reason = cross_protocol(left, right)
            record = pair_record(left, right, "cross_study_protocol", status, "protocol screen only", reason)
            for field in ("task", "metric", "unit", "left_observation", "right_observation",
                          "left_configuration", "right_configuration", "left_architecture", "right_architecture"):
                record[field] = ""
            record["split"] = f'{left["split"] or "[missing]"} | {right["split"] or "[missing]"}'
            yield record


def annotate(rows, contrasts):
    status_order = {"Missing": 0, "Incompatible": 1,
                    "Conditionally comparable": 2, "Directly comparable": 3}
    best = defaultdict(lambda: "Missing")
    for contrast in contrasts:
        if contrast["comparison_level"] == "within_block":
            for field in ("left_observation", "right_observation"):
                obs = contrast[field]
                if status_order[contrast["status"]] > status_order[best[obs]]:
                    best[obs] = contrast["status"]
    for row in rows:
        row["comparability_status"] = best[row["observation_id"]]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--input", type=Path, nargs="+")
    args = parser.parse_args()
    data = args.root / "data"
    if args.input:
        source = [
            row
            for path in args.input
            for row in (read_csv(path) if path.suffix == ".csv"
                        else json.loads(path.read_text(encoding="utf-8"))["observations"])
        ]
    else:
        source = read_csv(data / "raw_results.csv")
    manifest = {row["paper_id"]: row for row in read_csv(data / "cluster_b_paper_manifest.csv")}
    counts = {}
    for paper_id in {row["paper_id"] for row in source}:
        with pymupdf.open(args.root / "papers" / f"{paper_id}.pdf") as pdf:
            counts[paper_id] = len(pdf)
    rows = list(prepare(source, manifest, counts))
    contrasts = list(comparisons(rows))
    annotate(rows, contrasts)
    write_csv(data / "raw_results.csv", FIELDS, rows)
    verified = [row for row in rows if row["verification"] == "verified" and row["score"] != ""]
    write_csv(data / "validated_results.csv", FIELDS, verified)
    write_csv(data / "comparability.csv", COMPARISON_FIELDS, contrasts)
    print(f"{len(rows)} raw records; {len(verified)} verified displayed cells; "
          f"{sum(eligible(row) for row in verified)} non-excluded verified cells; "
          f"{len({row['configuration_id'] for row in verified})} verified configurations.")


if __name__ == "__main__":
    main()
