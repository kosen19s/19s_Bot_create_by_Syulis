async def now(message):
    from datetime import datetime
    text = message.content
    if text == "/now":
        hour = datetime.now().strftime("%H")
        minute = datetime.now().strftime("%M")
        H = int(hour)

        if 3 <= H < 11:
            x = "おはようございます\n"

        elif 11 <= H < 18:
            x = "こんにちは\n"

        else:
            x = "こんばんは\n"

        await message.channel.send("{0}{1}:{2}です".format(x, hour, minute))
        return

async def timer(message):
    import asyncio
    import useful
    text = message.content
    if "/timer" in text:
        global wait
        global done
        mint = useful.find_text_start_from("m:", text)
        sec = useful.find_text_start_from("s:", text)
        MINT = int(mint)
        SEC = int(sec)

        if MINT >= 1 and 0 <= SEC <= 59:
            await message.channel.send("{0}分{1}秒のタイマーを開始しました。".format(mint, sec))

        elif MINT == 0 and 1 <= SEC <= 59:
            await message.channel.send("{0}秒のタイマーを開始しました。".format(sec))

        wait = 60 * MINT + SEC
        await asyncio.sleep(wait)

        if MINT == 0 and 0 <= SEC <= 59:
            await message.channel.send("{0}{1}秒経ちました！".format(f'{message.author.mention}\n', sec))

        else:
            await message.channel.send("{0}{1}分{2}秒経ちました！".format(f'{message.author.mention}\n', mint, sec))

        return