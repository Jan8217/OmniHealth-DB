"""Inspect aggregate OmniHealth-DB split sizes from Hugging Face."""

import argparse
import json
from urllib.parse import urlencode
from urllib.request import urlopen

DATASET = "ZhaokunYan/OmniHealth-DB"
SUBSETS = ("A_preference", "B_multiturn", "C_audience_adaptation")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--subset", choices=SUBSETS, help="report only one subset")
    args = parser.parse_args()

    query = urlencode({"dataset": DATASET})
    subsets = [args.subset] if args.subset else SUBSETS
    try:
        with urlopen(f"https://datasets-server.huggingface.co/size?{query}", timeout=20) as response:
            metadata = json.load(response)
        test_splits = {row["config"]: row for row in metadata["size"]["splits"] if row["split"] == "test"}
        rows = [
            {
                "subset": name,
                "split": "test",
                "rows": test_splits[name]["num_rows"],
                "columns": test_splits[name]["num_columns"],
            }
            for name in subsets
        ]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f"Could not read Hugging Face split metadata: {exc}\n")

    print(json.dumps({"dataset": DATASET, "rows": sum(row["rows"] for row in rows), "subsets": rows}, indent=2))


if __name__ == "__main__":
    main()
