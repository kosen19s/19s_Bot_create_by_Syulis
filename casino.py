async def janken(message, save_data, message_author_id):
    import random
    text = message.content
    user_stat = save_data
    user_id = message_author_id
    if text == "じゃんけん":
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
        win_bot = "\n勝ち申した。"
        win_user = "\n負け申した。"
        soso = "\nあーいこーで\n```ぐー\nちょき\nぱー```"
        bot_pon = random.choice(["ぐー", "ちょき", "ぱー"])

        if bot_pon == "ぐー":
            user_stat[user_id]["janken"]["bot_pon_number"] = 0

        elif bot_pon == "ちょき":
            user_stat[user_id]["janken"]["bot_pon_number"] = 1

        elif bot_pon == "ぱー":
            user_stat[user_id]["janken"]["bot_pon_number"] = 2

        await message.channel.send(bot_pon)

        if text == "ぐー":

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
        if user_stat[user_id]["janken"]["result"] == "win":
            user_stat[user_id]["casino"]["coin"] \
                = user_stat[user_id]["casino"]["coin"] + user_stat[user_id]["casino"]["cost"]
            user_stat[user_id]["janken"]["result_count"][0] = user_stat[user_id]["janken"]["result_count"][0] + 1

        elif user_stat[user_id]["janken"]["result"] == "lose":
            user_stat[user_id]["casino"]["coin"] = user_stat[user_id]["casino"]["coin"] - \
                                                   user_stat[user_id]["casino"]["cost"]
            user_stat[user_id]["janken"]["result_count"][1] = user_stat[user_id]["janken"]["result_count"][1] + 1

        await message.channel.send("coin:{0}\n{1}勝 {2}敗\n連戦？\n```する\nしない```"\
                .format(user_stat[user_id]["casino"]["coin"],
                user_stat[user_id]["janken"]["result_count"][0],
                user_stat[user_id]["janken"]["result_count"][1]))
        user_stat[user_id]["trigger"]["janken"] = 4
        return

    if user_stat[user_id]["trigger"]["janken"] == 4:

        if text == "する":
            await message.channel.send("あなたのcoin:{0}\n掛け金を入力してください。\n(掛け金は5以下)"\
                                       .format(user_stat[user_id]["casino"]["coin"]))
            user_stat[user_id]["trigger"]["janken"] = 1
            return

        elif text == "しない":
            user_stat[user_id]["trigger"]["janken"] = 0
            user_stat[user_id]["casino"]["cost"] = 0
            await message.channel.send("またね！")
            return

async def slot(message, save_data, message_author_id, emoji):
    import random
    text = message.content
    user_stat = save_data
    user_id = message_author_id
    if text == "/slot" and user_stat[user_id]["trigger"]["slot"] == 0:
        user_stat[user_id]["trigger"]["slot"] = 1
        await message.channel.send("coin：{0}\n何コインスロット？(1 or 5 or 100)"\
                                   .format(user_stat[user_id]["casino"]["coin"]))
        return

    if user_stat[user_id]["trigger"]["slot"] == 1:
        if text == "/cancel":
            user_stat[user_id]["trigger"]["slot"] = 0
            await message.channel.send("あなたはスロット屋を去った。")
            return
        user_stat[user_id]["casino"]["cost"] = 0
        if text == "1":
            user_stat[user_id]["casino"]["cost"] = 1

        elif text == "5":
            user_stat[user_id]["casino"]["cost"] = 5

        elif text == "100":
            user_stat[user_id]["casino"]["cost"] = 100

        else:
            await message.channel.send("((1 or 5 or 100))")
            return

        if user_stat[user_id]["casino"]["coin"] < user_stat[user_id]["casino"]["cost"]:
            await message.channel.send("コインが足りません。")
            return

        user_stat[user_id]["trigger"]["slot"] = 2

    if user_stat[user_id]["trigger"]["slot"] == 3:
        if text == "1":
            if user_stat[user_id]["casino"]["coin"] < user_stat[user_id]["casino"]["cost"]:
                await message.channel.send("コインが足りません。")
                return
            user_stat[user_id]["trigger"]["slot"] = 2

        if text == "2":
            user_stat[user_id]["trigger"]["slot"] = 0
            await message.channel.send("あなたはスロット屋を去った。")
            return

        if text == "3":
            user_stat[user_id]["trigger"]["slot"] = 1
            await message.channel.send("何コインスロット？(1 or 5 or 100)")
            return

    if user_stat[user_id]["trigger"]["slot"] == 2:
        user_stat[user_id]["trigger"]["slot"] = 3
        cost = user_stat[user_id]["casino"]["cost"]

        user_stat[user_id]["casino"]["coin"] = user_stat[user_id]["casino"]["coin"] \
                                               - cost
        result_slot = []
        for i in range(9):
            a = random.choice(emoji["slot"]["emoji"])
            result_slot.append(a)

        get = 0
        if result_slot[0] == result_slot[1] == result_slot[2]:
            get = get + cost * emoji["slot"][result_slot[0]]

        if result_slot[3] == result_slot[4] == result_slot[5]:
            get = get + cost * emoji["slot"][result_slot[3]]

        if result_slot[6] == result_slot[7] == result_slot[8]:
            get = get + cost * emoji["slot"][result_slot[6]]

        if result_slot[0] == result_slot[4] == result_slot[8]:
            get = get + cost * emoji["slot"][result_slot[0]]

        if result_slot[6] == result_slot[4] == result_slot[2]:
            get = get + cost * emoji["slot"][result_slot[6]]

        d = []
        d.append(("{0}{1}{2}\n"
                  "{3}{4}{5}\n"
                  "{6}{7}{8}"
                  .format(result_slot[0], result_slot[1], result_slot[2],
                          result_slot[3], result_slot[4], result_slot[5],
                          result_slot[6], result_slot[7], result_slot[8])))

        if get > 0:
            user_stat[user_id]["casino"]["coin"] = user_stat[user_id]["casino"]["coin"] + get
            d.append("{0}コイン獲得！".format(get))

        if get < 0:
            user_stat[user_id]["casino"]["coin"] = user_stat[user_id]["casino"]["coin"] + get
            d.append("{0}コインを失った！".format(abs(get)))
            if user_stat[user_id]["casino"]["coin"] < 0:
                user_stat[user_id]["casino"]["coin"] = 0
                d.append("今やあなたは一文無しだ！")

        d.append("coin：{0}\nもう一度？(番号)\n```1.はい\n2.いいえ\n3.台を変える```"
                 .format(user_stat[user_id]["casino"]["coin"]))
        d = map(str, d)
        d = "\n".join(d)
        await message.channel.send(d)
        return

async def exchange(message, save_data, message_author_id):
    text = message.content
    user_stat = save_data
    user_id = message_author_id
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
