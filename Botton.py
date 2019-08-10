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
from collections import defaultdict
import math
from pytube import YouTube
from discord.ext import commands
from discord.voice_client import VoiceClient
from copy import deepcopy
import reactions

client = discord.Client()

A = 0
done = 0
gana = 0
free = 0
vote = 0
chat = 0
off = 0
data = 0
main = " **メニュー**\n```{0}\n1.アイテム　　　2.ステータス\n3.装備　　　　　" \
                        "4.フィールド移動\n5.エンカウント　6.RPGモード終了\nplace:{1}```"
select = 0
user_stat = None
monster_stat = None
user_id = None
user_id_reaction = None
kosen = None
token = None
emoji = None
emoji_user = defaultdict(dict)

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
    global emoji
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
    ks = open('kosen19s.json', 'r', encoding='utf-8')
    kosen = json.load(ks)
    ks.close()
    ej = open('emoji.json', 'r')
    emoji = json.load(ej)
    ej.close()
    # for M in channels.members:
    #     user_stat[str(M.id)]["trigger"] = user_stat["Starter"]["trigger"].copy()

def file_len(fname):
    with open(fname) as f:

        for i, l in enumerate(f):
            pass

    return i + 1

def lenlen(text):
    i = 0
    for i, l in enumerate(text):
        pass

    return i + 1

def find_text_start_from(keyword,text):
    search = keyword + ".+"
    result = re.search(search, text)

    if result == None:
       return None

    else:
       return result.group(0).replace(keyword, "").strip()

def normal_attack_mons():
    user_stat[user_id]["rpg"]["dm_user_ac"] = user_stat[user_id]["rpg"]["ch_monster_str"] + random.randint(-1, 1) \
                  - user_stat[user_id]["rpg"]["ch_user_def"]
    user_stat[user_id]["rpg"]["way_monster_name"] = "攻撃"

def mera_mons():
    user_stat[user_id]["rpg"]["dm_user_ac"] = \
        user_stat[user_id]["rpg"]["ch_monster_msr"] * 2 - user_stat[user_id]["rpg"]["ch_user_mdf"]
    user_stat[user_id]["rpg"]["way_monster_name"] = "メラ"
    user_stat[user_id]["rpg"]["ch_monster_mp"] = user_stat[user_id]["rpg"]["ch_monster_mp"] - 3
    user_stat[user_id]["rpg"]["rpg_trigger"]["magic_flag"] = 1

def attack_monster():
    eval(random.choice(monster_stat[user_stat[user_id]["rpg"]["monster_name"]]["way"]))()

def normal_attack_user():
    user_stat[user_id]["rpg"]["dm_mons_ac"] = user_stat[user_id]["rpg"]["ch_user_str"] \
                 + random.randint(weapon_stat[user_stat[user_id]["rpg"]["weapon"]]["mura"][0],
                                  weapon_stat[user_stat[user_id]["rpg"]["weapon"]]["mura"][1]) \
                                              - user_stat[user_id]["rpg"]["ch_monster_def"]
    user_stat[user_id]["rpg"]["way_user_name"] = "攻撃"

def mera():
    user_stat[user_id]["rpg"]["dm_mons_ac"] = user_stat[user_id]["rpg"]["ch_user_msr"] * 2 - \
                                              user_stat[user_id]["rpg"]["ch_monster_mdf"]
    user_stat[user_id]["rpg"]["ch_user_mp"] = user_stat[user_id]["rpg"]["ch_user_mp"] - 3
    user_stat[user_id]["rpg"]["way_user_name"] = "メラ"

def attack_user():
    eval(user_stat[user_id]["rpg"]["way_user"])()

def Medicinal_herbs():
    user_stat[user_id]["rpg"]["rpg_trigger"]["re_hp"] = 1
    user_stat[user_id]["rpg"]["vol_hp"] = 10
    user_stat[user_id]["rpg"]["ch_user_hp"] = user_stat[user_id]["rpg"]["ch_user_hp"] + 10

    if user_stat[user_id]["rpg"]["ch_user_hp"] > user_stat[user_id]["rpg"]["HP"]:
        user_stat[user_id]["rpg"]["ch_user_hp"] = user_stat[user_id]["rpg"]["HP"]

    user_stat[user_id]["rpg"]["way_user_name"] = "薬草"

def use_item(a):
    eval(user_stat[user_id]["rpg"]["item_list"][a])()

