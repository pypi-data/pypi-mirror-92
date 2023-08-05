import json


class PhotoSize(object):
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
        file_size = json_obj.get("file_size")

        return cls(file_id, file_unique_id, width, height, file_size)

    def __init__(self, file_id, file_unique_id, width, height, file_size):
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.width = width
        self.height = height
        self.file_size = file_size

    @classmethod
    def get_photo_sizes(cls, message):
        result = []
        for m in message:
            result.append(PhotoSize._de_json(dict(m)))
        return result
