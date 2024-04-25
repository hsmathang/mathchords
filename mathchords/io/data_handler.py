from pathlib import Path
from .data_io import load, save

# Loader classes

class ExperimentHandler:
    def __init__(self, base_addr) -> None:
        self.base_addr = Path(base_addr)

    def read(self, file_name: str) -> dict:
        addr = self.base_addr.joinpath(file_name)
        return load(addr)

    def write(self, data: dict, file_name: str) -> None:
        addr = self.base_addr.joinpath(file_name)
        save(data, addr)