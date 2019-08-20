import discord
from datetime import datetime
from statistics import mode
import json
import re
import sys
import json
import time
import logging
import os
import asyncio
import threading
import random
from pytube import YouTube
from discord.ext import commands
from discord.voice_client import VoiceClient
from copy import deepcopy

client = discord.Client()

jan = 0
anc = []
ques = []
A = 0
done = 0
gana = 0
free = 0
vote = 0
chat = 0
rpg = 0
off = 0
data = 0
main = " **メニュー**\n```1.アイテム　　　2.ステータス\n3.装備　　　　　" \
                        "4.フィールド移動\n5.エンカウント　6.RPGモード終了```"
vt = 0
mp_pass = 0
mp_pass_user = 0
magic_flag = 0
magic_flag_user = 0
down_mp = 0
down_mp_user = 0
user_turn = 0
monster_turn = 0
turn_system = 0
escape_trigger = 0
item_trigger = 0
select = 0
anc_result = []
place = None
place_trigger = 0
result = None
all_result = []
way_user = None
way_user_name = None
way_monster_name = None
vtr = None
user_stat = None
monster_stat = None
user_id = None
monster_name = None
kosen = None
token = None
<<<<<<< Updated upstream

dm_user_ac = 0
dm_mons_ac = 0

ch_user_hp = 0
ch_monster_hp = 0

ch_user_mp = 0
ch_monster_mp = 0

ch_user_str = 0
ch_monster_str = 0

ch_user_def = 0
ch_monster_def = 0

ch_user_msr = 0
ch_monster_msr = 0

ch_user_mdf = 0
ch_monster_mdf = 0

ch_user_spd = 0
ch_monster_spd = 0

up_hp_user = 0
up_mp_user = 0
up_str_user = 0
up_def_user = 0
up_msr_user = 0
up_mdf_user = 0
up_spd_user = 0

re_hp = 0
vol_hp = 0
re_mp = 0
vol_mp = 0
=======
emoji = None
vote = None
emoji_user = defaultdict(dict)
vote_content = defaultdict(dict)
>>>>>>> Stashed changes

PASSCORD = "3310"

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    global user_stat
    global monster_stat
    global enc_pass
    global place_enc
    global weapon_stat
    global kosen
    global token
<<<<<<< Updated upstream
    us = open('user_stat.json', 'r',  encoding='utf-8')
=======
    global emoji
    global vote
    us = open('user_stat.json', 'r', encoding='utf-8')
>>>>>>> Stashed changes
    user_stat = json.load(us)
    ms = open('monster_stat.json', 'r', encoding='utf-8')
    monster_stat = json.load(ms)
    en = open('enc.json', 'r', encoding='utf-8')
    place_enc = json.load(en)
    ws = open('weapon_stat.json', 'r', encoding='utf-8')
    weapon_stat = json.load(ws)
    ks = open('kosen19s.json', 'r', encoding='utf-8')
    kosen = json.load(ks)
    # tk = open('token.txt', 'r')
    # token = json.load(tk)
    us.close()
    ms.close()
    en.close()
    ws.close()
    ks.close()
<<<<<<< Updated upstream
=======
    ej = open('emoji.json', 'r')
    emoji = json.load(ej)
    ej.close()
    vo = open('vote.json', 'r')
    vote = json.load(vo)
    vo.close()
>>>>>>> Stashed changes

def file_len(fname):
    with open(fname) as f:

        for i, l in enumerate(f):
            pass

    return i + 1

def lenlen(text):
    for i, l in enumerate(text):
            pass

    return i + 1

def find_text_start_from(keyword,text):
    search = keyword + ".+"
    result = re.search(search,text)

    if result == None:
       return None

    else:
       return result.group(0).replace(keyword,"").strip()

def normal_attack_mons():
    global ch_monster_str
    global ch_monster_def
    global way_monster_name
    dm_for_mons = ch_monster_str + random.randint(-1,1) - user_stat[user_id]["rpg"]["ch_user_def"]
    way_monster_name = "攻撃"
    return dm_for_mons

def mera_mons():
    global ch_monster_msr
    global ch_monster_mdf
    global ch_monster_mp
    global way_monster_name
    global magic_flag
    dm_for_mons = ch_monster_msr * 2 - user_stat[user_id]["rpg"]["ch_user_mdf"]
    way_monster_name = "メラ"
    ch_monster_mp = ch_monster_mp - 3
    magic_flag = 1
    return dm_for_mons

def attack_monster(monster_stat,monster_name):
    global way
    way = random.choice(monster_stat[monster_name]["way"])
    dm_user_ac = eval(way)()
    return dm_user_ac

def normal_attack_user(user_stat,user_id,weapon_stat):
    global ch_user_str
    global ch_monster_def
    global way_user_name
    dm_mons_ac = user_stat[user_id]["rpg"]["ch_user_str"] \
                 + random.randint(weapon_stat[user_stat[user_id]["rpg"]["weapon"]]["mura"][0],
                                  weapon_stat[user_stat[user_id]["rpg"]["weapon"]]["mura"][1]) - ch_monster_def
    way_user_name = "攻撃"
    return dm_mons_ac

def mera(user_stat,user_id):
    global ch_monster_mdf
    global way_user_name
    dm_mons_ac = user_stat[user_id]["rpg"]["ch_user_msr"] * 2 - ch_monster_mdf
    user_stat[user_id]["rpg"]["ch_user_mp"] = user_stat[user_id]["rpg"]["ch_user_mp"] - 3
    way_user_name = "メラ"
    return dm_mons_ac

def attack_user(user_stat, user_id, weapon_stat, way_user):
    dm_monster_ac = eval(way_user)(user_stat,user_id,weapon_stat)
    return dm_monster_ac

def Medicinal_herbs(user_stat, user_id):
    global re_hp
    re_hp = 1
    global vol_hp
    vol_hp = 10
    user_stat[user_id]["rpg"]["ch_user_hp"] = user_stat[user_id]["rpg"]["ch_user_hp"] + 10

    if user_stat[user_id]["rpg"]["ch_user_hp"] > user_stat[user_id]["rpg"]["HP"]:
        user_stat[user_id]["rpg"]["ch_user_hp"] = user_stat[user_id]["rpg"]["HP"]

    way_user_name = "薬草"
    return way_user_name

def use_item(user_stat, user_id, a):
    way_user_name = eval(user_stat[user_id]["rpg"]["item_list"][a])(user_stat, user_id)
    return way_user_name

