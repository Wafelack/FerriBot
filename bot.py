import discord
import json
from play import play
import urllib.request
import asyncio

TOKEN = json.load(open("assets/token.json", "r"))['token']

client = discord.Client()
PREFIX = '&'

async def delout(message, user):
    def check(reaction, user):
        return str(reaction.emoji) == "🗑" and reaction.count > 1 and user == user and reaction.message.id == message.id

    reaction, user = await client.wait_for('reaction_add', check=check)
    if check(reaction, user):
        await message.delete()


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(name=f'{PREFIX}run <rust_code>', type=discord.ActivityType.playing))
    print("FerriBot is ready")


RUSTLINKS = json.load(open("assets/rustlinks.json"))['LINKS']

@client.event
async def on_message(message):
    if message.content.startswith(PREFIX + 'book'):
        splited = message.content.split(' ', 1)
        if len(splited) != 2:
            await message.channel.send(f"Usage : {PREFIX}book <concept>")
            return

        if splited[1] in RUSTLINKS.keys():
            embed = discord.Embed(title=splited[1], description=RUSTLINKS[splited[1]], color=0xff8800)
            embed.set_footer(text=f"{PREFIX}book • Wafelack • Rust Book")
            await message.channel.send(embed=embed)
        else:
            concepts = "\n•".join(RUSTLINKS.keys())
            embed = discord.Embed(title=f"Concept `{splited[1]}` not found.", description=f"**Available concepts :**\n\n•{concepts}", color=0xff0000)
            embed.set_footer(text=f"{PREFIX}book • Wafelack • Rust Book")
            await message.channel.send(embed=embed)

    if message.content.startswith(PREFIX + 'get_crate'):
        splited = message.content.split(' ', 2)
        if len(splited) != 2:
            await message.channel.send(f"Usage : {PREFIX}get_crate <crate>")
            return


        embed = discord.Embed(
            title=f'{splited[1]}', description=f'docs.rs : https://docs.rs/{splited[1]}\ncrates.io : https://crates.io/crates/{splited[1]}', color=00)
        await message.channel.send(f"<@{message.author.id}>\n", embed=embed)
    if message.content.startswith(PREFIX + 'playground') or message.content.startswith(PREFIX + 'run'):
        splited = message.content.split('\n')
        stderr, stdout = play(splited)
        if stdout == "":
            msg = await message.channel.send(f"Standard error : ```" + stderr.replace('`', '\'') + "```\n```No standard "
                                                                                             "output !```")
        else:
            msg = await message.channel.send(
                f"Standard error : ```" + stderr.replace('`', '\'') + f"```\nStandard output : ```{stdout}```")

        await msg.add_reaction("🗑")
        client.loop.create_task(delout(msg, message.author))
        return
    if message.content == PREFIX + "btc":
        VALUES = json.loads(urllib.request.urlopen('https://blockchain.info/ticker').read().decode())
        buy_usd = VALUES['USD']['buy']
        sell_usd = VALUES['USD']['sell']

        buy_eur = VALUES['EUR']['buy']
        sell_eur = VALUES['EUR']['sell']

        buy_rub = VALUES['RUB']['buy']
        sell_rub = VALUES['RUB']['sell']

        embed = discord.Embed(title="BTC Value:", description=f"**USD :**\n\tSell : ${sell_usd}\n\tBuy: ${buy_usd}\n\n**EUR :**\n\tSell : {sell_eur}€\n\tBuy : {buy_eur}€\n\n**RUB :**\n\tBuy : {buy_rub} Pуб\n\tSell : {sell_rub} Pуб", color=0xffbb00)
        embed.set_footer(text="Data picked on https://blockchain.info/ticker")

        await message.channel.send(embed=embed)

    if message.content == PREFIX + "help":
        embed = discord.Embed(title="Rustacean",
                              description=f"**{PREFIX}get_crate <crate_name>** : Gives you the link of a crate\n**{PREFIX}playground** or **{PREFIX}run \`\`\`rs\n\t<code>\`\`\`** : Runs the code on the rust playground\n**{PREFIX}btc** : Gives you the bitcoin value in EUR, USD and RUB\n**{PREFIX}book <concept>** : Gives you the rustbook's link of a rust concept")
        embed.set_author(name="Rustacean",
                         icon_url="https://cdn.discordapp.com/attachments/727885557430222849/754727660432785428/rustacean-flat-noshadow.png")
        embed.set_footer(text="!help • Copyleft Wafelack • Rustacean")
        await message.channel.send(embed=embed)


try:
    client.run(TOKEN)
except KeyboardInterrupt:
    exit()

