import json


class User(object):
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
        id = json_obj.get("id")
        is_bot = json_obj.get("is_bot")
        first_name = json_obj.get("first_name")
        last_name = json_obj.get("last_name")
        username = json_obj.get("username")
        lang_code = json_obj.get("language_code")
        can_join_groups = json_obj.get("can_join_groups")
        can_read_all_messages = json_obj.get("can_read_all_group_messages")
        supports_inline_queries = json_obj.get("supports_inline_queries")

        return cls(id, is_bot, first_name, last_name, username, lang_code, can_read_all_messages,
                   can_join_groups, supports_inline_queries)

    def __init__(self, id, is_bot, first_name, last_name, username, lang_code,
                 can_read_all_messages, can_join_groups, supports_inline_queries):
        self.id = id
        self.is_bot = is_bot,
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.lang_code = lang_code
        self.can_join_groups = can_join_groups,
        self.can_read_all_messages = can_read_all_messages
        self.supports_inline_queries = supports_inline_queries