def result_win():
    user_stat[user_id]["rpg"]["G"] = user_stat[user_id]["rpg"]["G"] \
                                     + monster_stat[user_stat[user_id]["rpg"]["monster_name"]]["drop"]["G"]
    user_stat[user_id]["rpg"]["EXP"] = user_stat[user_id]["rpg"]["EXP"] \
                                       + monster_stat[user_stat[user_id]["rpg"]["monster_name"]]["drop"]["EXP"]

    if user_stat[user_id]["rpg"]["EXP"] > \
            user_stat[user_id]["rpg"]["Lv"] * user_stat[user_id]["rpg"]["Lv"] * user_stat[user_id]["rpg"]["Lv"]:
        user_stat[user_id]["rpg"]["up_hp_user"] \
            = random.randint(user_stat[user_stat[user_id]["rpg"]["job"]]["up_hp"][0],
                             user_stat[user_stat[user_id]["rpg"]["job"]]["up_hp"][1])
        user_stat[user_id]["rpg"]["up_mp_user"] \
            = random.randint(user_stat[user_stat[user_id]["rpg"]["job"]]["up_mp"][0],
                             user_stat[user_stat[user_id]["rpg"]["job"]]["up_mp"][1])
        user_stat[user_id]["rpg"]["up_str_user"] \
            = random.randint(user_stat[user_stat[user_id]["rpg"]["job"]]["up_str"][0],
                             user_stat[user_stat[user_id]["rpg"]["job"]]["up_str"][1])
        user_stat[user_id]["rpg"]["up_def_user"] \
            = random.randint(user_stat[user_stat[user_id]["rpg"]["job"]]["up_def"][0],
                             user_stat[user_stat[user_id]["rpg"]["job"]]["up_def"][1])
        user_stat[user_id]["rpg"]["up_msr_user"] \
            = random.randint(user_stat[user_stat[user_id]["rpg"]["job"]]["up_msr"][0],
                             user_stat[user_stat[user_id]["rpg"]["job"]]["up_msr"][1])
        user_stat[user_id]["rpg"]["up_mdf_user"] \
            = random.randint(user_stat[user_stat[user_id]["rpg"]["job"]]["up_mdf"][0],
                             user_stat[user_stat[user_id]["rpg"]["job"]]["up_mdf"][1])
        user_stat[user_id]["rpg"]["up_spd_user"] \
            = random.randint(user_stat[user_stat[user_id]["rpg"]["job"]]["up_spd"][0],
                             user_stat[user_stat[user_id]["rpg"]["job"]]["up_spd"][1])
        user_stat[user_id]["rpg"]["Lv"] = user_stat[user_id]["rpg"]["Lv"] + 1
        user_stat[user_id]["rpg"]["HP"] = user_stat[user_id]["rpg"]["HP"] + user_stat[user_id]["rpg"]["up_hp_user"]
        user_stat[user_id]["rpg"]["MP"] = user_stat[user_id]["rpg"]["MP"] + user_stat[user_id]["rpg"]["up_mp_user"]
        user_stat[user_id]["rpg"]["STR"] = user_stat[user_id]["rpg"]["STR"] + user_stat[user_id]["rpg"]["up_str_user"]
        user_stat[user_id]["rpg"]["DEF"] = user_stat[user_id]["rpg"]["DEF"] + user_stat[user_id]["rpg"]["up_def_user"]
        user_stat[user_id]["rpg"]["MSR"] = user_stat[user_id]["rpg"]["MSR"] + user_stat[user_id]["rpg"]["up_msr_user"]
        user_stat[user_id]["rpg"]["MDF"] = user_stat[user_id]["rpg"]["MDF"] + user_stat[user_id]["rpg"]["up_mdf_user"]
        user_stat[user_id]["rpg"]["SPD"] = user_stat[user_id]["rpg"]["SPD"] + user_stat[user_id]["rpg"]["up_spd_user"]
        user_stat[user_id]["rpg"]["ch_user_hp"] = user_stat[user_id]["rpg"]["HP"]
        user_stat[user_id]["rpg"]["ch_user_mp"] = user_stat[user_id]["rpg"]["MP"]
        user_stat[user_id]["rpg"]["ch_user_str"] = user_stat[user_id]["rpg"]["STR"]
        user_stat[user_id]["rpg"]["ch_user_def"] = user_stat[user_id]["rpg"]["DEF"]
        user_stat[user_id]["rpg"]["ch_user_msr"] = user_stat[user_id]["rpg"]["MSR"]
        user_stat[user_id]["rpg"]["ch_user_mdf"] = user_stat[user_id]["rpg"]["MDF"]
        user_stat[user_id]["rpg"]["ch_user_spd"] = user_stat[user_id]["rpg"]["SPD"]
        user_stat[user_id]["rpg"]["rpg_trigger"]["Lv_up"] = 1

