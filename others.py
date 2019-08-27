async def greet(message):
    import re
    text = message.content
    if re.search("おは", text):
        await message.channel.send("おはようございます" + message.author.name + "さん！")

    elif re.search("こんに", text):
        await message.channel.send("こんにちは" + message.author.name + "さん！")

    elif re.search("こんば", text):
        await message.channel.send("こんばんは" + message.author.name + "さん！")

    elif "振られ" or "ふられ" or "フラれ" in text:
        await message.channel.send("そういう時もあります！\n次頑張りましょう！\n")

    return