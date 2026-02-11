from pyrogram.enums import ChatMemberStatus


async def is_group_admin(client, chat_id: int, user_id: int) -> bool:
    member = await client.get_chat_member(chat_id, user_id)
    return member.status in {ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR}


async def ensure_admin(client, msg) -> bool:
    if not msg.from_user:
        await msg.reply("❌ User context missing.")
        return False

    if await is_group_admin(client, msg.chat.id, msg.from_user.id):
        return True
    await msg.reply("❌ Admin only command.")
    return False
