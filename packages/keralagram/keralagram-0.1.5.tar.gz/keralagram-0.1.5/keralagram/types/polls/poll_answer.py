import json
from ..users_and_chats.user import User


class PollAnswer(object):
    @classmethod
    def _de_json(cls, json_str):
        if json_str is None:
            return None
        if isinstance(json_str, dict):
            json_obj = json_str
        elif isinstance(json_str, str):
            json_obj = json.loads(json_str)
        else:
            raise ValueError("Expected dict or str type")
        poll_id = json_obj.get("poll_id")
        if json_obj.get("user") is not None:
            user = User._de_json(dict(json_obj['user']))
        else:
            user = None
        option_ids = json_obj.get("option_ids")
