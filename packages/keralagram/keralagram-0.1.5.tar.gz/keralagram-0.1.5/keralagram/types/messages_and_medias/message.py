import json
from ..users_and_chats.user import User
from ..users_and_chats.chat import Chat
from .animation import Animation
from .message_entity import MessageEntity
from .photo_size import PhotoSize
from ..polls.poll import Poll
from ..polls.poll_answer import PollAnswer


class Message(object):
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
        message_id = json_obj.get("message_id")
        date = json_obj.get("date")
        text = json_obj.get("text")
        if json_obj.get("chat") is not None:
            chat = Chat._de_json(dict(json_obj['chat']))
        else:
            chat = None
        if json_obj.get("sender_chat") is not None:
            sender_chat = Chat._de_json(dict(json_obj['sender_chat']))
        else:
            sender_chat = None
        forward_from_message_id = json_obj.get("forward_from_message_id")
        forward_signature = json_obj.get("forward_signature")
        forward_sender_name = json_obj.get("forward_sender_name")
        forward_date = json_obj.get("forward_date")
        edit_date = json_obj.get("edit_date")
        media_group_id = json_obj.get("media_group_id")
        author_signature = json_obj.get("author_signature")
        caption = json_obj.get("caption")
        new_chat_title = json_obj.get("new_chat_title")
        delete_chat_photo = json_obj.get("delete_chat_photo")
        group_chat_created = json_obj.get("group_chat_created")
        supergroup_chat_created = json_obj.get("supergroup_chat_created")
        channel_created = json_obj.get("channel_chat_created")
        migrate_to_chat_id = json_obj.get("migrate_to_chat_id")
        migrate_from_chat_id = json_obj.get("migrate_from_chat_id")
        connected_website = json_obj.get("connected_website")
        if json_obj.get("pinned_message") is not None:
            pinned_message = Message._de_json(dict(json_obj["pinned_message"]))
        else:
            pinned_message = None
        if json_obj.get("from") is not None:
            from_user = User._de_json(dict(json_obj["from"]))
        else:
            from_user = None

        if json_obj.get("forward_from") is not None:
            forward_from = User._de_json(dict(json_obj["forward_from"]))
        else:
            forward_from = None

        if json_obj.get("forward_from_chat") is not None:
            forward_from_chat = Chat._de_json(dict(json_obj['forward_from_chat']))
        else:
            forward_from_chat = None

        if json_obj.get("via_bot") is not None:
            via_bot = User._de_json(dict(json_obj["via_bot"]))
        else:
            via_bot = None

        if json_obj.get("reply_to_message") is not None:
            reply_to_message = Message._de_json(dict(json_obj["reply_to_message"]))
        else:
            reply_to_message = None

        if json_obj.get("animation") is not None:
            animation = Animation._de_json(dict(json_obj['animation']))
        else:
            animation = None

        if json_obj.get("entities") is not None:
            entities = MessageEntity.parse_entities(json_obj['entities'])
        else:
            entities = None

        if json_obj.get("caption_entities") is not None:
            caption_entities = MessageEntity.parse_entities(json_obj['caption_entities'])
        else:
            caption_entities = None

        if json_obj.get("photo") is not None:
            photo = PhotoSize.get_photo_sizes(json_obj['photo'])
        else:
            photo = None

        if json_obj.get("new_chat_photo") is not None:
            new_chat_photo = PhotoSize.get_photo_sizes(json_obj['new_chat_photo'])
        else:
            new_chat_photo = None

        return cls(message_id, date, text, chat, forward_from_message_id, forward_signature,
                   forward_sender_name, forward_date, edit_date, media_group_id, author_signature,
                   caption, new_chat_title, delete_chat_photo, group_chat_created, supergroup_chat_created,
                   channel_created, migrate_to_chat_id, migrate_from_chat_id, connected_website,
                   pinned_message, from_user, forward_from, via_bot, sender_chat, forward_from_chat, reply_to_message,
                   animation, entities, caption_entities, photo, new_chat_photo)

    def __init__(self, message_id, date, text, chat, forward_from_message_id, forward_signature,
                 forward_sender_name, forward_date, edit_date, media_group_id, author_signature,
                 caption, new_chat_title, delete_chat_photo, group_chat_created, supergroup_chat_created,
                 channel_created, migrate_to_chat_id, migrate_from_chat_id, connected_website,
                 pinned_message, from_user, forward_from, via_bot, sender_chat, forward_from_chat, reply_to_message,
                 animation, entities, caption_entities, photo, new_chat_photo):
        self.message_id = message_id
        self.date = date
        self.text = text
        self.chat = chat
        self.forward_from_message_id = forward_from_message_id
        self.forward_signature = forward_signature
        self.forward_sender_name = forward_sender_name
        self.forward_date = forward_date
        self.forward_from = forward_from
        self.from_user = from_user
        self.edit_date = edit_date
        self.entities = entities
        self.media_group_id = media_group_id
        self.author_signature = author_signature
        self.caption = caption
        self.new_chat_title = new_chat_title
        self.delete_chat_photo = delete_chat_photo
        self.group_chat_created = group_chat_created
        self.supergroup_chat_created = supergroup_chat_created
        self.channel_created = channel_created
        self.migrate_to_chat_id = migrate_to_chat_id
        self.migrate_from_chat_id = migrate_from_chat_id
        self.connected_website = connected_website
        self.pinned_message = pinned_message
        self.via_bot = via_bot
        self.caption_entities = caption_entities
        self.sender_chat = sender_chat
        self.photo = photo
        self.new_chat_photo = new_chat_photo
        self.reply_to_message = reply_to_message
        self.forward_from_chat = forward_from_chat
        self.animation = animation

    async def reply_text(self, text, parse_mode: str = None, reply_markup=None,
                         disable_preview: bool = None, disable_notification: bool = None):
        updates = await self.bot.send_message(self.chat.id, text, reply_message_id=self.message_id,
                                              reply_markup=reply_markup, disable_preview=disable_preview,
                                              disable_notification=disable_notification, parse_mode=parse_mode)


