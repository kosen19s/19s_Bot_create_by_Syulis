import discord
import json
from collections import defaultdict

import server_mng
import bot_ctrl
import time_module
import casino
import rpg
import special

PASSCORD = 3310
client = discord.Client()

gana = 0
free = 0
chat = 0

user_stat = None
monster_stat = None
item_stat = None
user_id = None
user_id_reaction = None
kosen = None
token = None
emoji = None
vote = None
emoji_user = defaultdict(dict)
vote_content = defaultdict(dict)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    global user_stat
    global monster_stat
    global place_enc
    global weapon_stat
    global item_stat
    global kosen
    global token
    global emoji
    global vote
    us = open('user_stat.json', 'r', encoding='utf-8')
    user_stat = json.load(us)
    us.close()
    ms = open('monster_stat.json', 'r', encoding='utf-8')
    monster_stat = json.load(ms)
    ms.close()
    en = open('enc.json', 'r', encoding='utf-8')
    place_enc = json.load(en)
    ws = open('weapon_stat.json', 'r', encoding='utf-8')
    weapon_stat = json.load(ws)
    ws.close()
    im = open('item_stat.json', 'r', encoding='utf-8')
    item_stat = json.load(im)
    im.close()
    ks = open('kosen19s.json', 'r', encoding='utf-8')
    kosen = json.load(ks)
    ks.close()
    ej = open('emoji.json', 'r')
    emoji = json.load(ej)
    ej.close()
    vo = open('vote.json', 'r')
    vote = json.load(vo)
    vo.close()

@client.event
async def on_message(message):
    text = message.content
    global user_id
    user_id = str(message.author.id)

    if message.channel.id != 603525315515645962:  # 19s用
        return

    if message.author == client.user:
        print("bot message:{0}".format(text))
        return

    print("catch message:{0}".format(text))

    #メンバーデータセット
    await server_mng.set_server(message, user_stat, user_id)
    #メンバー役職セット
    await server_mng.role_server(message, user_stat)
    #個人データリセット
    await server_mng.reset(message, user_stat, user_id)
    #メンバーデータセーブ
    await server_mng.save(message, user_stat)
    #投票データセーブ
    await server_mng.save_vote(message, vote_content)
    #kosen19鯖専用役職セット
    await server_mng.role(message, user_stat, user_id, kosen)
    #役職確認コマンド
    await server_mng.roles(message, user_stat, user_id)
    #readme出力
    await bot_ctrl.help(message)
    #botログアウト
    await bot_ctrl.logout(message, user_stat, PASSCORD, client)
    #役職検索
    await bot_ctrl.search(message)
    #投票機能
    await bot_ctrl.vote(message, user_stat, user_id, emoji, vote_content)
    #会話ログ取得出力
    await bot_ctrl.chat(message, user_stat, user_id, free)
    #ドン
    await bot_ctrl.gana(message, gana)
    #なう
    await time_module.now(message)
    #タイマー機能
    await time_module.timer(message)
    #じゃんけん
    await casino.janken(message, user_stat, user_id)
    #スロッカス
    await casino.slot(message, user_stat, user_id, emoji)
    #G => coin
    await casino.exchange(message, user_stat, user_id)
    #RPG機能 <= 開発中
    await rpg.RPG(message, user_stat, user_id, monster_stat, place_enc, weapon_stat, place_enc)
    #test
    await special.test(message)

@client.event
async def on_reaction_add(reaction, user):
    global user_id_reaction
    user_id_reaction = str(user.id)
    if user_id_reaction == str(client.user.id):
        return
    message = reaction.message
    message_id_reaction = str(message.id)
    if message_id_reaction not in emoji_user[user_id_reaction]:
        emoji_user[user_id_reaction][message_id_reaction] = reaction.emoji
        try:
            vote_content[message_id_reaction]["vote"].append(reaction.emoji)
        except:
            return
        print("bbb")

    else:
        await message.remove_reaction(emoji_user[user_id_reaction][message_id_reaction], user)
        try:
            vote_content[message_id_reaction]["vote"].remove(emoji_user[user_id_reaction][message_id_reaction])
        except:
            return
        emoji_user[user_id_reaction][message_id_reaction] = reaction.emoji
        try:
            vote_content[message_id_reaction]["vote"].append(reaction.emoji)
        except:
            return
        print("ccc")



@client.event
async def on_reaction_remove(reaction, user):
    global user_id_reaction
    user_id_reaction = str(user.id)
    message = reaction.message
    message_id_reaction = str(message.id)
    if emoji_user[user_id_reaction][message_id_reaction] == reaction.emoji:
        try:
            vote_content[message_id_reaction]["vote"].remove(emoji_user[user_id_reaction][message_id_reaction])
        except:
            return
        del emoji_user[user_id_reaction][message_id_reaction]
        print("ddd")

with open('C:/Users/st158/OneDrive/ドキュメント/Python Scripts/Token.json', 'r', encoding='utf-8') as f:
    bot_token = json.load(f)
    client.run(bot_token["Botton"]["token"])