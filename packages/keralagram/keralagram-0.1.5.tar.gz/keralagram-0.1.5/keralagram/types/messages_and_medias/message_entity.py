import json
from ..users_and_chats.user import User


class MessageEntity(object):

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

        type = json_obj.get("type")
        offset = json_obj.get("offset")
        length = json_obj.get("length")
        url = json_obj.get("url")
        if json_obj.get("user") is not None:
            user = User._de_json(dict(json_obj.get("user")))
        else:
            user = None
        language = json_obj.get("language")

        return cls(type, offset, length, url, user, language)

    def __init__(self, type, offset, length, url, user, language):
        self.type = type
        self.offset = offset
        self.length = length
        self.url = url
        self.user = user
        self.language = language

    @classmethod
    def parse_entities(cls, message_entity):
        result = []
        for me in message_entity:
            result.append(MessageEntity._de_json(dict(me)))
        return result
