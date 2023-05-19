import abc
from dataclasses import dataclass
from typing import Callable, Optional

from etl.extractors.base import Extractor
from etl.loaders.base import Loader
from etl.transformers.base import Transformer


@dataclass(slots=True)
class Pipeline:
    extractor: Extractor
    transformer: Transformer
    loader: Loader
    post_load_handler: Optional[Callable] = None

    def run(self):
        for bunch in self.extractor.extract():
            transformed_data = self.transformer.transform(bunch)
            success = self.loader.load(transformed_data)
            if self.post_load_handler:
                self.post_load_handler(success=success, row_data=bunch, transformed_data=transformed_data)


class ETL:
    @abc.abstractmethod
    def run(self) -> None:
        pass


def run_pipelines(pipelines: list[Pipeline]) -> None:
    for pipeline in pipelines:
        pipeline.run()
