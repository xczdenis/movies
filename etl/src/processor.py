import time
from dataclasses import dataclass
from typing import Callable, Optional

from extractors.interface import IExtractor
from loaders.interface import ILoader
from transformers.interface import ITransformer


@dataclass
class Pipeline:
    extractor: IExtractor
    transformer: ITransformer
    loader: ILoader
    post_load_handler: Optional[Callable] = None

    def run(self):
        for bunch in self.extractor.extract():
            transformed_data = self.transformer.transform(bunch)
            success = self.loader.load(transformed_data)
            if self.post_load_handler:
                self.post_load_handler(success=success, row_data=bunch, transformed_data=transformed_data)


@dataclass
class ETLProcessor:
    pipelines: list[Pipeline]

    def start(self, repeat_interval: int = 0):
        if repeat_interval > 0:
            while True:
                self.transfer_data()
                time.sleep(repeat_interval)
        else:
            self.transfer_data()

    def transfer_data(self):
        for pipeline in self.pipelines:
            pipeline.run()
