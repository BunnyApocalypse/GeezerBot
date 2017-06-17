class Command():
    async def tellmeabout(message, client):
        if message.mentions:
            target = message.mentions[0]
        else:
            target = message.author

            status = target.status

            if status == Status.online:
                status = ':sunny: Online'
            elif status == Status.offline:
                status = ':sleeping_accomodation Offline'
            elif status == Status.idle:
                status = ':zzz: Idle'
            elif target.status == Status.dnd:
                status = ':octagonal_sign: Do Not Disturb'

                nick = target.display_name if target.name != target.display_name else "None"
                created_at = "{:%B %d %Y @ %I:M%p}".format(target.created_at)
                joined_at = "{:%B %d %Y @ %I:M%p}".format(target.joined_at)

                embed = embeds.Embed()
                embed.color = target.color
                embed.set_author(name=f'{target.name}#{target.discriminator}',
                                 icon_url='https://i.imgur.com/s2r7jp7.png')
                embed.set_thumbnail(url=target.avatar_url)
                embed.add_field(name='User ID', value=target.id)
                embed.add_field(name='Status', value=status)
                embed.add_field(name='Nick', value=nick)
                embed.add_field(name='Account Created', value=created_at)
                embed.add_field(name='Join Date', value=joined_at)

                if target.id == '164935798100197376' or target.id == '135261720921767936':
                    embed.add_field(name='Extra', value=':frog: This person is a cuck.')

                    embed.set_footer(text='Requested by {0}'.format(message.author.mention)
                                     , icon_url=message.author.avatar_url)

                    await client.send_message(message.channel, embed=embed)
