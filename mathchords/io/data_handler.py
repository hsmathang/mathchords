import os
from pathlib import Path
from .data_io import load, save

# Loader classes
class Experiment:
    def __init__(self, addr: str) -> None:
        self.addr = addr
        self.name = addr.split("/")[-1].split(".")[0]
        self.data = load(addr)
    
    def update(self, data):
        save(data, self.addr)

class ExperimentHandler:
    def __init__(self, base_addr) -> None:
        self.base_addr = Path(base_addr)
        self.file_list = self.get_files()

    def get_files(self) -> list:
        files_list = []
        for file_name in os.listdir(self.base_addr):
            file_path = os.path.join(self.base_addr, file_name)
            if os.path.isfile(file_path):
                files_list.append(file_name)
        return files_list

    def read(self, file_name: str) -> dict:
        addr = self.base_addr.joinpath(file_name)
        return load(addr)

    def write(self, data: dict, file_name: str) -> None:
        addr = self.base_addr.joinpath(file_name)
        save(data, addr)