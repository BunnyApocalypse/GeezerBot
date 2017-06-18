""" Command registrar """

import importlib
import sys
from abc import abstractmethod, abstractclassmethod, ABCMeta
import config as conf


__all__ = ['bot_command', 'AbstractCommand', 'CommandRegistrar']


def bot_command(cls):
    """ Decorator that will register a class as a bot command """
    command = cls()

    if not issubclass(command.__class__, AbstractCommand):
        print(f'[ERROR] {command.__module__} does not have an implementation of AbstractCommand and wont be loaded.')
        return

    command_registrar = CommandRegistrar.get_singleton()

    for alias in command.aliases:
        if alias.lower() not in command_registrar.command_table.keys():
            command_registrar.command_table[alias.lower()] = command

    # return command # not sure if needed

class AbstractCommand(metaclass=ABCMeta):
    """ Template for bot command classes. """
    @property
    @abstractmethod
    def name(self):
        """ The name of this command """
        raise NotImplementedError

    @property
    @abstractmethod
    def aliases(self):
        """ The aliases that can be used to call this command """
        raise NotImplementedError

    @property
    @abstractmethod
    def enabled(self):
        """ The aliases that can be used to call this command """
        return self.enabled

    @enabled.setter
    @abstractmethod
    def enabled(self, value):
        """ Setter for `enabled` """
        self.enabled = value

    @staticmethod
    @abstractclassmethod
    def execute(shards, client, msg):
        """
        Executes this instances command
        :param shards:
        :type shards: list(discord.Client)
        :type client: discord.Client
        :type msg: discord.Message
        """
        raise NotImplementedError


class CommandRegistrar(object):
    """A singleton that manages the command table and command execution."""
    _instance = None

    @property
    def loaded_commands(self):
        """ return a list of loaded commands """
        return [command.name for command in set(self.command_table.values())]

    @property
    def loaded_aliases(self):
        """ return a list of loaded aliases """
        return list(self.command_table.keys())

    @staticmethod
    def get_singleton():
        """Get an instance of the `BotCommandRegistrar` singleton
        :return `BotCommandRegistrar`
        """
        if not CommandRegistrar._instance:
            CommandRegistrar._instance = CommandRegistrar()
        return CommandRegistrar._instance

    def __init__(self):
        """ instantiate the command table """
        self.command_table = {}

    @staticmethod
    def load_command(command_name):
        """ load a command module """
        try:
            importlib.import_module(f'commands.{command_name.lower()}')
            return True
        except ModuleNotFoundError:
            return False

    def unload_command(self, command_name):
        """ Reload a command module """

        if command_name.lower() in self.loaded_aliases:
            command = self.command_table[command_name]
            module_name = command.__module__

            # remove references to this command from the command table
            to_delete = [k for k, v in self.command_table.items() if v is command]
            for i in to_delete:
                del self.command_table[i]

            # I don't this it can ever not be loaded here but just in case...
            if module_name in sys.modules:
                del sys.modules[module_name]
                return True
        return False

    def reload_command(self, command_name):
        """ unload and load a command, ez """

        if command_name.lower() not in self.loaded_aliases:
            return False

        module_name = self.command_table[command_name.lower()].__module__.replace('commands.', '')

        if self.unload_command(command_name) and self.load_command(module_name):
            return True
        return False

    async def execute_command(self, shards, client, msg):
        """ This is bad, pls dont judge, Ima fix it soon """
        if msg.content.startswith('!'):
            command_name = msg.content[1:].split()[0].lower()  # slice off the prefix and split to get the command

        if command_name not in self.command_table:
            return

        if self.command_table[command_name].enabled:
            await self.command_table[command_name].execute(shards, client, msg)
        else:
            await client.send_message(msg.channel, 'The {} command is disabled.'.format(command_name))
