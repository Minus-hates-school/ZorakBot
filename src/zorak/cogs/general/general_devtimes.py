"""
Sends the Current local time of the moderation staff.\
"""
import logging
import datetime
import pytz
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class GeneralDevtimes(commands.Cog):
    """
    Sends the Current local time of the moderation staff.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Current times of Staff.")
    async def devtimes(self, ctx):
        """
        Sends the Current local time of the moderation staff.
        TODO: again, dict mapping could be good to help here,
            could also provide a command with timezone as input.
             Could do a whole times cog probably.
        """
        logger.info("%s used the %s command."
                    , ctx.author.name
                    , ctx.command)

        embed = discord.Embed(title="**Staff Times**", description="")
        dev_times_list = self.bot.db_client.get_all_dev_times()

        for iteration, dev_time in enumerate(dev_times_list):
            tz = datetime.datetime.now(tz=pytz.timezone(dev_time['Timezone']))
            embed.add_field(
                name=f"{dev_time['Country']} ({dev_time['Username']}):",
                value=f"{tz.strftime('%m/%d/%Y %I:%M %p')}",
                inline=False,
            )
        await ctx.respond(embed=embed)

    @commands.slash_command(description="Add entry to devtimes. See pytz.timezone documentation for timezone (Staff Only).")
    @commands.has_role("Staff")
    async def add_devtime(self, ctx, username, country, timezone):
        """
        Add entry to devtimes.
        """
        logger.info("%s used the %s command."
                    , ctx.author.name
                    , ctx.command)

        self.bot.db_client.add_dev_time_to_table(username, country, timezone)
        await ctx.respond(f"Added {username} to devtimes.")

    @commands.slash_command(description="Remove entry from devtimes. (Staff Only).")
    @commands.has_role("Staff")
    async def remove_devtime(self, ctx, username):
        """
        Remove entry from devtimes.
        """
        logger.info("%s used the %s command."
                    , ctx.author.name
                    , ctx.command)

        self.bot.db_client.remove_dev_time_from_table(username)
        await ctx.respond(f"Removed {username} from devtimes.")

def setup(bot):
    """Required."""
    bot.add_cog(GeneralDevtimes(bot))
