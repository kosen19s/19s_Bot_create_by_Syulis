async def help(message):
    text = message.content
    if text == "/help":
        with open('readme.txt', 'r') as a:
            d = a.read()
        await message.channel.send("```{0}```".format(d))
        return

async def logout(message, save_data, PASSCORD, client):
    import json
    import sys
    import useful
    text = message.content
    user_stat = save_data
    if message.author.id == 432897451209261057:
        if text == "/logout@home":
            print("パスコードを入力してください。")
            Passcord = input("Please Enter Passcord:")
            if Passcord == PASSCORD:
                with open('user_stat.json', "w") as f:
                    json.dump(user_stat, f, indent=3)
                await message.channel.send("I'll be back.")
                await client.logout()
                await sys.exit()

            else:
                await message.channel.send("パスコードが違います。")
                return

        if "/logout@outside" in text:
            Passcord = useful.find_text_start_from(":", text)
            if Passcord == PASSCORD:
                with open('user_stat.json', "w") as f:
                    json.dump(user_stat, f, indent=3)
                await message.channel.send("I'll be back.")
                await client.logout()
                await sys.exit()

            else:
                await message.channel.send("パスコードが違います。")
                return

async def search(message):
    import useful
    text = message.content
    if text.startswith("/search"):
        try:
            a = useful.find_text_start_from("/search", text)
            d = []
            for M in message.guild.members:
                for R in M.roles:
                    if a in R.name:
                        d.append(M.name)
            map(str, d)
            d = "\n".join(d)
            await message.channel.send(d)

        except:
            await message.channel.send("None")

async def vote(message, save_data, message_author_id, emoji, vote_content):
    import asyncio
    import useful
    text = message.content
    user_stat = save_data
    user_id = message_author_id
    if text == "/cancel" and user_stat[user_id]["trigger"]["ques"] > 0:
        user_stat[user_id]["trigger"]["ques"] = 0
        await message.channel.send("投票設定を中止しました。")
        return

    # 投票
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
        user_stat[user_id]["question"]["content"] \
            .append(text + emoji["emoji"][len(user_stat[user_id]["question"]["content"]) - 1])
        await message.channel.send("今の投票候補数：{0}"
                                   .format(len(user_stat[user_id]["question"]["content"]) - 1))
        return

    if user_stat[user_id]["trigger"]["ques"] == 3:
        if text.isdecimal() == 1:
            user_stat[user_id]["trigger"]["ques"] = user_stat[user_id]["trigger"]["ques"] + 1
            user_stat[user_id]["question"]["content"].append(text)
            await message.channel.send("何分？(半角英数)")
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
                result = useful.list_search(max(vote_content[str(msg.id)]["vote"]), d)
                await message.channel.send \
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

async def chat(message, save_data, message_author_id, free):
    import random
    text = message.content
    user_stat = save_data
    user_id = message_author_id
    if text == "/chat" and user_stat[user_id]["rpg"]["rpg_trigger"]["rpg"] \
            and user_stat[user_id]["trigger"]["janken"] == 0:

        if free == 0:
            free = 1
            await message.channel.send("喋ります！")
            return

        else:
            free = 0
            await message.channel.send("黙ります。")
            return

    if "/" in text and len(text) < 1:
        pass

    else:
        if free == 0 and user_stat[user_id]["trigger"]["rpg"] == 0:
            with open('History.txt', 'a') as a:
                a.write(text + "\n")

        elif free == 1:
            with open('History.txt', 'a') as f:
                f.write(text + "\n")
            with open('History.txt', 'r') as p:
                s = p.readlines()
                await message.channel.send(random.choice(s))
            return

async def gana(message, gana):
    text = message.content
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
