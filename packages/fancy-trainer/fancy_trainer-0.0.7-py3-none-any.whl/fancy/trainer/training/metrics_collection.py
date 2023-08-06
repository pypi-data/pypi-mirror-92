from dataclasses import dataclass
from typing import List, Optional

from ..metrics import MetricBase


@dataclass
class MetricsCollection:
    train_metrics: List[MetricBase]
    test_metrics: List[MetricBase]
    valid_metrics: Optional[List[MetricBase]] = None
