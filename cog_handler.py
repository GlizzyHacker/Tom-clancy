from cogs import ping, ghostping, asked, react, symouse, insult, leseird, nemertem, faszopo, dummy_police, balint_reacting, segg, egyebkent, lol, purge

async def add_all_cogs(bot):
    await bot.add_cog(ping.Ping(bot))

    # command cogs
    await bot.add_cog(ghostping.GhostPing(bot))
    await bot.add_cog(asked.Asked(bot))
    await bot.add_cog(react.React(bot))
    await bot.add_cog(symouse.Symouse(bot))
    await bot.add_cog(insult.Insult(bot))

    # message reaction stuff
    await bot.add_cog(leseird.Leseird(bot))
    await bot.add_cog(nemertem.Nemertem(bot))
    await bot.add_cog(faszopo.Faszopo(bot))
    await bot.add_cog(dummy_police.DummyPolice(bot))
    await bot.add_cog(balint_reacting.BalintReacting(bot))
    await bot.add_cog(segg.Segg(bot))
    await bot.add_cog(egyebkent.Egyebkent(bot))
    await bot.add_cog(lol.Lol(bot))
