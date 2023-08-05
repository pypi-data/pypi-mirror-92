import json


class PollOption(object):
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
        text = json_obj.get("text")
        voter_count = json_obj.get("voter_count")

        return cls(text, voter_count)

    def __init__(self, text, voter_count):
        self.text = text
        self.voter_count = voter_count

    @classmethod
    def get_poll_options(cls, message):
        result = []
        for m in message:
            result.append(PollOption._de_json(dict(m)))
        return result
