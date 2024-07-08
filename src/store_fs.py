import os
from interfaces import Store
from loguru import logger


class FSStore(Store):
    def __init__(self, base_path: str):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    def upload(self, key: str, data: bytes):
        full_path = os.path.join(self.base_path, key)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        logger.info(f"Uploading data to filesystem with key: {key}")
        with open(full_path, "wb") as f:
            f.write(data)

    def download(self, key: str) -> bytes:
        with open(f"{self.base_path}/{key}", "rb") as f:
            data = f.read()
        logger.info(f"Downloaded data from filesystem with key: {key}")
        return data

    def exists(self, key: str) -> bool:
        exists = os.path.exists(f"{self.base_path}/{key}")
        logger.info(
            f"Data {'exists' if exists else 'does not exist'} in filesystem key: {key}"
        )
        return exists