def battle_system():    #1ターンの処理
    #turn_system > 0で渡される予定
    d = []
    #ターン処理開始
    while 0 < user_stat[user_id]["rpg"]["rpg_trigger"]["turn_system"] < 3:

        if user_stat[user_id]["rpg"]["rpg_trigger"]["user_turn"] == 1:
            attack_user()
            user_stat[user_id]["rpg"]["rpg_trigger"]["user_turn"] = 0
            if user_stat[user_id]["rpg"]["dm_mons_ac"] > 0:

                if user_stat[user_id]["rpg"]["rpg_trigger"]["magic_flag_user"] == 0:
                    user_stat[user_id]["rpg"]["ch_monster_hp"] = user_stat[user_id]["rpg"]["ch_monster_hp"] \
                                                                 - user_stat[user_id]["rpg"]["dm_mons_ac"]
                    d.append("{0}！\n{1}に**{2}**のダメージを与えた！"
                                                               .format(user_stat[user_id]["rpg"]["way_user_name"]
                                                                       ,user_stat[user_id]["rpg"]["monster_name"]
                                                                       ,user_stat[user_id]["rpg"]["dm_mons_ac"]))
                else:
                    if user_stat[user_id]["rpg"]["ch_user_mp"] > 0:
                        d.append("{0}！\n{1}に**{2}**のダメージを与えた！"
                                 .format(user_stat[user_id]["rpg"]["way_user_name"]
                                         , user_stat[user_id]["rpg"]["monster_name"]
                                         , user_stat[user_id]["rpg"]["dm_mons_ac"]))

                    else:
                        d.append("{0}の{1}！\nしかしMPが足りなかった！"
                                 .format(user_stat[user_id]["rpg"]["monster_name"],
                                         user_stat[user_id]["rpg"]["way_monster_name"],))

            else:
                d.append("{0}！\nしかし{1}にダメージを与えられなかった！"
                            .format(user_stat[user_id]["rpg"]["way_user_name"],
                            user_stat[user_id]["rpg"]["monster_name"]))

            if user_stat[user_id]["rpg"]["ch_monster_hp"] > 0:  #モンスター生きてたら
                user_stat[user_id]["rpg"]["rpg_trigger"]["turn_system"] = \
                    user_stat[user_id]["rpg"]["rpg_trigger"]["turn_system"] + 1

            else:   #モンスター死んでたら
                d.append("**{0}を倒した！**\n**{1}**EXP **{2}**G を得た！"
                                                           .format(user_stat[user_id]["rpg"]["monster_name"],
                                                                   monster_stat[user_stat[user_id]["rpg"]
                                                                   ["monster_name"]]["drop"]["EXP"],
                                                                   monster_stat[user_stat[user_id]["rpg"]
                                                                   ["monster_name"]]["drop"]["G"]))
                result_win()

                if user_stat[user_id]["rpg"]["rpg_trigger"]["Lv_up"] == 1:
                    user_stat[user_id]["rpg"]["rpg_trigger"]["Lv_up"] = 0
                    d.append("レベルが上がった！\nHPが{0} MPが{1}\nSTRが{2} DEFが{3}\nMSRが{4} MDFが{5}"
                             "\nSPD{6} 上がった！".format(user_stat[user_id]["rpg"]["up_hp_user"],
                                                                       user_stat[user_id]["rpg"]["up_mp_user"],
                                                                       user_stat[user_id]["rpg"]["up_str_user"],
                                                                       user_stat[user_id]["rpg"]["up_def_user"],
                                                                       user_stat[user_id]["rpg"]["up_msr_user"],
                                                                       user_stat[user_id]["rpg"]["up_mdf_user"],
                                                                       user_stat[user_id]["rpg"]["up_spd_user"]))
                user_stat[user_id]["rpg"]["rpg_trigger"]["turn_system"] = 0
                user_stat[user_id]["rpg"]["rpg_trigger"]["vt"] = 2
                user_stat[user_id]["rpg"]["rpg_trigger"]["magic_flag_user"] = 0
                user_stat[user_id]["rpg"]["rpg_trigger"]["magic_flag"] = 0
                break

            user_stat[user_id]["rpg"]["rpg_trigger"]["magic_flag_user"] = 0
            user_stat[user_id]["rpg"]["rpg_trigger"]["user_turn"] = 0
            user_stat[user_id]["rpg"]["rpg_trigger"]["monster_turn"] = 1
            user_stat[user_id]["rpg"]["rpg_trigger"]["turn_system"] = \
                user_stat[user_id]["rpg"]["rpg_trigger"]["turn_system"] + 1

        if user_stat[user_id]["rpg"]["rpg_trigger"]["monster_turn"] == 1:
            attack_monster()              # ユーザーダメージ蓄積
            user_stat[user_id]["rpg"]["rpg_trigger"]["monster_turn"] = 0
            if user_stat[user_id]["rpg"]["dm_user_ac"] > 0:
                if user_stat[user_id]["rpg"]["rpg_trigger"]["magic_flag"] == 0:
                    user_stat[user_id]["rpg"]["ch_user_hp"] = user_stat[user_id]["rpg"]["ch_user_hp"] \
                                                              - user_stat[user_id]["rpg"]["dm_user_ac"]
                    d.append("{0}の{1}！\n**{2}**のダメージを受けた！"
                                                            .format(user_stat[user_id]["rpg"]["monster_name"],
                                                                    user_stat[user_id]["rpg"]["way_monster_name"],
                                                                    user_stat[user_id]["rpg"]["dm_user_ac"]))

                else:
                    if user_stat[user_id]["rpg"]["ch_monster_mp"] > 0:
                        user_stat[user_id]["rpg"]["ch_user_hp"] = user_stat[user_id]["rpg"]["ch_user_hp"] \
                                                                  - user_stat[user_id]["rpg"]["dm_user_ac"]
                        d.append("{0}の{1}！\n**{2}**のダメージを受けた！"
                                                            .format(user_stat[user_id]["rpg"]["monster_name"],
                                                                    user_stat[user_id]["rpg"]["way_monster_name"],
                                                                    user_stat[user_id]["rpg"]["dm_user_ac"]))

                    else:
                        d.append("{0}の{1}！\nしかしMPが足りなかった！"
                               .format(user_stat[user_id]["rpg"]["monster_name"],
                                    user_stat[user_id]["rpg"]["way_monster_name"]))

            if user_stat[user_id]["rpg"]["ch_user_hp"] > 0:
                pass

            else:
                d.append("**死んでしまった！**")
                user_stat[user_id]["rpg"]["rpg_trigger"]["user_turn"] = 0
                user_stat[user_id]["rpg"]["rpg_trigger"]["monster_turn"] = 0
                user_stat[user_id]["rpg"]["rpg_trigger"]["turn_system"] = 0
                user_stat[user_id]["rpg"]["rpg_trigger"]["vt"] = 2
                user_stat[user_id]["rpg"]["ch_user_hp"] = user_stat[user_id]["rpg"]["HP"]
                user_stat[user_id]["rpg"]["ch_user_mp"] = user_stat[user_id]["rpg"]["MP"]
                user_stat[user_id]["rpg"]["ch_user_str"] = user_stat[user_id]["rpg"]["STR"]
                user_stat[user_id]["rpg"]["ch_user_def"] = user_stat[user_id]["rpg"]["DEF"]
                user_stat[user_id]["rpg"]["ch_user_msr"] = user_stat[user_id]["rpg"]["MSR"]
                user_stat[user_id]["rpg"]["ch_user_mdf"] = user_stat[user_id]["rpg"]["MDF"]
                user_stat[user_id]["rpg"]["ch_user_spd"] = user_stat[user_id]["rpg"]["SPD"]
                user_stat[user_id]["rpg"]["G"] = math.floor(user_stat[user_id]["rpg"]["G"] / 2)
                break

        user_stat[user_id]["rpg"]["rpg_trigger"]["magic_flag"] = 0
        user_stat[user_id]["rpg"]["rpg_trigger"]["user_turn"] = 1
        user_stat[user_id]["rpg"]["rpg_trigger"]["monster_turn"] = 0
        user_stat[user_id]["rpg"]["rpg_trigger"]["turn_system"] = \
            user_stat[user_id]["rpg"]["rpg_trigger"]["turn_system"] + 1

    user_stat[user_id]["rpg"]["rpg_trigger"]["magic_flag"] = 0
    user_stat[user_id]["rpg"]["rpg_trigger"]["magic_flag_user"] = 0
    user_stat[user_id]["rpg"]["rpg_trigger"]["user_turn"] = 0
    user_stat[user_id]["rpg"]["rpg_trigger"]["monster_turn"] = 0
    user_stat[user_id]["rpg"]["rpg_trigger"]["turn_system"] = 0

    d = map(str, d)
    d = "\n".join(d)
    return d

