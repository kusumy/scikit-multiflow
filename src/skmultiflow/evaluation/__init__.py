"""
The :mod:`skmultiflow.evaluation` module includes evaluation methods for stream learning.
"""

from .evaluate_prequential import EvaluatePrequential
from .evaluate_prequential_delayed import EvaluatePrequentialDelayed
from .evaluate_holdout import EvaluateHoldout
from .evaluation_data_buffer import EvaluationDataBuffer

__all__ = [
    "EvaluatePrequential",
    "EvaluatePrequentialDelayed",
    "EvaluateHoldout",
    "EvaluationDataBuffer"]