def result_win(user_stat,user_id,monster_stat,monster_name):
    global up_hp_user
    global up_mp_user
    global up_str_user
    global up_def_user
    global up_msr_user
    global up_mdf_user
    global up_spd_user
    user_stat[user_id]["rpg"]["G"] = user_stat[user_id]["rpg"]["G"] + monster_stat[monster_name]["drop"]["G"]
    user_stat[user_id]["rpg"]["EXP"] = user_stat[user_id]["rpg"]["EXP"] + monster_stat[monster_name]["drop"]["EXP"]

    if user_stat[user_id]["rpg"]["EXP"] > user_stat[user_id]["rpg"]["Lv"] * user_stat[user_id]["rpg"]["Lv"] * user_stat[user_id]["rpg"]["Lv"]:
        up_hp_user = random.randint(user_stat[user_stat[user_id]["rpg"]["job"]]["up_hp"][0],
                                    user_stat[user_stat[user_id]["rpg"]["job"]]["up_hp"][1])
        up_mp_user = random.randint(user_stat[user_stat[user_id]["rpg"]["job"]]["up_mp"][0],
                                    user_stat[user_stat[user_id]["rpg"]["job"]]["up_mp"][1])
        up_str_user = random.randint(user_stat[user_stat[user_id]["rpg"]["job"]]["up_str"][0],
                                     user_stat[user_stat[user_id]["rpg"]["job"]]["up_str"][1])
        up_def_user = random.randint(user_stat[user_stat[user_id]["rpg"]["job"]]["up_def"][0],
                                     user_stat[user_stat[user_id]["rpg"]["job"]]["up_def"][1])
        up_msr_user = random.randint(user_stat[user_stat[user_id]["rpg"]["job"]]["up_msr"][0],
                                     user_stat[user_stat[user_id]["rpg"]["job"]]["up_msr"][1])
        up_mdf_user = random.randint(user_stat[user_stat[user_id]["rpg"]["job"]]["up_mdf"][0],
                                     user_stat[user_stat[user_id]["rpg"]["job"]]["up_mdf"][1])
        up_spd_user = random.randint(user_stat[user_stat[user_id]["rpg"]["job"]]["up_spd"][0],
                                     user_stat[user_stat[user_id]["rpg"]["job"]]["up_spd"][1])
        user_stat[user_id]["rpg"]["Lv"] = user_stat[user_id]["rpg"]["Lv"] + 1
        user_stat[user_id]["rpg"]["HP"] = user_stat[user_id]["rpg"]["HP"] + up_hp_user
        user_stat[user_id]["rpg"]["MP"] = user_stat[user_id]["rpg"]["MP"] + up_mp_user
        user_stat[user_id]["rpg"]["STR"] = user_stat[user_id]["rpg"]["STR"] + up_str_user
        user_stat[user_id]["rpg"]["DEF"] = user_stat[user_id]["rpg"]["DEF"] + up_def_user
        user_stat[user_id]["rpg"]["MSR"] = user_stat[user_id]["rpg"]["MSR"] + up_msr_user
        user_stat[user_id]["rpg"]["MDF"] = user_stat[user_id]["rpg"]["MDF"] + up_mdf_user
        user_stat[user_id]["rpg"]["SPD"] = user_stat[user_id]["rpg"]["SPD"] + up_spd_user
        user_stat[user_id]["rpg"]["ch_user_hp"] = user_stat[user_id]["rpg"]["HP"]
        user_stat[user_id]["rpg"]["ch_user_mp"] = user_stat[user_id]["rpg"]["MP"]
        user_stat[user_id]["rpg"]["ch_user_str"] = user_stat[user_id]["rpg"]["STR"]
        user_stat[user_id]["rpg"]["ch_user_def"] = user_stat[user_id]["rpg"]["DEF"]
        user_stat[user_id]["rpg"]["ch_user_msr"] = user_stat[user_id]["rpg"]["MSR"]
        user_stat[user_id]["rpg"]["ch_user_mdf"] = user_stat[user_id]["rpg"]["MDF"]
        user_stat[user_id]["rpg"]["ch_user_spd"] = user_stat[user_id]["rpg"]["SPD"]
        global Lv_up
        Lv_up = 1
        return Lv_up

class question:

    def set_question(self, text):
        anc = []
        a = text.count("$:")
        A = 1
        Q = find_text_start_from("Q:", text)

        for i in range(a):
            anc.append(str(A) + ":" + find_text_start_from(str(A) + ":", text))
            A = A + 1

        hour = find_text_start_from("h:", text)
        HOUR = int(hour)
        mint = find_text_start_from("m:", text)
        MINT = int(mint)
        return Q, HOUR, MINT

@client.event
async def on_message(message):

    if client.user != message.author:
        text = message.content
        global free
        global gana
        global rpg
        global data
        global result
        global user_id
        user_id = str(message.author.id)
<<<<<<< Updated upstream
=======
        #初期データ
        starter = {
            "official": {
                "\u4e00\u822c\u5f79\u8077": []
            },
            "rpg": {
                "rpg_trigger": {
                    "main": 0,
                    "vt": 0,
                    "mp_pass": 0,
                    "mp_pass_user": 0,
                    "magic_flag": 0,
                    "magic_flag_user": 0,
                    "down_mp": 0,
                    "down_mp_user": 0,
                    "user_turn": 0,
                    "monster_turn": 0,
                    "turn_system": 0,
                    "escape_trigger": 0,
                    "item_trigger": 0,
                    "place_trigger": 0,
                    "re_hp": 0,
                    "re_mp": 0,
                    "Lv_up": 0,
                    "distance_trigger": 0
                 },
                 "job": "NEET",
                 "job_lv": 1,
                 "Lv": 1,
                 "HP": 5,
                 "ch_user_hp": 5,
                 "MP": 3,
                 "ch_user_mp": 3,
                 "STR": 2,
                 "ch_user_str": 2,
                 "DEF": 1,
                 "ch_user_def": 1,
                 "MSR": 1,
                 "ch_user_msr": 1,
                 "MDF": 1,
                 "ch_user_mdf": 1,
                 "SPD": 3,
                 "ch_user_spd": 3,
                 "item": {
                    "Medicinal_herbs": 1
                 },
                 "have weapon": [
                    "\u7d20\u624b"
                 ],
                 "weapon": "\u7d20\u624b",
                 "magic_way": [],
                 "skill_way": [],
                 "EXP": 0,
                 "G": 0,
                 "place": "家",
                 "vtr": 0,
                 "ch_monster_hp": 0,
                 "ch_monster_mp": 0,
                 "ch_monster_str": 0,
                 "ch_monster_def": 0,
                 "ch_monster_msr": 0,
                 "ch_monster_mdf": 0,
                 "ch_monster_spd": 0,
                 "vol_hp": 0,
                 "vol_mp": 0,
                 "dm_user_ac": 0,
                 "dm_mons_ac": 0,
                 "up_hp_user": 0,
                 "up_mp_user": 0,
                 "up_str_user": 0,
                 "up_def_user": 0,
                 "up_msr_user": 0,
                 "up_mdf_user": 0,
                 "up_spd_user": 0,
                 "way_user": 0,
                 "way_user_name": 0,
                 "way_monster_name": 0,
                 "monster_name": 0,
                "distance": 0
              },
              "trigger": {
                  "ques": 0,
                  "exchange": 0,
                 "janken": 0,
                 "data": 1,
                 "rpg": 0,
                 "\u5f79\u8077\u6c7a\u3081": 0
              },
              "casino": {
                 "coin": 5,
                 "cost": 0
              },
              "janken": {
                 "result": 0,
                 "result_count": [
                    0,
                    0
                 ],
                 "bot_pon_number": 0
              },
            "question": {
                "content": []
            }
        }
