from transform.base_transform import BaseTransform
from typing import List


class TransformsManager:
    def __init__(self, transforms: List[BaseTransform]) -> None:
        self.transforms = transforms

    def transform_all(self, data: dict) -> None:
        for transform in self.transforms:
            transform.tranform(data)