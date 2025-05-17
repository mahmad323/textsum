import os
import zipfile
from urllib import request
from pathlib import Path
from textsum.logging import logger
from textsum.utils.common import get_size
from pathlib import Path
from textsum.entity import DataIngestionConfig


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self):
        """Download the dataset from the configured URL if not already present."""
        local_path = self.config.local_data_file
        if not os.path.exists(local_path):
            try:
                filename, headers = request.urlretrieve(
                    url=self.config.source_URL,
                    filename=local_path
                )
                logger.info(f"✅ Downloaded file: {filename}\n📦 Headers: {headers}")
            except Exception as e:
                logger.error(f"❌ Failed to download file from {self.config.source_URL}: {e}")
                raise e
        else:
            size = get_size(Path(local_path))
            logger.info(f"⚠️ File already exists at {local_path} (Size: {size})")

    def extract_zip_file(self):
        """Extracts the downloaded zip file into the specified directory."""
        try:
            unzip_path = self.config.unzip_dir
            os.makedirs(unzip_path, exist_ok=True)

            with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
                zip_ref.extractall(unzip_path)

            logger.info(f"✅ Extraction completed. Files extracted to: {unzip_path}")
        except Exception as e:
            logger.error(f"❌ Failed to extract zip file {self.config.local_data_file}: {e}")
            raise e