class Update(object):
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
        update_id = json_obj.get('update_id')
        if json_obj.get('message') is not None:
            message = Message._de_json(dict(json_obj['message']))
        elif json_obj.get('edited_message') is not None:
            message = Message._de_json(dict(json_obj['edited_message']))
        elif json_obj.get('channel_post') is not None:
            message = Message._de_json(dict(json_obj['channel_post']))
        elif json_obj.get('edited_channel_post') is not None:
            message = Message._de_json(dict(json_obj['edited_channel_post']))
        else:
            message = None

        if json_obj.get('inline_query') is not None:
            inline_query = InlineQuery._de_json(dict(json_obj['inline_query']))
        else:
            inline_query = None

        if json_obj.get("callback_query") is not None:
            callback_query = CallbackQuery._de_json(dict(json_obj['callback_query']))
        else:
            callback_query = None

        if json_obj.get("poll") is not None:
            poll = Poll._de_json(dict(json_obj['poll']))
        else:
            poll = None

        if json_obj.get("poll_answer") is not None:
            poll_answer = PollAnswer._de_json(dict(json_obj['poll_answer']))
        else:
            poll_answer = None
        return cls(update_id, message, inline_query, callback_query, poll, poll_answer)

    def __init__(self, update_id, message, inline_query, callback_query, poll, poll_answer):
        self.update_id = update_id
        self.message = message
        self.inline_query = inline_query
        self.callback_query = callback_query
        self.poll = poll
        self.poll_answer = poll_answer


class InlineQuery(object):
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
        from_user = User._de_json(dict(json_obj.get("from")))
        query = json_obj.get("query")
        offset = json_obj.get("offset")
        return cls(id, from_user, query, offset)

    def __init__(self, id, from_user, query, offset):
        self.id = id
        self.from_user = from_user
        self.query = query
        self.offset = offset

class CallbackQuery(object):
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
        if json_obj.get("from") is not None:
            from_user = User._de_json(dict(json_obj['from']))
        else:
            from_user = None

        if json_obj.get("message") is not None:
            message = Message._de_json(dict(json_obj['message']))
        else:
            message = None

        inline_message_id = json_obj.get("inline_message_id")
        chat_instance = json_obj.get("chat_instance")
        data = json_obj.get("data")
        game_short_name = json_obj.get("game_short_name")

        return cls(id, from_user, message, inline_message_id, chat_instance,
                   data, game_short_name)

    def __init__(self, id, from_user, message, inline_message_id, chat_instance,
                 data, game_short_name):
        self.id = id
        self.from_user = from_user
        self.message = message
        self.inline_message_id = inline_message_id
        self.chat_instance = chat_instance
        self.data = data
        self.game_short_name = game_short_name


