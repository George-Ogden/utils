from dataclasses import dataclass
from typing import Optional

from .config import Config

@dataclass
class DefaultTrainingConfig(Config):
    epochs: int = 10
    """number of epochs to train model for"""
    batch_size: int = 256
    """batch size"""
    training_patience: Optional[int] = 7
    """number of epochs without improvement during training"""
    lr: float = 1e-3
    """learning rate"""
    validation_split: float = 0.1
    """proportion of data to validate on"""
    optimizer_type: str = "Adam"