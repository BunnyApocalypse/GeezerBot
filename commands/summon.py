""" Display some information about a user """

from registrar import AbstractCommand, bot_command
import discord
from discord import embeds
from discord.enums import Status
from discord.ext import commands


@bot_command
class Command(AbstractCommand):
    """ Template for bot command classes. """
    _name = 'summon'
    _aliases = ['summon']
    _enabled = True

    @staticmethod
    async def execute(shards, client, msg):
        """ Executes this command.
        :param shards:
        :type client: discord.Client
        :type msg: discord.Message
        """

        if not discord.opus.is_loaded():
            discord.opus.load_opus('libopus.so')
            print ("loading opus")
        print ("opus loaded")

        target = msg.author
        channel = target.voice_channel
        if channel is None:
            await client.send_message(msg.channel, 'You\'re not in a voice channel! Join one you dingus!one1!!' )

        state = client.get_voice_state(msg.server)
        if state.voice is None:
            state.voice = await client.join_voice_channel(channel)

        else:
            await state.voice.move_to(channel)

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
