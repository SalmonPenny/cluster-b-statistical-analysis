"""Index local PDFs by page for targeted experimental screening."""
import argparse
import csv
from pathlib import Path
import re

import pymupdf


KEYWORDS = {
    "LongMemEval": r"long\s*mem\s*eval",
    "LoCoMo": r"\blocomo\b(?!\s*[-+]\s*plus|\s*\+)",
    "HaluMem": r"\bhalumem\b",
    "MemoryAgentBench": r"\bmemoryagentbench\b",
    "RealMem": r"\brealmem\b",
    "tables": r"\b(?:table|fig(?:ure)?\.?)\s*[A-Z]?\d+",
    "experiments": r"\b(?:experiments?|evaluation|benchmarks?|baselines?|ablation)\b",
    "metrics": r"\b(?:accuracy|precision|recall|hallucination|f1|rouge|exact match|llm.judge)\b",
    "common_systems": r"\b(?:mem0|a-mem|memgpt|langmem|supermemory|memoryos|rag)\b",
}


def index(root):
    for pdf in sorted((root / "papers").glob("*.pdf")):
        with pymupdf.open(pdf) as document:
            for number, page in enumerate(document, 1):
                text = page.get_text()
                yield {
                    "paper_id": pdf.stem,
                    "pdf_page": number,
                    "text_characters": len(text.strip()),
                    **{
                        name: len(re.findall(pattern, text, re.I))
                        for name, pattern in KEYWORDS.items()
                    },
                }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    output = args.output or args.root / "data" / "pdf_page_index.csv"
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, ["paper_id", "pdf_page", "text_characters", *KEYWORDS])
        writer.writeheader()
        writer.writerows(index(args.root))


if __name__ == "__main__":
    main()
