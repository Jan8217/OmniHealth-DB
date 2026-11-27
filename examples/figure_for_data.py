"""Plot aggregate statistics for the three OmniHealth-DB subsets.

Adapted from the dataset authors' original three-panel plotting script:
https://huggingface.co/datasets/ZhaokunYan/OmniHealth-DB/blob/1a496f8333c323f2af8a87ef98b388c1ef42fe76/code%20for%20data_/figure_for_data.py
The counts describe the released data documented in the Hugging Face dataset card.
"""

import argparse
from pathlib import Path

SUBSETS = ("Subset A", "Subset B", "Subset C")
PANELS = (
    (
        "Public-health domains",
        (
            ("Foundations and methods", (1667, 1667, 1666), "#2c3e50"),
            ("Non-communicable diseases", (1667, 1666, 1667), "#20638a"),
            ("Infectious disease prevention", (1666, 1667, 1667), "#287da8"),
        ),
    ),
    (
        "Released formats",
        (
            ("Question-answer", (2005, 0, 2004), "#1b7065"),
            ("Single-choice", (2995, 0, 2996), "#267660"),
            ("Multi-turn conversation", (0, 5000, 0), "#2c5447"),
        ),
    ),
    (
        "Languages",
        (
            ("English", (2956, 2955, 2955), "#694099"),
            ("French", (2044, 2045, 2045), "#8a569c"),
        ),
    ),
)


def plot_stacked(ax, title, bands):
    bottom = [0] * len(SUBSETS)
    for label, counts, color in bands:
        bars = ax.bar(SUBSETS, counts, bottom=bottom, label=label, color=color, width=0.55)
        for bar, count in zip(bars, counts):
            if count:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_y() + count / 2,
                    f"{count:,}",
                    ha="center",
                    va="center",
                    color="white",
                    fontsize=11,
                )
        bottom = [base + count for base, count in zip(bottom, counts)]
    ax.set_title(title)
    ax.set_ylim(0, 5500)
    ax.grid(axis="y", alpha=0.22)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), frameon=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--output", type=Path, default=Path("artifacts/omnihealth_distribution.png"),
        help="figure path such as artifacts/omnihealth_distribution.png",
    )
    args = parser.parse_args()

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    output = args.output if args.output.suffix else args.output.with_suffix(".png")
    output.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 3, figsize=(13, 5.7), sharey=True, layout="constrained")
    fig.suptitle("OmniHealth-DB dataset distribution", fontsize=17)
    axes[0].set_ylabel("Records")
    for ax, (title, bands) in zip(axes, PANELS):
        plot_stacked(ax, title, bands)
    fig.savefig(output, dpi=220, bbox_inches="tight")
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    main()
