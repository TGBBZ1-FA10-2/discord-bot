import datetime
from discord.ext import commands, tasks
import discord
import random
import math

KANZLER_ID = 173659630470299651


class Kanzler(commands.Cog):
    max_mute_time = 181

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

        self._end_time = None

    @commands.command(name="kanzler", aliases=["k"])
    async def mute_kanzler(self, ctx: commands.Context) -> None:
        """Mutes Kanzler!"""
        # Get discord server, kanzlers user object and muted role from ctx
        guild: discord.Guild = ctx.guild
        kanzler = guild.get_member(KANZLER_ID)
        muted_role = discord.utils.get(ctx.guild.roles, name="muted")

        # check if already muted
        if muted_role in kanzler.roles:
            await ctx.send("Kanzler ist bereits stummgeschalten. :sob:")
            return

        # Calculate end time
        muted_time = random.randint(1, self.max_mute_time)
        now = datetime.datetime.now()
        self._end_time = now + datetime.timedelta(seconds=muted_time)

        await kanzler.add_roles(muted_role)

        self.remove_muted_role.start(ctx)

        msg = f"{kanzler.mention} wurde für {muted_time}s stummgeschalten!"
        # Number of party faces depending on the amount of muted time.
        # 10 can only be reached with max mute of 180 seconds (-> math.floor)
        # max time is decreased by one because random.randint does only return
        # 1 ~ max_time -1
        n_faces = math.floor((muted_time/(self.max_mute_time - 1)) * 100) // 10
        msg += " :partying_face:" * n_faces

        await ctx.send(msg)

    @tasks.loop(seconds=2)
    async def remove_muted_role(self, ctx: commands.Context) -> None:
        now = datetime.datetime.now()

        if now >= self._end_time:
            guild: discord.Guild = ctx.guild
            kanzler = guild.get_member(KANZLER_ID)
            muted_role = discord.utils.get(ctx.guild.roles, name="muted")

            await kanzler.remove_roles(muted_role)
            await ctx.send(f"{kanzler.mention} ist wieder frei! :scream:")

            self.remove_muted_role.cancel()
