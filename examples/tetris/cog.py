from discord.ext import commands


class Games(commands.Cog):
    @commands.command(name='leaderboard', aliases=['leader'], help='Shows game\'s leaderboard.')
    async def leaderboard(self, ctx: commands.Context):
        nums = self.pad(list(range(1, len(ctx.game.leaderboard[:10]) + 1)))
        names = self.pad(['Names'] + [f'{i}{record[0]}' for i, record in zip(nums, ctx.game.leaderboard[:10])], 2)
        scores = self.pad(['Points'] + [record[1] for record in ctx.game.leaderboard[:10]])

        board = '\n'.join([f'{name}{score}' for name, score in zip(names, scores)])
        await ctx.send(f"**Leaderboard**\n```\n{board}\n```")

    @staticmethod
    def pad(items: iter, minimum: int = 1):
        if not items:
            return items

        items = [str(item).strip() for item in items]
        length = len(max(items, key=len))

        return [item + ' ' * (length - len(item) + minimum) for item in items]


def setup(bot: commands.Bot):
    bot.add_cog(Games())
