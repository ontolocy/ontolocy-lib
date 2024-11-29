from abc import abstractmethod
from hashlib import sha256
from pathlib import Path

import requests

from ..ingester import IngesterBase


class OntolocyParser(IngesterBase):
    def detect(self, input_data) -> bool:
        return self._detect(input_data)

    def parse_data(self, input_data, populate=True):
        if self.detect(input_data) is False:
            raise ValueError(
                "Detection suggests input data is not valid for this parser"
            )

        if self.private_namespace is None and self.auto_namespace is True:
            private_namespace = sha256(input_data.encode("utf-8")).hexdigest()

        else:
            private_namespace = self.private_namespace

        self._process_data(input_data, private_namespace)

        if populate is True:
            self.populate()

    def parse_file(self, file_path, populate=True):
        with open(file_path, "r") as f:  # type: ignore [arg-type]
            data = f.read()

        input_data = str(data)

        self.parse_data(input_data, populate=populate)

    def parse_directory(
        self, dir_path, populate: bool = True, path_pattern: str = "**/*"
    ):
        path = Path(dir_path)
        for file_path in path.glob(path_pattern):
            # if we're parsing a directory, don't populate until we've parsed all files
            self.parse_file(file_path, populate=False)

        if populate is True:
            self.populate()

    def parse_url(self, url, populate=True):
        response = requests.get(url)

        data = response.text

        input_data = str(data)

        self.parse_data(input_data, populate=populate)

    @abstractmethod
    def _detect(self, input_data) -> bool:
        """Implement code which returns True if it's valid for this parser
        and returns False otherwise.
        """

        raise NotImplementedError
