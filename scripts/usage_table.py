"""The token kinds usage.py totals, and how it prints them."""

from collections.abc import Mapping

KINDS = (
    "input_tokens",
    "cache_creation_input_tokens",
    "cache_read_input_tokens",
    "output_tokens",
)


def show(totals: Mapping[str, Mapping[str, int]]) -> None:
    """Each model, then one aligned line per token kind."""
    for model, counts in totals.items():
        print(model)
        for kind in KINDS:
            print(f"  {kind:<28} {counts.get(kind, 0):>8}")