>>>>>>> Stashed changes

        #データの有無
        try:
            if not user_stat[user_id]["trigger"]["data"] == 0:
                pass

        except:
            user_stat[user_id] = user_stat["Starter"].copy()

        finally:
            #初期設定
            if text == "/set.server":

                if message.author.guild_permissions.administrator:

                    for M in message.guild.members:
                        print(str(M) + "\n" + str(M.id))
                        user_stat[str(M.id)] = user_stat["Starter"].copy()

                    with open('user_stat.json', "w") as f:
                        json.dump(user_stat, f, indent=3)

                    await message.channel.send("(ﾟ∀ﾟ)ｱﾋｬﾋｬﾋｬﾋｬﾋｬﾋｬ")
                    return

                else:
                    await message.channel.send("サーバーの管理者が操作してください。")

        #要改良
        if text == "/save.vote":
            with open('vote.json', "w") as w:
                json.dump(vote_content, w, indent=3)
            await message.channel.send("投票のセーブが完了しました。")

        #ユーザーデータセーブ
        if text == "/save":
            with open('user_stat.json', "w") as f:
                json.dump(user_stat, f, indent=3)
            await message.channel.send("セーブが完了しました。")

<<<<<<< Updated upstream
        if re.search("じゃんけん", text) and rpg == 0 and free == 0:
            global jan
            global bot_pon_number
=======
        #じゃんけん
        if re.search("じゃんけん", text) and user_stat[user_id]["trigger"]["rpg"] == 0:
            await message.channel.send("あなたのcoin:{0}\n掛け金を入力してください。\n(掛け金は5以下)"
                                       .format(user_stat[user_id]["casino"]["coin"]))
            user_stat[user_id]["trigger"]["janken"] = 1
            return

        if user_stat[user_id]["trigger"]["janken"] == 1:

            if text == "/cancel":
                await message.channel.send("キャンセルしました。")
                user_stat[user_id]["trigger"]["janken"] = 0
                return

            cost = int(text)
            user_stat[user_id]["casino"]["cost"] = cost
            if cost > user_stat[user_id]["casino"]["coin"] or cost > 5:
                await message.channel.send("掛け金が大きすぎます。")
                return

            elif cost == 0:
                await message.channel.send("掛け金を0にはできません。")
                return

            user_stat[user_id]["trigger"]["janken"] = 2
            pass
>>>>>>> Stashed changes

            if jan == 0:
                await message.channel.send("じゃーんけーん\n```ぐー\nちょき\nぱー```")
                jan = 1

        if jan == 1:
            win_bot = "勝ち申した。"
            win_user = "負け申した。"
            soso = "あーいこーで\n```ぐー\nちょき\nぱー```"
            bot_pon = random.choice(["ぐー", "ちょき", "ぱー"])

            if bot_pon == "ぐー":
                bot_pon_number = 0

            elif bot_pon == "ちょき":
                bot_pon_number = 1

            elif bot_pon == "ぱー":
                bot_pon_number = 2

            if text == "ぐー":
                await message.channel.send(bot_pon)

                if bot_pon_number == 0:
                    await message.channel.send(soso)
                    return

                elif bot_pon_number == 1:
                    await message.channel.send(win_user)
                    jan = 2
                    result = "win"

                elif bot_pon_number == 2:
                    await message.channel.send(win_bot)
                    jan = 2
                    result = "lose"

            elif text == "ちょき":
                await message.channel.send(bot_pon)

                if bot_pon_number == 0:
                    await message.channel.send(win_bot)
                    jan = 2
                    result = "lose"

                elif bot_pon_number == 1:
                    await message.channel.send(soso)
                    return

                elif bot_pon_number == 2:
                    await message.channel.send(win_user)
                    jan = 2
                    result = "win"

            elif text == "ぱー":
                await message.channel.send(bot_pon)

                if bot_pon_number == 0:
                    await message.channel.send(win_user)
                    jan = 2
                    result = "win"

                elif bot_pon_number == 1:
                    await message.channel.send(win_bot)
                    jan = 2
                    result = "lose"

                elif bot_pon_number == 2:
                    await message.channel.send(soso)
                    return

        if jan == 2:

            if result == "win":
                user_stat[user_id]["others"]["result"][0] = user_stat[user_id]["others"]["result"][0] + 1

            elif result == "lose":
                user_stat[user_id]["others"]["result"][1] = user_stat[user_id]["others"]["result"][1] + 1

            await message.channel.send("あなた：{0}勝 {1}敗中\n連戦？\n```する\nしない```"
                                       .format(user_stat[user_id]["others"]["result"][0], user_stat[user_id]["others"]["result"][1]))
            jan = 3

        if jan == 3:

            if text == "する":
                jan = 1
                await message.channel.send("じゃーんけーん\n```ぐー\nちょき\nぱー```")
                return

            elif text == "しない":
                jan = 0
                await message.channel.send("またね！")
                return

        #製作者
        if message.author.id == 432897451209261057:
            global PASSCORD
            global off

            if text == "/role.server":

                if message.author.guild_permissions.administrator:

                    for M in message.guild.members:
                        user_stat[str(M.id)]["official"]["一般役職"].clear()
                        for i in M.roles:
                            print(i)
                            user_stat[str(M.id)]["official"]["一般役職"].append(i)
                            if "@everyone" in user_stat[str(M.id)]["official"]["一般役職"]:
                                user_stat[str(M.id)]["official"]["一般役職"].remove("@everyone")
                            if "bot" in user_stat[str(M.id)]["official"]["一般役職"]:
                                user_stat[str(M.id)]["official"]["一般役職"].remove("bot")
                            if "開発" in user_stat[str(M.id)]["official"]["一般役職"]:
                                user_stat[str(M.id)]["official"]["一般役職"].remove("開発")
                            if "つよつよ" in user_stat[str(M.id)]["official"]["一般役職"]:
                                user_stat[str(M.id)]["official"]["一般役職"].remove("つよつよ")

                    with open('user_stat.json', "w") as f:
                        json.dump(user_stat, f, indent=3)

                    await message.channel.send("(ﾟ∀ﾟ)ｱﾋｬ")

            if text == "/logout@home":
                await message.channel.send("\パスコードを入力してください。")
                Passcord = input("Please Enter Passcord:")

                if Passcord == PASSCORD:
                    with open('user_stat.json', "w") as f:
                        json.dump(user_stat, f, indent=3)
                    await message.channel.send("I'll be back.")
                    await client.logout()
                    await sys.exit()

                else:
                    await message.channel.send("パスコードが違うぞ？。\n私は永久に不滅だ。\nフハハハハハ。")
                    return

            elif text == "/logout@outside":
                await message.channel.send("パスコードを入力してください。")
                off = 1
                return

            if off == 1:

                if str(text) == PASSCORD:
                    with open('user_stat.json', "w") as f:
                        json.dump(user_stat, f, indent=3)
                    await message.channel.send("パスコード変更を推奨します。\nI'll be back.")
                    await client.logout()
                    await sys.exit()

                else:
                    await message.channel.send("パスコードが違うぞ？。\n私は永久に不滅だ。\nフハハハハハ。")
                    off = 0
                    return

        #役職表示
        if text == "/roles":
            d = []
            for i in message.author.roles:
                if not i.name == "@everyone":
                    d.append(i.name)

                else:
                    pass

            d = map(str, d)
            d = "\n".join(d)
            await message.channel.send(d)

