import json
from .photo_size import PhotoSize


class Animation(object):
    @classmethod
    def _de_json(cls, json_str: dict):
        if json_str is None:
            return None
        if isinstance(json_str, dict):
            json_obj = json_str
        elif isinstance(json_str, str):
            json_obj = json.loads(json_str)
        else:
            raise ValueError("Expected dict or str type")

        file_id = json_obj.get("file_id")
        file_unique_id = json_obj.get("file_unique_id")
        width = json_obj.get("width")
        height = json_obj.get("height")
        duration = json_obj.get("duration")
        if json_obj.get("thumb") is not None:
            thumb = PhotoSize._de_json(dict(json_obj.get("thumb")))
        else:
            thumb = None
        file_name = json_obj.get("file_name")
        mime_type = json_obj.get("mime_type")
        file_size = json_obj.get("file_size")

        return cls(file_id, file_unique_id, width, height, duration, thumb, file_name,
                   mime_type, file_size)

    def __init__(self, file_id, file_unique_id, width, height, duration, thumb, file_name,
                 mime_type, file_size):
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.width = width
        self.height = height
        self.duration = duration
        self.thumb = thumb
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = file_size
