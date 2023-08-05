import asyncio
import re
from .types import Update, Message
from .bot import KeralaGram
from typing import Union
from keralagram import __version__


class Dispatcher(object):

    def __init__(self, bot):
        if not isinstance(bot, KeralaGram):
            raise TypeError(f'Expected class KeralaGram got {type(bot).__name__}')

        self.bot = bot
        self.running = False
        self._commands = []
        self.process_loop = asyncio.get_event_loop()
        self.plugins = self.bot.plugins

    def loop(self):
        self.running = True
        while self.running:
            updates = self.bot._retrieve_updates(offset=self.bot._offset + 1)
            self.process_updates(updates)

    def run(self):
        loop = asyncio.get_event_loop()
        bot = self.bot._get_bot()
        print(f"KeralaGram version : {__version__}")
        print(f'KeralaGram (Bot) started on {bot.username}')
        run_up = asyncio.ensure_future(self.loop())
        try:
            loop.run_until_complete(run_up)
        except KeyboardInterrupt:
            run_up.cancel()
            self.stop()
            quit()

    def stop(self):
        quit()
        self.running = False

    def on_command(self, command: str, prefixes: Union[list, str] = None):
        def decorator(func):
            self.add_command(command, func, prefixes)
        return decorator

    def add_command(self, command, function, prefixes: Union[list, str] = None):
        self._commands.append((command, function, prefixes))

    def process_command_update(self, message: Message):
        if message is not None:
            for commands, handler, prefixes in self._commands:
                if message.text is not None:
                    if prefixes is not None:
                        if type(prefixes) is str:
                            if message.text.startswith(prefixes):
                                pass
                        else:
                            for pre in prefixes:
                                if message.text.startswith(pre):
                                    pass
                    else:
                        if message.text.startswith("/"):
                            pass
                        else:
                            return

                    m = re.search(commands, message.text, re.I)
                    if m:
                        message.bot = self.bot
                        return self.process_loop.run_until_complete(handler(self.bot, message))

    def process_updates(self, updates: list[Update]):
        for update in updates:
            self.bot._offset = max(self.bot._offset, update.update_id)
            if len(self._commands) != 0:
                self.process_command_update(update.message)