@client.event
async def on_message(message):

    if not message.channel.id == 603525315515645962: #19s用
        return

    if client.user != message.author:
        text = message.content
        global free
        global gana
        global user_id
        global main
        user_id = str(message.author.id)
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
              }
            }

        if message.channel.id in client.get_all_channels() == 0:
            print("全く、Botに世知辛い世の中だぜっ。")
            return

        try:
            if not user_stat[user_id]["trigger"]["data"] == 0:
                pass

        except:
            user_stat[user_id] = starter.copy()

        finally:
            if text == "/set.server":

                if message.author.guild_permissions.administrator:

                    for M in message.guild.members:
                        print(str(M) + "\n" + str(M.id))
                        user_stat[str(M.id)] = starter.copy()

                    with open('user_stat.json', "w") as a:
                        json.dump(user_stat, a, indent=3)

                    await message.channel.send("(ﾟ∀ﾟ)ｱﾋｬﾋｬﾋｬﾋｬﾋｬﾋｬ")
                    return

                else:
                    await message.channel.send("サーバーの管理者が操作してください。")

        if text == "/save":
            with open('user_stat.json', "w") as w:
                json.dump(user_stat, w, indent=3)
            await message.channel.send("セーブが完了しました。")

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

        if user_stat[user_id]["trigger"]["janken"] == 2:
            await message.channel.send("じゃーんけーん\n```ぐー\nちょき\nぱー```")
            user_stat[user_id]["trigger"]["janken"] = 3
            return

        if user_stat[user_id]["trigger"]["janken"] == 3:
            win_bot = "勝ち申した。"
            win_user = "負け申した。"
            soso = "あーいこーで\n```ぐー\nちょき\nぱー```"
            bot_pon = random.choice(["ぐー", "ちょき", "ぱー"])

            if bot_pon == "ぐー":
                user_stat[user_id]["janken"]["bot_pon_number"] = 0

            elif bot_pon == "ちょき":
                user_stat[user_id]["janken"]["bot_pon_number"] = 1

            elif bot_pon == "ぱー":
                user_stat[user_id]["janken"]["bot_pon_number"] = 2

            if text == "ぐー":
                await message.channel.send(bot_pon)

                if user_stat[user_id]["janken"]["bot_pon_number"] == 0:
                    await message.channel.send(soso)
                    return

                elif user_stat[user_id]["janken"]["bot_pon_number"] == 1:
                    await message.channel.send(win_user)
                    user_stat[user_id]["janken"]["result"] = "win"

                elif user_stat[user_id]["janken"]["bot_pon_number"] == 2:
                    await message.channel.send(win_bot)
                    user_stat[user_id]["janken"]["result"] = "lose"

            elif text == "ちょき":
                await message.channel.send(bot_pon)

                if user_stat[user_id]["janken"]["bot_pon_number"] == 0:
                    await message.channel.send(win_bot)
                    user_stat[user_id]["janken"]["result"] = "lose"

                elif user_stat[user_id]["janken"]["bot_pon_number"] == 1:
                    await message.channel.send(soso)
                    return

                elif user_stat[user_id]["janken"]["bot_pon_number"] == 2:
                    await message.channel.send(win_user)
                    user_stat[user_id]["janken"]["result"] = "win"

            elif text == "ぱー":
                await message.channel.send(bot_pon)

                if user_stat[user_id]["janken"]["bot_pon_number"] == 0:
                    await message.channel.send(win_user)
                    user_stat[user_id]["janken"]["result"] = "win"

                elif user_stat[user_id]["janken"]["bot_pon_number"] == 1:
                    await message.channel.send(win_bot)
                    user_stat[user_id]["janken"]["result"] = "lose"

                elif user_stat[user_id]["janken"]["bot_pon_number"] == 2:
                    await message.channel.send(soso)
                    return

            else:
                return

            user_stat[user_id]["trigger"]["janken"] = 4

        if user_stat[user_id]["trigger"]["janken"] == 4:

            if user_stat[user_id]["janken"]["result"] == "win":
                user_stat[user_id]["casino"]["coin"] \
                    = user_stat[user_id]["casino"]["coin"] + user_stat[user_id]["casino"]["cost"]
                user_stat[user_id]["janken"]["result_count"][0] = user_stat[user_id]["janken"]["result_count"][0] + 1

            elif user_stat[user_id]["janken"]["result"] == "lose":
                user_stat[user_id]["casino"]["coin"] = user_stat[user_id]["casino"]["coin"] - \
                                                       user_stat[user_id]["casino"]["cost"]
                user_stat[user_id]["janken"]["result_count"][1] = user_stat[user_id]["janken"]["result_count"][1] + 1

            await message.channel.send("coin:{0}\n{1}勝 {2}敗\n連戦？\n```する\nしない```"
                                       .format(user_stat[user_id]["casino"]["coin"],
                                               user_stat[user_id]["janken"]["result_count"][0],
                                               user_stat[user_id]["janken"]["result_count"][1]))
            user_stat[user_id]["trigger"]["janken"] = 5

        if user_stat[user_id]["trigger"]["janken"] == 5:

            if text == "する":
                await message.channel.send("あなたのcoin:{0}\n掛け金を入力してください。\n(掛け金は5以下)"
                                           .format(user_stat[user_id]["casino"]["coin"]))
                user_stat[user_id]["trigger"]["janken"] = 1
                pass

            elif text == "しない":
                user_stat[user_id]["trigger"]["janken"] = 0
                user_stat[user_id]["casino"]["cost"] = 0
                await message.channel.send("またね！")
                return

        if message.author.id == 432897451209261057:
            global PASSCORD
            global off

            if text == "/role.server":

                if message.author.guild_permissions.administrator:

                    for M in message.guild.members:
                        user_stat[user_id]["official"]["一般役職"] = []
                        for i in M.roles:
                            print(i.name)
                            user_stat[str(M.id)]["official"]["一般役職"].append(i.name)
                            if "@everyone" in user_stat[str(M.id)]["official"]["一般役職"]:
                                user_stat[str(M.id)]["official"]["一般役職"].remove("@everyone")
                            if "bot" in user_stat[str(M.id)]["official"]["一般役職"]:
                                user_stat[str(M.id)]["official"]["一般役職"].remove("bot")
                            if "開発" in user_stat[str(M.id)]["official"]["一般役職"]:
                                user_stat[str(M.id)]["official"]["一般役職"].remove("開発")
                            if "つよつよ" in user_stat[str(M.id)]["official"]["一般役職"]:
                                user_stat[str(M.id)]["official"]["一般役職"].remove("つよつよ")
                            if "ドン" in user_stat[str(M.id)]["official"]["一般役職"]:
                                user_stat[str(M.id)]["official"]["一般役職"].remove("ドン")
                            if "ヤクザ" in user_stat[str(M.id)]["official"]["一般役職"]:
                                user_stat[str(M.id)]["official"]["一般役職"].remove("ヤクザ")

                    with open('user_stat.json', "w") as a:
                        json.dump(user_stat, a, indent=3)

                    await message.channel.send("(ﾟ∀ﾟ)ｱﾋｬ")

            if text == "/logout@home":
                await message.channel.send("パスコードを入力してください。")
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

            # if text.startswith("/tes"):
            #     await VoiceClient.connect(client.get_channel("604527782977863700"))
            #
            #     # player = await voice.create_ytdl_player(find_text_start_from("url:", text))
            #     # player.start()

        if text == "/roles":
            d = []

            for i in user_stat[user_id]["official"]["一般役職"]:
                c = discord.utils.get(message.guild.roles, name=i)
                await message.author.add_roles(c)

            for i in message.author.roles:
                if not i.name == "@everyone":
                    d.append(i.name)

                else:
                    pass

            d = map(str, d)
            d = "\n".join(d)
            await message.channel.send(d)
            return

        if text == "/role":
            user_stat[user_id]["trigger"]["役職決め"] = 0
            try:
                for i in user_stat[user_id]["official"]["一般役職"]:
                    d = discord.utils.get(message.guild.roles, name=i)
                    await message.author.remove_roles(d)
            except:
                pass

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

        if not user_stat[user_id]["trigger"]["役職決め"] == 0 and text == "/cancel":
            await message.channel.send("役職追加をもう一度最初からお願いします！")
            user_stat[user_id]["trigger"]["役職決め"] = 0
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

            if text == "/finish"and user_stat[user_id]["trigger"]["役職決め"] == 5:
                for i in user_stat[user_id]["official"]["一般役職"]:
                    d = discord.utils.get(message.guild.roles, name=i)
                    await message.author.add_roles(d)

                await message.channel.send("お疲れ様でした！\nこれで役職設定は終了です！")
                user_stat[user_id]["trigger"]["役職決め"] = 0
                return

        if text == "/help":
            with open('readme.txt', 'r') as a:
                d = a.read()
                await message.channel.send("```{0}```".format(d))

        if text == "/reset" and user_stat[user_id]["trigger"]["rpg"] == 0:

            try:
                for i in user_stat[user_id]["official"]["一般役職"]:
                    d = discord.utils.get(message.guild.roles, name=i)
                    await message.author.remove_roles(d)

            except:
                pass

            print(starter)
            user_stat[user_id] = starter.copy()

            with open('user_stat.json', "w") as a:
                json.dump(user_stat, a, indent=3)
            await message.channel.send("データを初期化しました。")
            return

        if text == "/exchange":
            await message.channel.send("G:{0}\n10G→1coinです。\nいくら交換しますか？(coin数)"
                                       .format(user_stat[user_id]["rpg"]["G"]))
            user_stat[user_id]["trigger"]["exchange"] = 1
            return

        if user_stat[user_id]["trigger"]["exchange"] == 1:

            if text == "/cancel":
                user_stat[user_id]["trigger"]["exchange"] = 0
                await message.channel.send("交換を中止しました。")
                return

            change = int(text)
            if change * 10 > user_stat[user_id]["rpg"]["G"]:
                await message.channel.send("値が大きすぎます。")
                return

            else:
                user_stat[user_id]["rpg"]["G"] = user_stat[user_id]["rpg"]["G"] - change * 10
                user_stat[user_id]["casino"]["coin"] = user_stat[user_id]["casino"]["coin"] + change
                user_stat[user_id]["trigger"]["exchange"] = 0
                await message.channel.send("交換しました。")
                return

        if text.startswith("/ques"):
            a = text.count(".")
            Q = find_text_start_from("q:", text)
            H = int(find_text_start_from("h:", text))
            M = int(find_text_start_from("m:", text))
            T = H * 3600 + M * 60
            anc = []
            b = 0
            for i in range(a):
                anc.append("{0}  {1}".format(find_text_start_from(("{0}.".format(i + 1)), text), emoji["emoji"][b]))
                b = b + 1
            d = map(str, anc)
            d = "\n".join(d)
            msg = await message.channel.send("{0}\n{1}".format(Q, d))
            # for i in range(a):
            # await client.add_reaction(msg, "dog")
            await asyncio.sleep(T)

            #reaction数計測
            #結果表示


        if text == "/now":

            if user_stat[user_id]["trigger"]["rpg"] == 1:
                await message.channel.send("[RPGモード中です]")

            hour = datetime.now().strftime("%H")
            minute = datetime.now().strftime("%M")
            H = int(hour)

            if client.user != message.author:

                if 3 <= H < 11:
                    x = "おはようございます\n"

                elif 11 <= H < 18:
                    x = "こんにちは\n"

                else:
                    x = "こんばんは\n"

                await message.channel.send("{0}{1}:{2}です".format(x, hour, minute))
                return

        if text.startswith("/timer"):

            try:

                if user_stat[user_id]["rpg"]["rpg_trigger"]["rpg"] == 1:
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

                    if user_stat[user_id]["rpg"]["rpg_trigger"]["rpg"] == 1:
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
                return

        if text == "/stop":
            done = 1
            await message.channel.send("全てのタイマーを止めました。")
            return

        if text == "/chat" and user_stat[user_id]["rpg"]["rpg_trigger"]["rpg"]\
            and user_stat[user_id]["trigger"]["janken"] == 0:

            if free == 0:
                free = 1
                await message.channel.send("喋ります！")
                return

            else:
                free = 0
                await message.channel.send("黙ります。")
                return

        if text == "/rpg" and chat == 0 and user_stat[user_id]["trigger"]["rpg"] == 0:
            user_stat[user_id]["trigger"]["rpg"] = 1
            await message.channel.send("RPGモードです。")
            user_stat[user_id]["rpg"]["rpg_trigger"]["main"] = 1
            await message.channel.send(main.format(message.author.name, user_stat[user_id]["rpg"]["place"]))

        if text == "/test":
            try:
                # for M in message.guild.members:
                #     print(str(M) + "\n" + str(M.id))
                #     user_stat[str(M.id)]["rpg"]["rpg_trigger"]["main"] = starter["rpg"]["rpg_trigger"]["main"]

                print(user_stat[user_id])
                return

            except:
                await message.channel.send("エラー。")
                return

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

        if re.search("おは", text) and user_stat[user_id]["trigger"]["rpg"] == 0:
            await message.channel.send("おはようございます" + message.author.name + "さん！")
            return

        elif re.search("こんに", text) and user_stat[user_id]["trigger"]["rpg"] == 0:
            await message.channel.send( "こんにちは" + message.author.name + "さん！")
            return

        elif re.search("こんば", text) and user_stat[user_id]["trigger"]["rpg"] == 0:
            await message.channel.send("こんばんは" + message.author.name + "さん！")
            return

        elif re.search("振られ" or "ふられ" or "フラれ", text) and user_stat[user_id]["trigger"]["rpg"] == 0:
            await message.channel.send("そういう時もあります！\n次頑張りましょう！\n")
            return

        # if re.search("/", text) and user_stat[user_id]["trigger"]["rpg"] == 1:
        #     pass
        #
        # else:
        #     if free == 0 and user_stat[user_id]["trigger"]["rpg"] == 0:
        #         with open('History.txt', 'a') as a:
        #             a.write(text + "\n")
        #
        #     elif free == 1:
        #         with open('History.txt', 'a') as f:
        #             f.write(text + "\n")
        #         with open('History.txt', 'r') as p:
        #             s = p.readlines()
        #             await message.channel.send(random.choice(s))
        #         return

        if user_stat[user_id]["trigger"]["rpg"] == 1:

            if user_stat[user_id]["rpg"]["rpg_trigger"]["main"] == 1:

                if text == "1" and user_stat[user_id]["rpg"]["rpg_trigger"]["main"] == 1:
                    user_stat[user_id]["rpg"]["rpg_trigger"]["main"] = 0
                    user_stat[user_id]["rpg"]["rpg_trigger"]["item_trigger"] = 1
                    user_stat[user_id]["rpg"]["item_list"] = []
                    if len(user_stat[user_id]["rpg"]["item"]) == 0:
                        user_stat[user_id]["rpg"]["rpg_trigger"]["main"] = 1
                        user_stat[user_id]["rpg"]["rpg_trigger"]["item_trigger"] = 0
                        await message.channel.send("しかしアイテムを持っていなかった！")
                        await message.channel.send(main.format(message.author.name, user_stat[user_id]["rpg"]["place"]))
                        return
                    a = 1
                    d = []
                    user_stat[user_id]["rpg"]["item_list"] = []
                    for item in user_stat[user_id]["rpg"]["item"]:
                        d.append("**{0}.{1}**：{2}".format(a, item, user_stat[user_id]["rpg"]["item"][item]))
                        user_stat[user_id]["rpg"]["item_list"].append(item)
                        a = a + 1
                    d.append("{0}.戻る".format(a))
                    d = map(str, d)
                    d = "\n".join(d)
                    await message.channel.send(d)
                    return

                if text == "2" and user_stat[user_id]["rpg"]["rpg_trigger"]["main"] == 1:
                    user_stat[user_id]["rpg"]["rpg_trigger"]["main"] = 0
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
                    user_stat[user_id]["rpg"]["rpg_trigger"]["main"] = 1
                    await message.channel.send(main.format(message.author.name, user_stat[user_id]["rpg"]["place"]))
                    return

                if text == "3" and user_stat[user_id]["rpg"]["rpg_trigger"]["main"] == 1:
                    user_stat[user_id]["rpg"]["ch_user_str"] = \
                        user_stat[user_id]["rpg"]["ch_user_str"] - weapon_stat[user_stat[user_id]["rpg"]["weapon"]]["STR_Plus"]
                    #変更処理を挟みたい
                    user_stat[user_id]["rpg"]["ch_user_str"] = \
                        user_stat[user_id]["rpg"]["ch_user_str"] + weapon_stat[user_stat[user_id]["rpg"]["weapon"]]["STR_Plus"]
                    return

                if text == "4" and user_stat[user_id]["rpg"]["rpg_trigger"]["main"] == 1:
                    user_stat[user_id]["rpg"]["rpg_trigger"]["place_trigger"] = 1
                    user_stat[user_id]["rpg"]["rpg_trigger"]["main"] = 0
                    await message.channel.send("番号を入力してください。")
                    a = 1
                    d = []
                    for Place in place_enc["place"]:
                        d.append("**{0}.{1}**".format(a, Place))
                        a = a + 1
                    d.append("{0}.戻る".format(a))
                    d = map(str, d)
                    d = "\n".join(d)
                    await message.channel.send(d)
                    return

                if text == "5" and user_stat[user_id]["rpg"]["rpg_trigger"]["main"] == 1:
                    user_stat[user_id]["rpg"]["rpg_trigger"]["main"] = 0

                    if user_stat[user_id]["rpg"]["place"] == "家" or user_stat[user_id]["rpg"]["place"] == "町":
                        await message.channel.send("ここにはモンスターがいない！")
                        user_stat[user_id]["rpg"]["rpg_trigger"]["main"] = 1
                        await message.channel.send(main.format(message.author.name, user_stat[user_id]["rpg"]["place"]))
                        return

                    user_stat[user_id]["rpg"]["vtr"] = message.author.name
                    user_stat[user_id]["rpg"]["monster_name"] \
                        = random.choice(place_enc[user_stat[user_id]["rpg"]["place"]]["enc"])
                    user_stat[user_id]["rpg"]["ch_monster_hp"] = \
                    monster_stat[user_stat[user_id]["rpg"]["monster_name"]]["HP"]
                    user_stat[user_id]["rpg"]["ch_monster_mp"] = \
                    monster_stat[user_stat[user_id]["rpg"]["monster_name"]]["MP"]
                    user_stat[user_id]["rpg"]["ch_monster_str"] = \
                    monster_stat[user_stat[user_id]["rpg"]["monster_name"]]["STR"]
                    user_stat[user_id]["rpg"]["ch_monster_def"] = \
                    monster_stat[user_stat[user_id]["rpg"]["monster_name"]]["DEF"]
                    user_stat[user_id]["rpg"]["ch_monster_msr"] = \
                    monster_stat[user_stat[user_id]["rpg"]["monster_name"]]["MSR"]
                    user_stat[user_id]["rpg"]["ch_monster_mdf"] = \
                    monster_stat[user_stat[user_id]["rpg"]["monster_name"]]["MDF"]
                    user_stat[user_id]["rpg"]["ch_monster_spd"] = \
                    monster_stat[user_stat[user_id]["rpg"]["monster_name"]]["SPD"]
                    user_stat[user_id]["rpg"]["rpg_trigger"]["magic_flag"] = 0
                    user_stat[user_id]["rpg"]["rpg_trigger"]["magic_flag_user"] = 0
                    user_stat[user_id]["rpg"]["rpg_trigger"]["mp_pass_user"] = 0
                    user_stat[user_id]["rpg"]["rpg_trigger"]["vt"] = 1
                    user_stat[user_id]["rpg"]["rpg_trigger"]["turn_system"] = 0
                    await message.channel.send("戦闘開始！\n**{0}**が現れた！".format(user_stat[user_id]["rpg"]["monster_name"]))
                    await message.channel.send("どうする？\n```{0}\n1.戦う\n2.特技\n3.魔法\n4.道具\n5.ステータス\n6.逃げる```"
                                               .format(message.author.name))
                    return

                if text == "6" and user_stat[user_id]["rpg"]["rpg_trigger"]["main"] == 1:
                    user_stat[user_id]["trigger"]["rpg"] = 0
                    user_stat[user_id]["rpg"]["rpg_trigger"]["main"] = 0
                    await message.channel.send("RPGモード解除。")
                    return

            if user_stat[user_id]["rpg"]["rpg_trigger"]["place_trigger"] == 1:
                if int(text) == len(place_enc["place"]) + 1:
                    user_stat[user_id]["rpg"]["rpg_trigger"]["place_trigger"] = 0
                    user_stat[user_id]["rpg"]["rpg_trigger"]["main"] = 1
                    await message.channel.send(main.format(message.author.name, user_stat[user_id]["rpg"]["place"]))
                    return

                if 0 < int(text) <= len(place_enc["place"]):
                    a = int(text) - 1
                    if user_stat[user_id]["rpg"]["place"] == place_enc["place"][a]:
                        await message.channel.send("あなたはそこにいます。")
                        return
                    user_stat[user_id]["rpg"]["place"] = place_enc["place"][a]
                    user_stat[user_id]["rpg"]["rpg_trigger"]["place_trigger"] = 2
                    user_stat[user_id]["rpg"]["distance"] = place_enc[user_stat[user_id]["rpg"]["place"]]["distance"]
                    await message.channel.send("{0}に移動します。\n距離:{1}\n1.歩く 2.調べる"
                                               .format(user_stat[user_id]["rpg"]["place"], user_stat[user_id]["rpg"]["distance"]))
                    return

            if user_stat[user_id]["rpg"]["rpg_trigger"]["place_trigger"] == 2:
                if text == "1":
                    user_stat[user_id]["rpg"]["distance"] = user_stat[user_id]["rpg"]["distance"] - 1
                    if user_stat[user_id]["rpg"]["distance"] == 0:
                        user_stat[user_id]["rpg"]["rpg_trigger"]["place_trigger"] = 0
                        user_stat[user_id]["rpg"]["rpg_trigger"]["main"] = 1
                        await message.channel.send("{0}に着きました。\n{1}".format(user_stat[user_id]["rpg"]["place"],
                                                                            main.format(message.author.name,
                                                                                        user_stat[user_id]["rpg"][
                                                                                            "place"])))
                        return

                    await message.channel.send("距離:{0}\n1.歩く 2.調べる"
                                               .format(user_stat[user_id]["rpg"]["distance"]))
                    return
                if text == "2":
                    await message.channel.send("何も見つからなかった。")
                    await message.channel.send("距離:{0}\n1.歩く 2.調べる"
                                               .format(user_stat[user_id]["rpg"]["distance"]))
                    return

            if user_stat[user_id]["rpg"]["rpg_trigger"]["item_trigger"] == 1:

                if int(text) == len(user_stat[user_id]["rpg"]["item_list"]) + 1:
                    user_stat[user_id]["rpg"]["rpg_trigger"]["item_trigger"] = 0
                    user_stat[user_id]["rpg"]["rpg_trigger"]["main"] = 1
                    await message.channel.send(main.format(message.author.name, user_stat[user_id]["rpg"]["place"]))
                    return

                if 0 < int(text) <= len(user_stat[user_id]["rpg"]["item_list"]):
                    a = int(text) - 1
                    await message.channel.send("**{0}**を使った！"
                                               .format(user_stat[user_id]["rpg"]["item_list"][a]))
                    use_item(a)
                    if user_stat[user_id]["rpg"]["rpg_trigger"]["re_hp"] == 1:
                        await message.channel.send("HPが**{0}**回復した！"
                                                   .format(user_stat[user_id]["rpg"]["vol_hp"]))
                        user_stat[user_id]["rpg"]["rpg_trigger"]["re_hp"] = 0
                        user_stat[user_id]["rpg"]["vol_hp"] = 0

                    if user_stat[user_id]["rpg"]["rpg_trigger"]["re_mp"] == 1:
                        await message.channel.send("MPが**{0}**回復した！"
                                                   .format(user_stat[user_id]["rpg"]["vol_mp"]))
                        user_stat[user_id]["rpg"]["rpg_trigger"]["re_mp"] = 0
                        user_stat[user_id]["rpg"]["vol_mp"] = 0

                    user_stat[user_id]["rpg"]["item"][user_stat[user_id]["rpg"]["item_list"][a]] = \
                        user_stat[user_id]["rpg"]["item"][user_stat[user_id]["rpg"]["item_list"][a]] - 1

                    if user_stat[user_id]["rpg"]["item"][user_stat[user_id]["rpg"]["item_list"][a]] == 0:
                        del user_stat[user_id]["rpg"]["item"][user_stat[user_id]["rpg"]["item_list"][a]]

                    user_stat[user_id]["rpg"]["rpg_trigger"]["item_trigger"] = 0
                    user_stat[user_id]["rpg"]["rpg_trigger"]["main"] = 1
                    await message.channel.send(main.format(message.author.name, user_stat[user_id]["rpg"]["place"]))
                    return

        if user_stat[user_id]["rpg"]["rpg_trigger"]["vt"] == 1:
            if user_stat[user_id]["rpg"]["ch_user_spd"] > user_stat[user_id]["rpg"]["ch_monster_spd"]:  # SED判定
                user_stat[user_id]["rpg"]["rpg_trigger"]["user_turn"] = 1
                user_stat[user_id]["rpg"]["rpg_trigger"]["monster_turn"] = 0

            else:
                user_stat[user_id]["rpg"]["rpg_trigger"]["monster_turn"] = 1
                user_stat[user_id]["rpg"]["rpg_trigger"]["user_turn"] = 0

            if text == "1":
                user_stat[user_id]["rpg"]["way_user"] = "normal_attack_user"
                user_stat[user_id]["rpg"]["rpg_trigger"]["turn_system"] = 1
                pass

            # if text == "4":
            #     user_stat[user_id]["rpg"]["rpg_trigger"]["item_trigger"] = 1
            #     i = 1
            #     for Item in user_stat[user_id]["rpg"]["item"]:
            #         user_stat[user_id]["rpg"]["item_list"].append("**{0}.{1}**".format(i, Item))
            #         i = i + 1
            #     user_stat[user_id]["rpg"]["item_list"] = map(str, user_stat[user_id]["rpg"]["item_list"])
            #     user_stat[user_id]["rpg"]["item_list"] = "\n".join(user_stat[user_id]["rpg"]["item_list"])
            #
            # if user_stat[user_id]["rpg"]["rpg_trigger"]["item_trigger"] == 1:
            #     if text in user_stat[user_id]["rpg"]["item"]:
            #         user_stat[user_id]["rpg"]["item_list"] = text
            #
            #         return
            #
            #     else:
            #         await message.channel.send("しかしそのアイテムは持っていない！")
            #         return

            if text == "5":
                await message.channel.send(
                    "Lv:{0}\nHP:{1}/{2} MP:{3}/{4}\nSTR:{5}/{6} DEF:{7}/{8}\nMSR:{9}/{10} MDF:{11}/{12}\n"
                    "SPD:{13}/{14}".format(
                        user_stat[user_id]["rpg"]["Lv"], user_stat[user_id]["rpg"]["ch_user_hp"],
                        user_stat[user_id]["rpg"]["HP"],
                        user_stat[user_id]["rpg"]["ch_user_mp"], user_stat[user_id]["rpg"]["MP"],
                        user_stat[user_id]["rpg"]["ch_user_str"], user_stat[user_id]["rpg"]["STR"],
                        user_stat[user_id]["rpg"]["ch_user_def"],user_stat[user_id]["rpg"]["DEF"],
                        user_stat[user_id]["rpg"]["ch_user_msr"], user_stat[user_id]["rpg"]["MSR"],
                        user_stat[user_id]["rpg"]["ch_user_mdf"], user_stat[user_id]["rpg"]["MDF"],
                        user_stat[user_id]["rpg"]["ch_user_spd"], user_stat[user_id]["rpg"]["SPD"],))
                await message.channel.send("どうする？\n```{0}\n1.戦う\n2.特技\n3.魔法\n4.道具\n5.ステータス\n6.逃げる```"
                                           .format(message.author.name))
                return

            if text == "6":
                if user_stat[user_id]["rpg"]["rpg_trigger"]["user_turn"] == 1:
                    await message.channel.send("**逃げ切れた！**")
                    user_stat[user_id]["rpg"]["rpg_trigger"]["vt"] = 0
                    user_stat[user_id]["rpg"]["rpg_trigger"]["turn_system"] = 0
                    user_stat[user_id]["rpg"]["rpg_trigger"]["user_turn"] = 0
                    user_stat[user_id]["rpg"]["rpg_trigger"]["monster_turn"] = 0

                    if user_stat[user_id]["rpg"]["rpg_trigger"]["distance_trigger"] == 2:
                        user_stat[user_id]["rpg"]["rpg_trigger"]["distance_trigger"] = 1
                        await message.channel.send("1.歩く 2.調べる")
                        return

                    else:
                        user_stat[user_id]["rpg"]["rpg_trigger"]["main"] = 1
                        await message.channel.send(main.format(message.author.name,
                                                               user_stat[user_id]["rpg"]["place"]))
                        return

                elif user_stat[user_id]["rpg"]["rpg_trigger"]["monster_turn"] == 1:
                    await message.channel.send("しかし回り込まれてしまった！")
                    user_stat[user_id]["rpg"]["rpg_trigger"]["turn_system"] = 2

            if text == "7":
                await message.channel.send("デバッグ用")
                user_stat[user_id]["rpg"]["rpg_trigger"]["user_turn"] = 0
                user_stat[user_id]["rpg"]["rpg_trigger"]["monster_turn"] = 1
                user_stat[user_id]["rpg"]["rpg_trigger"]["turn_system"] = 2

        if user_stat[user_id]["rpg"]["rpg_trigger"]["turn_system"] > 0:
            await message.channel.send(battle_system())
            if user_stat[user_id]["rpg"]["rpg_trigger"]["vt"] == 2:
                user_stat[user_id]["rpg"]["rpg_trigger"]["vt"] = 0
                if user_stat[user_id]["rpg"]["rpg_trigger"]["place_trigger"] == 0:
                    user_stat[user_id]["rpg"]["rpg_trigger"]["main"] = 1
                    await message.channel.send(main.format(message.author.name, user_stat[user_id]["rpg"]["place"]))
            else:
                await message.channel.send("どうする？\n```{0}\n1.戦う\n2.特技\n3.魔法\n4.道具\n5.ステータス\n6.逃げる```"
                                           .format(message.author.name))
                return


@client.event
async def on_reaction_add(reaction, user):
    global user_id_reaction
    user_id_reaction = str(user.id)
    message = reaction.message
    message_id_reaction = str(message.id)
    if message_id_reaction not in emoji_user[user_id_reaction]:
        emoji_user[user_id_reaction][message_id_reaction] = reaction.emoji
        print("bbb")

    else:
        await message.remove_reaction(emoji_user[user_id_reaction][message_id_reaction], user)
        emoji_user[user_id_reaction][message_id_reaction] = reaction.emoji
        print("ccc")

@client.event
async def on_reaction_remove(reaction, user):
    global user_id_reaction
    user_id_reaction = str(user.id)
    message = reaction.message
    message_id_reaction = str(message.id)
    if emoji_user[user_id_reaction][message_id_reaction] == reaction.emoji:
        del emoji_user[user_id_reaction][message_id_reaction]
        print("ddd")

with open('C:/Users/st158/OneDrive/ドキュメント/Python Scripts/Token.json', 'r', encoding='utf-8') as f:
    bot_token = json.load(f)
    client.run(bot_token["Botton"]["token"])