<<<<<<< Updated upstream
        try:
            if text == "/role" and user_stat[user_id]["trigger"]["役職決め"] == 0:
=======
        #kosen19s専用役職設定
        if text == "/role":
            user_stat[user_id]["trigger"]["役職決め"] = 0
            try:
>>>>>>> Stashed changes
                for i in user_stat[user_id]["official"]["一般役職"]:
                    d = discord.utils.get(message.guild.roles, name=i)
                    await message.author.remove_roles(d)

                user_stat[user_id]["official"]["一般役職"] = []
                await message.channel.send("番号を入力してね！")
                a = 1
                d = []
                for chiho in kosen["場所役職"]["地方"]:
                    d.append("{0}.{1}".format(a, chiho))
                    a = a + 1

                d = map(str, d)
                d = "\n".join(d)
                await message.channel.send(d)
                user_stat[user_id]["trigger"]["役職決め"] = user_stat[user_id]["trigger"]["役職決め"] + 1
                return

            if user_stat[user_id]["trigger"]["役職決め"] == 1:
                a = int(text) - 1
                aa = kosen["場所役職"]["地方"][a]
                print(aa)
                user_stat[user_id]["official"]["一般役職"].append(aa)
                await message.channel.send("番号を入力してね！")
                a = 1
                d = []
                for chiho in kosen["場所役職"][aa]:
                    d.append("{0}.{1}".format(a, chiho))
                    a = a + 1

                d = map(str, d)
                d = "\n".join(d)
                await message.channel.send(d)
                user_stat[user_id]["trigger"]["役職決め"] = user_stat[user_id]["trigger"]["役職決め"] + 1
                return

            if user_stat[user_id]["trigger"]["役職決め"] == 2:
                a = int(text) - 1
                aa = kosen["場所役職"][user_stat[user_id]["official"]["一般役職"][0]][a]
                print(aa)
                user_stat[user_id]["official"]["一般役職"].append(aa)
                await message.channel.send("場所登録が完了したよ！\n次は学科登録だよ！")
                user_stat[user_id]["trigger"]["役職決め"] = user_stat[user_id]["trigger"]["役職決め"] + 1
                a = 1
                d = []
                for gakka in kosen["その他役職"]["学科"]:
                    d.append("{0}.{1}".format(a, gakka))
                    a = a + 1

                d = map(str, d)
                d = "\n".join(d)
                await message.channel.send(d)
                return

            if user_stat[user_id]["trigger"]["役職決め"] == 3:
                a = int(text) - 1
                aa = kosen["その他役職"]["学科"][a]
                print(aa)
                user_stat[user_id]["official"]["一般役職"].append(aa)
                await message.channel.send("次は学科登録が完了したよ！\n次は性別だね！")
                user_stat[user_id]["trigger"]["役職決め"] = user_stat[user_id]["trigger"]["役職決め"] + 1
                a = 1
                d = []
                for seibetu in kosen["その他役職"]["性別"]:
                    d.append("{0}.{1}".format(a, seibetu))
                    a = a + 1

                d = map(str, d)
                d = "\n".join(d)
                await message.channel.send(d)
                return

            if user_stat[user_id]["trigger"]["役職決め"] == 4:
                a = int(text) - 1
                aa = kosen["その他役職"]["性別"][a]
                print(aa)
                user_stat[user_id]["official"]["一般役職"].append(aa)
                if kosen["その他役職"]["性別"][a] == "設定しない":
                    await message.channel.send("性別は登録しなかったよ！")
                    pass

                else:
                    await message.channel.send("性別登録が完了したよ")
                    pass

                user_stat[user_id]["trigger"]["役職決め"] = user_stat[user_id]["trigger"]["役職決め"] + 1
                await message.channel.send("最後に部活だね！\nロボコン\n"
                                           "プロコン\nと打ち込むとそれに応じた役職が付けられるよ！\n"
                                           "どちらも付けない場合や満足したら\n/finishで役職登録を終えてね！")
                return

            if user_stat[user_id]["trigger"]["役職決め"] == 5:

                try:

                    if text == "ロボコン":
                        if "robocon" in user_stat[user_id]["official"]["一般役職"]:
                            await message.channel.send("既にその役職は付いているよ！")
                            return

                        await message.channel.send("ロボコンを追加したよ！")
                        user_stat[user_id]["official"]["一般役職"].append("robocon")
                        return

                    if text == "プロコン":
                        if "procon" in user_stat[user_id]["official"]["一般役職"]:
                            await message.channel.send("既にその役職は付いているよ！")
                            return

                        await message.channel.send("プロコンを追加したよ！")
                        user_stat[user_id]["official"]["一般役職"].append("procon")
                        return

                except:
                    await message.channel.send("既にその役職は付いているよ！")
                    return

                if text == "/finish":
                    for i in user_stat[user_id]["official"]["一般役職"]:
                        d = discord.utils.get(message.guild.roles, name=i)
                        await message.author.add_roles(d)

                    await message.channel.send("お疲れ様でした！\nこれで役職設定は終了です！")
                    user_stat[user_id]["trigger"]["役職決め"] = 0
                    return

        except:
            if text == "/cancel":
                await message.channel.send("役職追加をもう一度最初からお願いします！")
                user_stat[user_id]["trigger"]["役職決め"] = 0
                return

            else:
                await message.channel.send("正しい値を入力してください。")
                return

        if text.startswith("/"):

            if text == "/reset" and rpg == 0:

                if user_stat[user_id]["official"]["一般役職"] == 0:
                    pass

                else:
                    for i in user_stat[user_id]["official"]["一般役職"]:
                        d = discord.utils.get(message.guild.roles, name=i)
                        await message.author.remove_roles(d)

                print(user_stat["Starter"])
                user_stat[user_id] = user_stat["Starter"].copy
                with open('user_stat.json', "w") as f:
                    json.dump(user_stat, f, indent=3)
                await message.channel.send("データを初期化しました。")
                data = 1
                return

<<<<<<< Updated upstream
            global vote
            if text.startswith("/ques") and vote == 0:
                vote = 1
                global select
                global anc_result
                global anc
                global A
                anc = []

                try:
                    a = len(anc)
                    A = 1
                    Q = find_text_start_from("Q:", text)
