from dataclasses import dataclass
from typing import ClassVar

from ml_utils.config import Config, DefaultTrainingConfig

def test_config_with_all_attrs():
    @dataclass
    class CustomConfig(Config):
        name: str = "hello"
        number: int = 12
    
    assert dict(**CustomConfig()) == dict(name="hello", number=12)

def test_config_with_restricted_attrs():
    @dataclass
    class CustomConfig(Config):
        name: str = "hello"
        number: int = 12
        cls_attr: ClassVar[float] = .5
    
    assert dict(**CustomConfig()) == dict(name="hello", number=12)

def test_default_training_config():
    training_config = DefaultTrainingConfig()
    for k in (
        "batch_size",
        "lr",
        "epochs",
    ):
        assert k in training_config.keys()
        assert hasattr(training_config, k)

def test_custom_training_config():
    @dataclass
    class CustomTrainingConfig(DefaultTrainingConfig):
        epochs: int = 54
        lr: float = 11e-4
    training_config = CustomTrainingConfig()
    assert training_config.epochs == 54
    assert training_config.lr == 11e-4