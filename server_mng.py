async def set_server(message, save_data, message_author_id):
    import json
    text = message.content
    user_stat = save_data
    user_id = message_author_id
    try:
        if not user_stat[user_id]["trigger"]["data"] == 0:
            pass

    except:
        user_stat[user_id] = starter.copy()
        pass

    finally:
        # 初期設定
        if text == "/set.server":

            if message.author.guild_permissions.administrator:

                for M in message.guild.members:
                    print(str(M) + "\n" + str(M.id))
                    user_stat[str(M.id)] = starter.copy()

                with open('user_stat.json', "w") as a:
                    json.dump(user_stat, a, indent=3)

                await message.channel.send("(ﾟ∀ﾟ)ｱﾋｬﾋｬﾋｬﾋｬﾋｬﾋｬ")

            else:
                await message.channel.send("サーバーの管理者が操作してください。")

            return

async def role_server(message, save_data):
    import json
    text = message.content
    user_stat = save_data
    if text == "/role.server":
        if message.author.guild_permissions.administrator:
            for M in message.guild.members:
                user_stat[str(M.id)]["official"]["一般役職"] = []
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

async def save(message, save_data):
    import json
    text = message.content
    user_stat = save_data
    if text == "/save":
        with open('user_stat.json', "w") as w:
            json.dump(user_stat, w, indent=3)
        await message.channel.send("セーブが完了しました。")
        return

async def save_vote(message, vote_save_data):
    import json
    text = message.content
    vote_content = vote_save_data
    if text == "/save.vote":
        with open('vote.json', "w") as w:
            json.dump(vote_content, w, indent=3)
        await message.channel.send("投票のセーブが完了しました。")
        return

async def role(message, save_data, message_author_id, kosen):
    import discord
    text = message.content
    user_stat = save_data
    user_id = message_author_id

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

    if user_stat[user_id]["trigger"]["役職決め"] != 0 and text == "/cancel":
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
        await message.channel.send("最後に部活だね！\nロボコン\n"\
                    "プロコン\nと打ち込むとそれに応じた役職が付けられるよ！\n"\
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

        if text == "/finish" and user_stat[user_id]["trigger"]["役職決め"] == 5:
            for i in user_stat[user_id]["official"]["一般役職"]:
                d = discord.utils.get(message.guild.roles, name=i)
                await message.author.add_roles(d)
            await message.channel.send("お疲れ様でした！\nこれで役職設定は終了です！")
            user_stat[user_id]["trigger"]["役職決め"] = 0
            return

async def roles(message, save_data, message_author_id):
    import discord
    import json
    text = message.content
    user_stat = save_data
    user_id = message_author_id
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

async def reset(message, save_data, message_author_id):
    import discord
    import json
    text = message.content
    user_stat = save_data
    user_id = message_author_id
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

# 初期データ
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
            "薬草": 1
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
        "slot": 0,
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