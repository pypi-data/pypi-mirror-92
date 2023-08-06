"""Handlers for honeybee model."""
import os
import json
import tempfile
import uuid
from honeybee.model import Model


def model_to_json(model_obj):
    """Translate a Honeybee model to a HBJSON file.

        Args:
            model_obj: Either a Honeybee model or the path to the HBJSON file.
                In case the model_obj is a path it will be returned as is. For HBModels
                the model will be saved to a HBJSON file in a temp folder.

        Returns:
            str -- Path to HBJSON file.
    """
    if isinstance(model_obj, str):
        if not os.path.isfile(model_obj):
            raise ValueError('Invalid file path: %s' % model_obj)
        hb_file = model_obj
    elif isinstance(model_obj, Model):
        file_name = str(uuid.uuid4())[:6]
        temp_dir = tempfile.gettempdir()
        hb_file = os.path.join(temp_dir, file_name + '.hbjson')

        try:
            obj_dict = model_obj.to_dict(abridged=True)
        except TypeError:  # no abridged option
            obj_dict = model_obj.to_dict()

        # write the dictionary into a file
        with open(hb_file, 'w') as fp:
            json.dump(obj_dict, fp)
    else:
        raise ValueError(
            'Model input should be a string or a Honeybee Model not a ' + type(model_obj)
        )
    return hb_file
