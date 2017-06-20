""" Display some information about a user """

from registrar import AbstractCommand, bot_command
from discord import embeds
from discord.enums import Status
from discord.ext import commands


@bot_command
class Command(AbstractCommand):
    """ Template for bot command classes. """
    _name = 'play'
    _aliases = ['play']
    _enabled = True

    @staticmethod
    async def execute(shards, client, msg):
        """ Executes this command.
        :param shards:
        :type client: discord.Client
        :type msg: discord.Message
        """

        print (msg.content)
        if not discord.opus.is_loaded():
            discord.opus.load_opis('libopus.so')

    @property
    def name(self):
        """ The name of this command """
        return self._name

    @property
    def aliases(self):
        """ The aliases that can be used to call this command """
        return self._aliases

    @property
    def enabled(self):
        """ Controls whether the command is allowed to be executed. """
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        """ Setter for `enabled` """
        self.enabled = value