=======
        #ヘルプ
        if text == "/help":
            with open('readme.txt', 'r') as a:
                d = a.read()
                await message.channel.send("```{0}```".format(d))

        #個人データリセット
        if text == "/reset" and user_stat[user_id]["trigger"]["rpg"] == 0:
>>>>>>> Stashed changes

                    for i in range(a):
                        anc.append(str(A) + ":" + find_text_start_from(str(A) + ":", text))
                        A = A + 1

                    hour = find_text_start_from("h:", text)
                    HOUR = int(hour)

                    mint = find_text_start_from("m:", text)
                    MINT = int(mint)
                    await message.channel.send(Q)

                    for name in anc:
                        await message.channel.send(name)

<<<<<<< Updated upstream
                    if HOUR >= 1 and 0 <= MINT <= 59:
                        await message.channel.send("投票期間は{0}時間{1}分です。".format(hour, mint))
=======
        #RPGコイン→カジノコインの変換
        if text == "/exchange":
            await message.channel.send("G:{0}\n10G→1coinです。\nいくら交換しますか？(coin数)"
                                       .format(user_stat[user_id]["rpg"]["G"]))
            user_stat[user_id]["trigger"]["exchange"] = 1
            return
>>>>>>> Stashed changes

                    elif HOUR == 0 and 1 <= MINT <= 59:
                        await message.channel.send("投票期間は{0}分です。".format(mint))

                    wait_vote = HOUR * 3600 + MINT * 60
                    anc_result = []
                    select = 1
                    await asyncio.sleep(wait_vote)

                except:
                    await message.channel.send("正しい値を入力してください。")
                    select = 0
                    return

                try:
                    if vote == 1:
                        await message.channel.send("**投票が終了しました。**\n一番投票が多かったのは\n**{0}**\nでした。"
                                               .format(anc[mode(anc_result) - 1]))
                        anc = []
                        anc_result = []
                        vote = []
                        select = 0
                        return

<<<<<<< Updated upstream
                    else:
                        return

                except:
                    await message.channel.send("この投票では一番は決まりませんでした。\n結果{0}".format(anc_result))
                    select = 0
                    anc = []
                    anc_result = []
                    vote = []
                    return

            if select == 1:
                global ques
                try:
                    if text.startswith("/vote"):
                        result = int(find_text_start_from("/vote", text))

                        if user_id in ques:
                            await message.channel.send("投票済みです。")
                            return

                        else:
                            if 0 < result <= A:
                                ques.append(user_id)
                                anc_result.append(result)
                                await message.channel.send("{0}さんの投票が完了しました。".format(message.author))
                                print(anc_result)
                                return

                except:
                    await message.channel.send("正しい値を入力してください。")
                    return

                if text == "/cancel" and vote == 1:
                    vote = 0
                    select = 0
                    anc = []
                    anc_result = []
                    vote = []
                    await message.channel.send("投票を中止しました。")

            if text == "/now":

                if rpg == 1:
                    await message.channel.send("[RPGモード中です]")

                hour = datetime.now().strftime("%H")
                minute = datetime.now().strftime("%M")
                H = int(hour)
=======
        #投票設定キャンセル
        if text == "/cancel" and user_stat[user_id]["trigger"]["ques"] > 0:
            user_stat[user_id]["trigger"]["ques"] = 0
            await message.channel.send("投票設定を中止しました。")
            return

        #投票
        if text.startswith("/vote") and user_stat[user_id]["trigger"]["ques"] == 0:
            user_stat[user_id]["question"]["content"] = []
            user_stat[user_id]["trigger"]["ques"] = user_stat[user_id]["trigger"]["ques"] + 1
            await message.channel.send("投票のタイトルを入力してください。")
            return

        if user_stat[user_id]["trigger"]["ques"] == 1:
            user_stat[user_id]["trigger"]["ques"] = user_stat[user_id]["trigger"]["ques"] + 1
            user_stat[user_id]["question"]["content"].append(text)
            await message.channel.send("投票候補を入力してください。\n入力を終えたら/next。")
            return

        if user_stat[user_id]["trigger"]["ques"] == 2:
            if text == "/next":
                if len(user_stat[user_id]["question"]["content"]) == 1:
                    await message.channel.send("少なくとも一つは投票候補を入力してください。")
                    return
                user_stat[user_id]["trigger"]["ques"] = user_stat[user_id]["trigger"]["ques"] + 1
                await message.channel.send("何時間？(半角英数)")
                return
            user_stat[user_id]["question"]["content"]\
                .append(text + emoji["emoji"][len(user_stat[user_id]["question"]["content"]) - 1])
            await message.channel.send("今の投票候補数：{0}"
                                       .format(len(user_stat[user_id]["question"]["content"]) - 1))
            return

        if user_stat[user_id]["trigger"]["ques"] == 3:
            if text.isdecimal() == 1:
                user_stat[user_id]["trigger"]["ques"] = user_stat[user_id]["trigger"]["ques"] + 1
                user_stat[user_id]["question"]["content"].append(text)
                await message.channel.send("何分？")
                return
            else:
                await message.channel.send("((半角英数字で))")
                return

        if user_stat[user_id]["trigger"]["ques"] == 4:
            if text.isdecimal() == 1:
                user_stat[user_id]["trigger"]["ques"] = 0
                d = []
                e = []
                user_stat[user_id]["trigger"]["ques"] = 0
                user_stat[user_id]["question"]["content"].append(text)
                d.append(user_stat[user_id]["question"]["content"][0])
                a = 1
                for i in user_stat[user_id]["question"]["content"][1:len(user_stat[user_id]["question"]["content"]) - 2]:
                    d.append("{0}.{1}".format(a, i))
                    a = a + 1
                for i in user_stat[user_id]["question"]["content"][len(user_stat[user_id]["question"]["content"]) - 2:
                                                                   len(user_stat[user_id]["question"]["content"])]:
                    e.append(i)
                H = int(e[0])
                M = int(e[1])
                T = H * 3600 + M * 60
                d.append("投票期間は{0}時間{1}分です。".format(H, M))
                map(str, d)
                dd = "\n".join(d)
                msg = await message.channel.send(dd)
                await msg.pin()
                vote_content[str(msg.id)]["vote"] = []
                a = 0
                for i in range(len(user_stat[user_id]["question"]["content"]) - 3):
                    await msg.add_reaction(emoji["emoji"][a])
                    a = a + 1
                await asyncio.sleep(T)
                try:
                    result = [i for i in d if i.endswith(max(vote_content[str(msg.id)]["vote"]))]   #要改良
                    await message.channel.send\
                        ("{0}という投票で\n一番得票が多かったのは\n**{1}**でした！\n総投票数：{2}"
                         .format(d[0], result[0], len(vote_content[str(msg.id)]["vote"])))

                except:
                    await message.channel.send("この投票では一番は決まりませんでした。\n総投票数：{0}"
                                               .format(len(vote_content[str(msg.id)]["vote"])))

                finally:
                    await msg.unpin()
                    return

            else:
                await message.channel.send("((半角英数字で))")
                return

        #時間
        if text == "/now":
            hour = datetime.now().strftime("%H")
            minute = datetime.now().strftime("%M")
            H = int(hour)
