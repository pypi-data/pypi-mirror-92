import json
from ..users_and_chats.user import User
from ..messages_and_medias.location import Location


class ChosenInlineResult(object):
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

        result_id = json_obj.get("result_id")
        if json_obj.get("from") is not None:
            from_user = User._de_json(dict(json_obj['from']))
        else:
            from_user = None

        if json_obj.get("location") is not None:
            location = Location._de_json(dict(json_obj['location']))
        else:
            location = None
        inline_message_id = json_obj.get("inline_message_id")
        query = json_obj.get("query")

        return cls(result_id, from_user, location, inline_message_id, query)

    def __init__(self, result_id, from_user, location, inline_message_id, query):
        self.result_id = result_id
        self.from_user = from_user
        self.location = location
        self.inline_message_id = inline_message_id
        self.query = query
