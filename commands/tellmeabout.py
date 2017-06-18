""" Display some information about a user """

from registrar import AbstractCommand, bot_command
from discord import embeds
from discord.enums import Status


@bot_command
class Command(AbstractCommand):
    """ Template for bot command classes. """
    _name = 'tellmeabout'
    _aliases = ['tellmeabout']
    _enabled = True

    @staticmethod
    async def execute(shards, client, msg):
        """ Executes this command.
        :param shards:
        :type client: discord.Client
        :type msg: discord.Message
        """

        if msg.mentions:
            target = msg.mentions[0]
        else:
            target = msg.author


        shared_guilds = len([i for i in client.get_all_members() if i.id == target.id])

        if target.status == Status.online:
            status = ':sunny: Online'
        elif target.status == Status.offline:
            status = ':sleeping_accommodation: Offline'
        elif target.status == Status.idle:
            status = ':zzz: Idle'
        elif target.status == Status.dnd:
            status = ':octagonal_sign: DnD'

        nick = target.display_name if target.name != target.display_name else "None"
        created_at = "{:%B %d %Y @ %I:%M%p}".format(target.created_at)
        joined_at = "{:%B %d %Y @ %I:%M%p}".format(target.joined_at)

        embed = embeds.Embed()
        embed.color = target.color
        embed.set_author(name=f'{target.name}#{target.discriminator}',
                         icon_url='https://i.imgur.com/s2r7jp7.png')
        embed.set_thumbnail(url=target.avatar_url)
        embed.add_field(name='User ID', value=target.id)
        embed.add_field(name='Status', value=status)
        embed.add_field(name='Nick', value=nick)
        embed.add_field(name='Shared Servers', value=shared_guilds)
        embed.add_field(name='Account Created', value=created_at, inline=False)
        embed.add_field(name='Join Date', value=joined_at, inline=False)
        embed.set_footer(text=f'Requested by {msg.author.display_name}#{msg.author.discriminator}',
                         icon_url=msg.author.avatar_url)

        await client.send_message(msg.channel, embed=embed)

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
