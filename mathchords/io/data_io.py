import os
import pickle as pkl
from pathlib import Path

# Loader functions

def load(data_addr: str | Path) -> dict:
    """
    Chords data loader to store as consts.

    Args:
        data_addr (str): Data file address (.pkl file)

    Returns:
        Dict[str, Any]: Expected structure of data file
    """
    with open(data_addr, "rb") as data_file:
        return pkl.load(data_file)

def save(data: dict, data_addr: str | Path) -> None:
    """_summary_

    Args:
        data (dict): _description_
        data_addr (str): _description_

    Returns:
        _type_: _description_
    """
    os.makedirs(os.path.dirname(data_addr), exist_ok=True)
    with open(data_addr, "wb") as data_file:
        pkl.dump(data, data_file)
        