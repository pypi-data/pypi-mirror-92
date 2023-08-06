import json
import os

from pollination_handlers.inputs.model import model_to_json
from honeybee.model import Model


def test_read_model_str():
    res = model_to_json('./tests/assets/two_rooms.hbjson')
    assert res.replace('\\', '/').endswith('tests/assets/two_rooms.hbjson')


def test_read_model_object():
    with open('./tests/assets/two_rooms.hbjson') as hb_model:
        data = hb_model.read()
    data = json.loads(data)
    model = Model.from_dict(data)

    res = model_to_json(model)
    assert os.path.isfile(res)