>>>>>>> Stashed changes

                if client.user != message.author:

                    if 3 <= H < 11:
                        x = "おはようございます\n"

                    elif 11 <= H < 18:
                        x = "こんにちは\n"

                    else:
                        x = "こんばんは\n"

                    await message.channel.send("{0}{1}:{2}です".format(x, hour, minute))
                    return

<<<<<<< Updated upstream
            if text.startswith("/timer"):
=======
        #タイマー
        if text.startswith("/timer"):
>>>>>>> Stashed changes

                try:

                    if rpg == 1:
                        await message.channel.send("[RPGモード中です]")

                    global wait
                    global done
                    mint = find_text_start_from("m:", text)
                    sec = find_text_start_from("s:", text)
                    MINT = int(mint)
                    SEC = int(sec)

                    if MINT >= 1 and 0 <= SEC <= 59:
                        await message.channel.send("{0}分{1}秒のタイマーを開始しました。".format(mint, sec))

                    elif MINT == 0 and 1 <= SEC <= 59:
                        await message.channel.send("{0}秒のタイマーを開始しました。".format(sec))

                    wait = 60 * MINT + SEC
                    await asyncio.sleep(wait)

                    if done == 0:

                        if rpg == 1:
                            await message.channel.send("[RPGモード中です]")

                        if MINT == 0 and 0 <= SEC <= 59:
                            await message.channel.send(
                                "{0}{1}秒経ちました！".format(f'{message.author.mention}\n', sec))
                            return

                        else:
                            await message.channel.send(
                                "{0}{1}分{2}秒経ちました！".format(f'{message.author.mention}\n', mint, sec))
                            return

                    else:
                        return

                except:
                    await message.channel.send("正しい数値を入力してください。")
                    return

            if text == "/stop":
                done = 1
                await message.channel.send("全てのタイマーを止めました。")
                return

            if text == "/chat" and rpg == 0 and jan == 0:

                if free == 0:
                    free = 1
                    await message.channel.send("喋ります！")
                    return

<<<<<<< Updated upstream
                else:
                    free = 0
                    await message.channel.send("黙ります。")
                    return

            global vt
            if text == "/rpg" and chat == 0 and jan == 0:
                if rpg == 0:
                    rpg = 1
                    await message.channel.send("RPGモードです。")
                    await message.channel.send("**メニュー**\n```1.アイテム　　　2.ステータス\n3.装備　　　　　"
                                               "4.フィールド移動\n5.エンカウント　6.RPGモード終了```")
                    return

            # if text == "/test":
            #     try:
            #         while True:
            #             await message.channel.send(f'{str(588020674002419742)}')
            #
            #     except:
            #         await message.channel.send("エラー。")
            #         return
=======
        if text == "/test":
            print(vote_content)
            print(emoji_user)
>>>>>>> Stashed changes

        if text == "/gaaaaaaa_na":
            if gana == 0:
                gana = 1
                await message.channel.send("あぁぁぁぁ、がーな。様ぁぁああ。")
                return

            else:
                gana = 0
                await message.channel.send("黙ります。")
                return

        if message.author.id == 603462377874259968 and gana == 1:
            await message.channel.send("がーな。様の素晴らしいお言葉、ありがとうございます。")
            pass

        if re.search("おは",text) and rpg == 0:
            await message.channel.send("おはようございます" + message.author.name + "さん！")
            return

<<<<<<< Updated upstream
        elif re.search("こんに",text) and rpg == 0:
            await message.channel.send( "こんにちは" + message.author.name + "さん！")
=======
        elif re.search("こんに", text) and user_stat[user_id]["trigger"]["rpg"] == 0:
            await message.channel.send("こんにちは" + message.author.name + "さん！")
