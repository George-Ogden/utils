import numpy as np
import os

from ml_utils import SaveableObject

from tests.config import cleanup, requires_cleanup, SAVE_DIR

class SaveableModel(SaveableObject):
    SEPARATE_ATTRIBUTES = []
    DEFAULT_FILENAME = "model"
    number: int = 1

def save_load(object: SaveableObject) -> SaveableObject:
    object.save(SAVE_DIR)
    new_object = type(object).load(SAVE_DIR)
    assert type(new_object) == type(object)
    return new_object

@requires_cleanup
def test_saveable_object_saves():
    SaveableObject.DEFAULT_FILENAME = "file"
    object = SaveableObject()
    object.save(SAVE_DIR)

    assert os.path.exists(SAVE_DIR)
    assert os.path.exists(os.path.join(SAVE_DIR, object.DEFAULT_FILENAME))
    assert os.path.getsize(os.path.join(SAVE_DIR, object.DEFAULT_FILENAME)) > 0

    # cleanup
    SaveableObject.DEFAULT_FILENAME = None

@requires_cleanup
def test_saveable_object_saves_and_loads():
    SaveableObject.DEFAULT_FILENAME = "file"
    object1 = SaveableObject()
    object2 = save_load(object1)
    assert object1.DEFAULT_FILENAME == object2.DEFAULT_FILENAME

    # cleanup
    SaveableObject.DEFAULT_FILENAME = None

@requires_cleanup
def test_saveable_object_saves_and_loads_with_separate_attributes():
    SaveableObject.DEFAULT_FILENAME = "file"
    SaveableObject.SEPARATE_ATTRIBUTES = ["model"]
    object1 = SaveableObject()
    object1.model = SaveableModel()
    object1.model.number = 2
    object2 = save_load(object1)
    assert os.path.exists(os.path.join(SAVE_DIR, SaveableModel.DEFAULT_FILENAME))
    assert np.all(object1.model.number == object2.model.number)

    # cleanup
    SaveableObject.DEFAULT_FILENAME = None
    SaveableObject.SEPARATE_ATTRIBUTES = []