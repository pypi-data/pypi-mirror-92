"""
Tools for an access to the pre cached data.
"""
# import functools
import importlib
from pathlib import Path
import ec2_compare.utils as utils


# @functools.lru_cache()
def get(key: str, value: str) -> list:
    """
    Returns list of the instances by search key and it's value.

    More info: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html
    General info anout EC2 instances https://aws.amazon.com/ec2/instance-types/
    """
    _module_name = utils.module_name(search_key=key)
    try:
        _mod = importlib.import_module(
            "ec2_compare.internal.{mod}.{val}".format(
                mod=_module_name, val=value.lower()
            )
        )
        return _mod.get  # type: ignore

    except ModuleNotFoundError:

        val = list({
            x.stem
            for x in list(
                Path(Path(__file__).parent / f"internal/{_module_name}").glob(
                    "*.py"
                )
            )
            if x.is_file() and not x.stem.startswith("_")
        })
        if val:
            raise ValueError(f"The '{key}' has no '{value} in {val}") from None
        raise ValueError(f"Please check if {key} is legit") from None