>>>>>>> Stashed changes
            return

        elif re.search("こんば",text) and rpg == 0:
            await message.channel.send("こんばんは" + message.author.name + "さん！")
            return

        elif re.search("振られ" or "ふられ" or "フラれ", text) and rpg == 0:
            await message.channel.send("そういう時もあります！\n次頑張りましょう！\n")
            return

        if re.search("/", text):
            pass

        else:
            if free == 0 and rpg == 0:
                with open('History.txt', 'a') as f:
                    f.write(text + "\n")

            elif free == 1:
                with open('History.txt', 'a') as f:
                    f.write(text + "\n")
                with open('History.txt', 'r') as p:
                    s = p.readlines()
                    await message.channel.send(random.choice(s))
                return

        if rpg == 1:
            # try:
                global place
                global main
                global monster_name
                global re_hp
                global vol_hp
                global re_mp
                global vol_mp
                global ch_monster_hp
                global ch_monster_mp
                global ch_monster_str
                global ch_monster_def
                global ch_monster_msr
                global ch_monster_mdf
                global ch_monster_spd
                global mp_pass
                global mp_pass_user
                global way
                global way_user
                global way_user_name
                global way_monster_name
                global user_turn
                global monster_turn
                global escape_trigger
                global item_trigger
                global item_name
                global turn_system
                global magic_flag
                global magic_flag_user
                global dm_user_ac
                global dm_mons_ac
                global monster_stat
                global enc_pass
                global place_enc
                global weapon_stat

                if text == "6" and vt == 0:
                    rpg = 0
                    await message.channel.send("RPGモード解除。")
                    return

                if text == "1" and vt == 0 and item_trigger == 0:
                    a = 1
                    user_stat[user_id]["rpg"]["item_list"] = []

                    if len(user_stat[user_id]["rpg"]["item"]) == 0:
                        await message.channel.send("しかしアイテムを持っていなかった！")
                        await message.channel.send(main)
                        return

                    for item in user_stat[user_id]["rpg"]["item"]:
                        user_stat[user_id]["rpg"]["item_list"].append(item)
                        await message.channel.send("{0}.{1}:{2}".format(a, item, user_stat[user_id]["rpg"]["item"][item]))
                        a = a + 1

                    item_trigger = 1
                    return

                if item_trigger == 1 and vt == 0:

                    # try:
                        if 0 < int(text) <= len(user_stat[user_id]["rpg"]["item_list"]):
                            a = int(text) - 1
                            await message.channel.send("**{0}**を使った！".format(use_item(user_stat, user_id, a)))

                            if re_hp == 1:
                                await message.channel.send("HPが**{0}**回復した！".format(vol_hp))
                                re_hp = 0
                                vol_hp = 0

                            if re_mp == 1:
                                await message.channel.send("MPが**{0}**回復した！".format(vol_mp))
                                re_mp = 0
                                vol_mp = 0

                            user_stat[user_id]["rpg"]["item"][user_stat[user_id]["rpg"]["item_list"][a]] = \
                                user_stat[user_id]["rpg"]["item"][user_stat[user_id]["rpg"]["item_list"][a]] - 1

                            if user_stat[user_id]["rpg"]["item"][user_stat[user_id]["rpg"]["item_list"][a]] == 0:
                                del user_stat[user_id]["rpg"]["item"][user_stat[user_id]["rpg"]["item_list"][a]]

                            await message.channel.send(main)
                            item_trigger = 0
                            return

                    # except:
                    #     await message.channel.send("正しい値を入力してください。")

                if text == "2" and vt == 0:
                    await message.channel.send(
                        "Lv:{0} JOB:{1}\nHP:{2}/{3} MP:{4}/{5}\nSTR:{6}/{7} DEF:{8}/{9}\nMSR:{10}/{11} MDF:{12}/{13}\n"
                        "SPD:{14}/{15} WEAPON:{16}\n{17}G {18}EXP\nPlace:{19}".format(
                            user_stat[user_id]["rpg"]["Lv"], user_stat[user_id]["rpg"]["job"], user_stat[user_id]["rpg"]["ch_user_hp"],
                            user_stat[user_id]["rpg"]["HP"], user_stat[user_id]["rpg"]["ch_user_mp"], user_stat[user_id]["rpg"]["MP"],
                            user_stat[user_id]["rpg"]["ch_user_str"], user_stat[user_id]["rpg"]["STR"],
                            user_stat[user_id]["rpg"]["ch_user_def"], user_stat[user_id]["rpg"]["DEF"],
                            user_stat[user_id]["rpg"]["ch_user_msr"], user_stat[user_id]["rpg"]["MSR"],
                            user_stat[user_id]["rpg"]["ch_user_mdf"], user_stat[user_id]["rpg"]["MDF"],
                            user_stat[user_id]["rpg"]["ch_user_spd"], user_stat[user_id]["rpg"]["SPD"],
                            user_stat[user_id]["rpg"]["weapon"], user_stat[user_id]["rpg"]["G"],
                            user_stat[user_id]["rpg"]["EXP"], user_stat[user_id]["rpg"]["place"]))
                    await message.channel.send(main)

                if text == "3" and vt == 0:
                    user_stat[user_id]["rpg"]["ch_user_str"] = \
                        user_stat[user_id]["rpg"]["ch_user_str"] - weapon_stat[user_stat[user_id]["rpg"]["weapon"]]["STR_Plus"]
                    #変更処理を挟みたい
                    user_stat[user_id]["rpg"]["ch_user_str"] = \
                        user_stat[user_id]["rpg"]["ch_user_str"] + weapon_stat[user_stat[user_id]["rpg"]["weapon"]]["STR_Plus"]

                if text == "4" and vt == 0:
                    global place_trigger
                    await message.channel.send("地名を入力してください。")

                    for Place in place_enc["place"]:
                        await message.channel.send("**{0}**".format(Place))

                    place_trigger = 1
                    return

                if place_trigger == 1:

                    if text in place_enc["place"]:
                        user_stat[user_id]["rpg"]["place"] = text
                        await message.channel.send("{0}に移動しました。".format(text))
                        await message.channel.send(main)
                        place_trigger = 0
                        return

                    else:
                        await message.channel.send("正しい地名を入力してください。")
                        for Place in place_enc["place"]:
                            await message.channel.send("**{0}**".format(Place))
                        return

                if text == "5" and vt == 0:

                    if user_stat[user_id]["rpg"]["place"] == "Home" or user_stat[user_id]["rpg"]["place"] == "Town":
                        await message.channel.send("ここにはモンスターがいない！")
                        await message.channel.send(main)
                        return

                    global vtr
                    text = None
                    vtr = message.author
                    monster_name = random.choice(place_enc[user_stat[user_id]["rpg"]["place"]]["enc"])
                    ch_monster_hp = monster_stat[monster_name]["HP"]
                    ch_monster_mp = monster_stat[monster_name]["MP"]
                    ch_monster_str = monster_stat[monster_name]["STR"]
                    ch_monster_def = monster_stat[monster_name]["DEF"]
                    ch_monster_msr = monster_stat[monster_name]["MSR"]
                    ch_monster_mdf = monster_stat[monster_name]["MDF"]
                    ch_monster_spd = monster_stat[monster_name]["SPD"]
                    magic_flag = 0
                    magic_flag_user = 0
                    mp_pass = 0
                    mp_pass_user = 0
                    print("{0}{1}{2}{3}{4}{5}{6}".format(ch_monster_hp, ch_monster_mp, ch_monster_str, ch_monster_def,
                                                         ch_monster_msr, ch_monster_mdf, ch_monster_spd))
                    await message.channel.send("戦闘開始！\n**{0}**が現れた！".format(monster_name))
                    await message.channel.send("どうする？\n```1.戦う\n2.特技\n3.魔法\n4.道具\n5.ステータス\n6.逃げる```")
                    vt = 1

                if vt == 1 and vtr == message.author:

                    if user_stat[user_id]["rpg"]["ch_user_spd"] > ch_monster_spd:#SED判定
                        user_turn = 1
                        monster_turn = 0

                    else:
                        monster_turn = 1
                        user_turn = 0

                    if text == "1":
                        way_user = "normal_attack_user"
                        turn_system = 1

                    if text == "4":
                        item_trigger = 1

                    if item_trigger == 1:
                        if text in user_stat[user_id]["rpg"]["item"]:
                            user_stat[user_id]["rpg"]["place"] = text
                            await message.channel.send("{0}に移動しました。".format(text))
                            await message.channel.send(main)
                            place_trigger = 0
                            return

                        else:
                            await message.channel.send("しかしそのアイテムは持っていない！")
                            for Item in user_stat[user_id]["rpg"]["item"]:
                                await message.channel.send("**{0}**".format(Item))
                            return

                    if text == "5":
                        await message.channel.send(
                            "Lv:{0}\nHP:{1}/{2} MP:{3}/{4}\nSTR:{5}/{6} DEF:{7}/{8}\nMSR:{9}/{10} MDF:{11}/{12}\n"
                            "SPD:{13}/{14}".format(
                                user_stat[user_id]["rpg"]["Lv"], user_stat[user_id]["rpg"]["ch_user_hp"], user_stat[user_id]["rpg"]["HP"],
                                user_stat[user_id]["rpg"]["ch_user_mp"], user_stat[user_id]["rpg"]["MP"],
                                user_stat[user_id]["rpg"]["ch_user_str"], user_stat[user_id]["rpg"]["STR"],
                                user_stat[user_id]["rpg"]["ch_user_def"],user_stat[user_id]["rpg"]["DEF"],
                                user_stat[user_id]["rpg"]["ch_user_msr"], user_stat[user_id]["rpg"]["MSR"],
                                user_stat[user_id]["rpg"]["ch_user_mdf"],user_stat[user_id]["rpg"]["MDF"],
                                user_stat[user_id]["rpg"]["ch_user_spd"], user_stat[user_id]["rpg"]["SPD"],))
                        await message.channel.send("どうする？\n```1.戦う\n2.特技\n3.魔法\n4.道具\n5.ステータス\n6.逃げる```")
                        return

                    if text == "6":
                        if user_turn == 1:
                            await message.channel.send("**逃げ切れた！**")
                            vt = 0
                            await message.channel.send(main)

                        elif monster_turn == 1:
                            await message.channel.send("しかし回り込まれてしまった！")
                            escape_trigger = 1
                            turn_system = 2

                    if text == "7":
                        print("デバッグ用")
                        user_turn = 0
                        escape_trigger = 1
                        turn_system = 2

                    if turn_system == 1 and escape_trigger == 0:    # 逃げなし
                        mp_pass = 0
                        dm_mons_ac = attack_user(user_stat,user_id,weapon_stat,way_user)    # モンスターダメージ蓄積

                    if turn_system == 1 or escape_trigger == 1:     # 逃げあり
                        mp_pass = 0
                        dm_user_ac = attack_monster(monster_stat,monster_name)              # ユーザーダメージ蓄積

