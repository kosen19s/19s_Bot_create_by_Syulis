async def RPG(message, save_data, message_author_id, monster_stat, place_enc, weapon_stat, item_stat):
    import math
    import random
    main = " **メニュー**\n```{0}\n1.アイテム　　　2.ステータス\n3.装備　　　　　" \
           "4.フィールド移動\n5.エンカウント　6.RPGモード終了\nplace:{1}```"
    text = message.content
    user_stat = save_data
    user_id = message_author_id

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
                                                  + random.randint(
            weapon_stat[user_stat[user_id]["rpg"]["weapon"]]["mura"][0],
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

    def Medicinal_herb():
        user_stat[user_id]["rpg"]["rpg_trigger"]["re_hp"] = 1
        user_stat[user_id]["rpg"]["vol_hp"] = 10
        user_stat[user_id]["rpg"]["ch_user_hp"] = user_stat[user_id]["rpg"]["ch_user_hp"] + 10

        if user_stat[user_id]["rpg"]["ch_user_hp"] > user_stat[user_id]["rpg"]["HP"]:
            user_stat[user_id]["rpg"]["ch_user_hp"] = user_stat[user_id]["rpg"]["HP"]

        user_stat[user_id]["rpg"]["way_user_name"] = "薬草"

    def use_item(a):
        eval(item_stat[user_stat[user_id]["rpg"]["item_list"][a]]["name"])()

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
            user_stat[user_id]["rpg"]["STR"] = user_stat[user_id]["rpg"]["STR"] + user_stat[user_id]["rpg"][
                "up_str_user"]
            user_stat[user_id]["rpg"]["DEF"] = user_stat[user_id]["rpg"]["DEF"] + user_stat[user_id]["rpg"][
                "up_def_user"]
            user_stat[user_id]["rpg"]["MSR"] = user_stat[user_id]["rpg"]["MSR"] + user_stat[user_id]["rpg"][
                "up_msr_user"]
            user_stat[user_id]["rpg"]["MDF"] = user_stat[user_id]["rpg"]["MDF"] + user_stat[user_id]["rpg"][
                "up_mdf_user"]
            user_stat[user_id]["rpg"]["SPD"] = user_stat[user_id]["rpg"]["SPD"] + user_stat[user_id]["rpg"][
                "up_spd_user"]
            user_stat[user_id]["rpg"]["ch_user_hp"] = user_stat[user_id]["rpg"]["HP"]
            user_stat[user_id]["rpg"]["ch_user_mp"] = user_stat[user_id]["rpg"]["MP"]
            user_stat[user_id]["rpg"]["ch_user_str"] = user_stat[user_id]["rpg"]["STR"]
            user_stat[user_id]["rpg"]["ch_user_def"] = user_stat[user_id]["rpg"]["DEF"]
            user_stat[user_id]["rpg"]["ch_user_msr"] = user_stat[user_id]["rpg"]["MSR"]
            user_stat[user_id]["rpg"]["ch_user_mdf"] = user_stat[user_id]["rpg"]["MDF"]
            user_stat[user_id]["rpg"]["ch_user_spd"] = user_stat[user_id]["rpg"]["SPD"]
            user_stat[user_id]["rpg"]["rpg_trigger"]["Lv_up"] = 1

    def battle_system():  # 1ターンの処理
        # turn_system > 0で渡される予定
        d = []
        # ターン処理開始
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
                                         , user_stat[user_id]["rpg"]["monster_name"]
                                         , user_stat[user_id]["rpg"]["dm_mons_ac"]))
                    else:
                        if user_stat[user_id]["rpg"]["ch_user_mp"] > 0:
                            d.append("{0}！\n{1}に**{2}**のダメージを与えた！"
                                     .format(user_stat[user_id]["rpg"]["way_user_name"]
                                             , user_stat[user_id]["rpg"]["monster_name"]
                                             , user_stat[user_id]["rpg"]["dm_mons_ac"]))

                        else:
                            d.append("{0}の{1}！\nしかしMPが足りなかった！"
                                     .format(user_stat[user_id]["rpg"]["monster_name"],
                                             user_stat[user_id]["rpg"]["way_monster_name"], ))

                else:
                    d.append("{0}！\nしかし{1}にダメージを与えられなかった！"
                             .format(user_stat[user_id]["rpg"]["way_user_name"],
                                     user_stat[user_id]["rpg"]["monster_name"]))

                if user_stat[user_id]["rpg"]["ch_monster_hp"] > 0:  # モンスター生きてたら
                    user_stat[user_id]["rpg"]["rpg_trigger"]["turn_system"] = \
                        user_stat[user_id]["rpg"]["rpg_trigger"]["turn_system"] + 1

                else:  # モンスター死んでたら
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
                attack_monster()  # ユーザーダメージ蓄積
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

    if text == "/rpg" and user_stat[user_id]["trigger"]["rpg"] == 0:
            user_stat[user_id]["trigger"]["rpg"] = 1
            await message.channel.send("RPGモードです。")
            user_stat[user_id]["rpg"]["rpg_trigger"]["main"] = 1
            await message.channel.send(main.format(message.author.name, user_stat[user_id]["rpg"]["place"]))

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
                        user_stat[user_id]["rpg"]["Lv"], user_stat[user_id]["rpg"]["job"],
                        user_stat[user_id]["rpg"]["ch_user_hp"],
                        user_stat[user_id]["rpg"]["HP"], user_stat[user_id]["rpg"]["ch_user_mp"],
                        user_stat[user_id]["rpg"]["MP"],
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
                    user_stat[user_id]["rpg"]["ch_user_str"] - weapon_stat[user_stat[user_id]["rpg"]["weapon"]][
                        "STR_Plus"]
                # 変更処理を挟みたい
                user_stat[user_id]["rpg"]["ch_user_str"] = \
                    user_stat[user_id]["rpg"]["ch_user_str"] + weapon_stat[user_stat[user_id]["rpg"]["weapon"]][
                        "STR_Plus"]
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

                if user_stat[user_id]["rpg"]["place"] == "家" or user_stat[user_id]["rpg"]["place"] == "街":
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
                                           .format(user_stat[user_id]["rpg"]["place"],
                                                   user_stat[user_id]["rpg"]["distance"]))
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
                    user_stat[user_id]["rpg"]["ch_user_def"], user_stat[user_id]["rpg"]["DEF"],
                    user_stat[user_id]["rpg"]["ch_user_msr"], user_stat[user_id]["rpg"]["MSR"],
                    user_stat[user_id]["rpg"]["ch_user_mdf"], user_stat[user_id]["rpg"]["MDF"],
                    user_stat[user_id]["rpg"]["ch_user_spd"], user_stat[user_id]["rpg"]["SPD"], ))
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