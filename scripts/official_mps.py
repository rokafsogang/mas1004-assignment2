"""Run src/official.py, unchanged, on an Apple GPU (MPS).

With torch 2.6, official.py stops on MPS in the first backward pass:
"view size is not compatible with input tensor's size and stride". It comes
from the channels_last memory format official.py asks for. This wrapper only
turns `.to(memory_format=torch.channels_last)` into a no-op, so tensors keep
the default layout; the arithmetic, the recipe, the selection, the budget and
the seeds are exactly those of official.py. Same arguments as official.py:

    uv run python scripts/official_mps.py --tag baseline
    uv run python scripts/official_mps.py --quick
"""

import sys
from pathlib import Path

import torch

_CHANNELS_LAST = torch.channels_last


def _without_channels_last(original):
    def to(self, *args, **kwargs):
        if kwargs.get("memory_format") is _CHANNELS_LAST:
            kwargs.pop("memory_format")
            if not args and not kwargs:
                return self
        return original(self, *args, **kwargs)
    return to


torch.Tensor.to = _without_channels_last(torch.Tensor.to)
torch.nn.Module.to = _without_channels_last(torch.nn.Module.to)

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import official  # noqa: E402

if __name__ == "__main__":
    official.main()
