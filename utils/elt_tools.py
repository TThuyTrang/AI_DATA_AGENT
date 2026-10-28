import os
from pathlib import Path

import requests
import pandas as pd


class ETLTools:

    def __init__(self):
        # Project root: DATA_AGENT/
        self.project_root = Path(__file__).resolve().parent.parent

    def extract_load(self, url: str, output_folder: str, format: str):
        """Extract API data and save it to the project directory."""

        output_dir = self.project_root / output_folder
        output_dir.mkdir(parents=True, exist_ok=True)

        filename = output_dir / f"extracted_data.{format}"

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()

            if "results" not in data:
                return "Failed: API response does not contain 'results'."

            df = pd.json_normalize(data["results"])

            if format == "csv":
                df.to_csv(filename, index=False)
            elif format == "json":
                df.to_json(filename, orient="records", lines=True)
            elif format == "parquet":
                df.to_parquet(filename, index=False)
            else:
                return f"Unsupported format: {format}"

            return f"Data successfully saved to {filename}"

        except (requests.exceptions.RequestException, ValueError, KeyError) as e:
            return f"Failed to extract data: {e}"

    def transform_load_context(self, file_path: str):
        """Read a supported file and return its first three rows."""

        path = Path(file_path)

        # Allow paths relative to DATA_AGENT/
        if not path.is_absolute():
            path = self.project_root / path

        if not path.is_file():
            return f"File not found: {path}"

        extension = path.suffix.lower()

        try:
            if extension == ".csv":
                df = pd.read_csv(path)
            elif extension == ".json":
                df = pd.read_json(path, lines=True)
            elif extension == ".parquet":
                df = pd.read_parquet(path)
            else:
                return f"Unsupported file format: {extension}"

            return df.head(3).to_string(index=False)

        except (OSError, ValueError, ImportError) as e:
            return f"Failed to read data: {e}"


if __name__ == "__main__":
    obj = ETLTools()

    path = "data/extract/extracted_data.csv"
    print(obj.transform_load_context(path))