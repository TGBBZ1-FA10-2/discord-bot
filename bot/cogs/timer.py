import typing
from discord.ext import commands, tasks
import datetime


class Timer(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

        self.timers: typing.List[dict] = []

    @commands.command(name="list_timers", aliases=["timers"])
    async def list_timers(self, ctx: commands.Context) -> None:
        """Lists all active timers."""
        now = datetime.datetime.now()

        msg = "\n".join(["Timer von {user} - {left} verbleibend.".format(
            user=timer["user"].display_name,
            left=timer["end"] - now,
        ) for timer in self.timers])

        await ctx.send(msg)

    @commands.command(name="clear_timers")
    async def clear_timers(self, ctx: commands.Context) -> None:
        """Clears all active timers."""
        self.timers.clear()
        self.check_timer_end.cancel()

        await ctx.send("Alle Timer gelöscht.")

    @commands.command(name="timer")
    async def timer(self, ctx: commands.Context, minutes: int) -> None:
        """Creates a timer for x minutes."""
        # Check if minutes is positive
        if 0 <= minutes <= 300:
            await ctx.send("Zeit muss zwischen 0-300 Minuten sein.")
            return

        # Calculate dates
        minutes_added = datetime.timedelta(minutes=minutes)

        start_time = datetime.datetime.now()
        end_time = start_time + minutes_added

        timer = {
            "user": ctx.author,
            "start": start_time,
            "end": end_time,
            "duration": minutes,
        }

        # Check if there are any timers, if not, start the loop
        if not self.timers:
            self.check_timer_end.start(ctx)

        self.timers.append(timer)

        await ctx.send(f"Dein Timer wurde auf {minutes} Minute(n) gesetzt.")

    @tasks.loop(seconds=5.0)
    async def check_timer_end(self, ctx: commands.Context) -> None:
        for timer in self.timers:
            now = datetime.datetime.now()
            end = timer["end"]
            user = timer["user"]

            if now >= end:
                msg = f"{user.mention} - Dein Timer ist abgelaufen!"
                await ctx.send(msg)

                # Remove timer from list
                self.timers.remove(timer)

                # Check if there are any timers left, if not, cancel task
                if not self.timers:
                    self.check_timer_end.cancel()
