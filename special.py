async def test(message):
    text = message.content
    if text == "/test":
        await message.channel.send("test")
        return