<<<<<<< Updated upstream
                        if dm_user_ac > 0:

                            if magic_flag == 0:
                                user_stat[user_id]["rpg"]["ch_user_hp"] = user_stat[user_id]["rpg"]["ch_user_hp"] - dm_user_ac

                            else:
                                if ch_monster_mp > 0:
                                    user_stat[user_id]["rpg"]["ch_user_hp"] = user_stat[user_id]["rpg"]["ch_user_hp"] - dm_user_ac

                                else:
                                    mp_pass = 1
                                    pass

                        if dm_mons_ac > 0 and escape_trigger == 0:

                            if magic_flag_user == 0:
                                ch_monster_hp = ch_monster_hp - dm_mons_ac

                            else:
                                if user_stat[user_id]["rpg"]["ch_user_mp"] > 0:
                                    ch_monster_hp = ch_monster_hp - dm_mons_ac

                                else:
                                    mp_pass_user = 1
                                    pass

                        while 0 < turn_system < 3:

                            if user_stat[user_id]["rpg"]["ch_user_spd"] > ch_monster_spd and escape_trigger == 0:  # SED判定
                                user_turn = 1

                            else:
                                monster_turn = 1

                            if user_turn == 1 and turn_system < 3:
                                if dm_mons_ac > 0 and escape_trigger == 0:
                                    if mp_pass_user == 0:
                                        await message.channel.send("{0}！\n{1}に**{2}**のダメージを与えた！"
                                                                   .format(way_user_name,monster_name,dm_mons_ac))

                                    else:
                                        await message.channel.send("{0}！\nしかしMPが足りなかった！")
                                        mp_pass_user = 0

                                else:
                                    if mp_pass_user == 0:
                                        await message.channel.send("{0}！\nしかし{1}にダメージを与えられなかった！"
                                                                   .format(way_user_name,monster_name))

                                    else:
                                        await message.channel.send("{0}！\nしかしMPが足りなかった！".format(way_user_name))
                                        mp_pass_user = 0

                                if ch_monster_hp > 0:
                                    user_turn = 0
                                    monster_turn = 1
                                    turn_system = turn_system + 1

                                else:
                                    await message.channel.send("**{0}を倒した！**\n**{1}**EXP\n**{2}**G\nを得た！"
                                                               .format(monster_name,
                                                                       monster_stat[monster_name]["drop"]["EXP"],
                                                                       monster_stat[monster_name]["drop"]["G"]))

                                    Lv_up = result_win(user_stat, user_id, monster_stat, monster_name)

                                    if Lv_up == 1:
                                        await message.channel.send("レベルが上がった！")
                                        await message.channel.send("HPが{0} MPが{1}\nSTRが{2} DEFが{3}\n"
                                                                   "MSRが{4} MDFが{5}\nSPD{6} 上がった！"
                                                                   .format(up_hp_user, up_mp_user, up_str_user,
                                                                           up_def_user, up_msr_user, up_mdf_user,
                                                                           up_spd_user))

                                    user_turn = 0
                                    monster_turn = 0
                                    turn_system = 0
                                    vt = 0
                                    await message.channel.send(main)

                            if monster_turn == 1 and turn_system < 3:

                                if dm_user_ac > 0:

                                    if mp_pass == 0:
                                        await message.channel.send("{0}の{1}！\n**{2}**のダメージを受けた！"
                                                                   .format(monster_name,way_monster_name,dm_user_ac))

                                    else:
                                        await message.channel.send("{0}の{1}！\nしかしMPが足りなかった！"
                                                                   .format(monster_name,way_monster_name))
                                        mp_pass = 0

                                else:
                                    if mp_pass == 0:
                                        await message.channel.send("{0}の{1}！\nしかしダメージを受けなかった！"
                                                                   .format(monster_name, way_monster_name))

                                    else:
                                        await message.channel.send("{0}の{1}！\nしかしMPが足りなかった！"
                                                                   .format(monster_name,way_monster_name))
                                        mp_pass = 0

                                if user_stat[user_id]["rpg"]["ch_user_hp"] > 0:
                                    user_turn = 1
                                    monster_turn = 0
                                    turn_system = turn_system + 1

                                else:
                                    await message.channel.send("**死んでしまった！**")
                                    user_turn = 0
                                    monster_turn = 0
                                    turn_system = 0
                                    vt = 0
                                    user_stat[user_id]["rpg"]["ch_user_hp"] = user_stat[user_id]["rpg"]["HP"]
                                    user_stat[user_id]["rpg"]["ch_user_mp"] = user_stat[user_id]["rpg"]["MP"]
                                    user_stat[user_id]["rpg"]["ch_user_str"] = user_stat[user_id]["rpg"]["STR"]
                                    user_stat[user_id]["rpg"]["ch_user_def"] = user_stat[user_id]["rpg"]["DEF"]
                                    user_stat[user_id]["rpg"]["ch_user_msr"] = user_stat[user_id]["rpg"]["MSR"]
                                    user_stat[user_id]["rpg"]["ch_user_mdf"] = user_stat[user_id]["rpg"]["MDF"]
                                    user_stat[user_id]["rpg"]["ch_user_spd"] = user_stat[user_id]["rpg"]["SPD"]
                                    user_stat[user_id]["rpg"]["G"] = user_stat[user_id]["rpg"]["G"] / 2
                                    await message.channel.send(main)
                                    return

                        if turn_system == 3:
                            turn_system = 0
                            magic_flag = 0
                            magic_flag_user = 0
                            mp_pass = 0
                            mp_pass_user = 0
                            escape_trigger = 0
                            await message.channel.send("どうする？\n```1.戦う\n2.特技\n3.魔法\n4.道具\n5.ステータス\n6.逃げる```")
                            return

with open('C:/Users/st158/OneDrive/ドキュメント/Python Scripts/Token.json', 'r') as f:
=======
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
>>>>>>> Stashed changes
    bot_token = json.load(f)
    client.run(bot_token["Botton"]["token"])