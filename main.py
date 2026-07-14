import asyncio
import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.constants import ChatType
from telegram.error import RetryAfter, TimedOut, NetworkError
import logging
import re
import random

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.WARNING
)

OWNER_ID = int(os.getenv("OWNER_ID", "30340766"))
BOT_TOKENS = [8653123838:AAHUY-_sL7SOHOfHfab_vNSkYwxyFoujDVg
    os.getenv("BOT_TOKEN_1", ""),
    os.getenv("BOT_TOKEN_2", ""),
    os.getenv("BOT_TOKEN_3", ""),
    os.getenv("BOT_TOKEN_4", ""),
    os.getenv("BOT_TOKEN_5", ""),
    os.getenv("BOT_TOKEN_6", ""),
    os.getenv("BOT_TOKEN_7", ""),
]

BOT_TOKENS = [t for t in BOT_TOKENS if t]

if not BOT_TOKENS:
    print("ERROR: No bot tokens found! Set BOT_TOKEN_1, BOT_TOKEN_2, etc. environment variables")
    exit(1)

HEART_EMOJIS = ['❤️', '🧡', '💛', '💚', '💙', '💜', '🤎', '🖤', '🤍', '💘', '💝', '💖', '💗', '💓', '💞', '💌', '💕', '💟', '♥️', '❣️', '💔']

UNAUTHORIZED_MESSAGE = "𝐑𝐊_𝐑𝐀𝐉𝐀_𝐇𝐄𝐑𝐄 𝐁𝐀𝐁𝐘🎀😻"

NAME_CHANGE_MESSAGES = [
    "RK_RAJA_XWD _HERE🔥⃤⃟⃝🐦‍🔥『🚩』",
    "{target} TERI BHEN KA BHOSADA 🔥⃤⃟⃝🐦‍🔥『🚩』",
    "{target} TERI MAA DEV KE LUND PR 🔥⃤⃟⃝🐦‍🔥『🚩』",
    "{target} TERI MAA KA BHOSADA CHUDA 🔥⃤⃟⃝🐦‍🔥『🚩』",
    "{target} TERI CHUDAYI BY DEV PAPA 🔥⃤⃟⃝🐦‍🔥『🚩』",
    "{target} CVR LE RANDI KE BACCHE 🔥⃤⃟⃝🐦‍🔥『🚩』",
    "{target} TERI MAA RANDI 🔥⃤⃟⃝🐦‍🔥 『🚩』",
    "{target} TERI BHEN KAALI CHUT 🔥⃤⃟⃝🐦‍🔥『🚩』",
]

REPLY_MESSAGES = [
    "{target} ---RDI🐣",
    "{target} चुद गया -!",
    "Aʟᴏᴏ Kʜᴀᴋᴇ {target} Kɪ Mᴀ Cʜᴏᴅ Dᴜɴɢᴀ!",
    "{target} Cʜᴜᴅᴀ🦖🪽",
    "{target} Bᴏʟᴇ ᴅᴇᴠ ᴘᴀᴘᴀ पिताश्री Mᴇʀɪ Mᴀ Cʜᴏᴅ Dᴏ",
    "{target} Kɪ Mᴀ Bᴏʟᴇ ᴅᴇᴠ ᴘᴀᴘᴀ Sᴇ Cʜᴜᴅᴜɴɢɪ",
    "{target} Kɪ Bᴇʜɴ Kɪ Cʜᴜᴛ Kᴀʟɪ Kᴀʟɪ",
    "{target} Kɪ Mᴀ Rᴀɴᴅɪ",
    "{target} ɢᴀʀᴇᴇʙ ᴋᴀ ʙᴀᴄʜʜᴀ",
    "{target} ᴄʜᴜᴅ ᴋᴇ ᴘᴀɢᴀʟ ʜᴏɢᴀʏᴀ",
    "{target} ᴋɪ ʙᴇʜɴ ᴄʜᴏᴅᴜ",
    "{target} ʟᴜɴᴅ ᴄʜᴜsᴇɢᴀ sᴀʙᴋᴀ",
    "{target} ᴋɪ ᴍᴀ ᴋᴏ ᴄʜᴏᴅᴇ ᴅᴇᴠ ᴘᴀᴘᴀ",
    "{target} ᴋɪ ᴍᴀ ᴅᴇᴠ ᴘᴀᴘᴀ ꜱᴇ ᴄʜᴜᴅᴇ",
    "{target} ᴅᴇᴠ ᴘᴀᴘᴀ ꜱᴇ ᴄʜᴜᴅᴀ",
    "{target} CUDKE MARGYA",
    "{target} ɴᴇ ᴅᴇᴠ ᴘᴀᴘᴀ ᴋᴏ ʙᴀᴀᴩ ʙɴᴀ ʟɪyᴀ",
    "{target} ʙᴏʟᴇ ᴅᴇᴠ ᴘᴀᴘᴀ ᴩᴀᴩᴀ",
    "{target} ᴋɪ ᴀᴍᴍᴀ ᴄʜᴜᴅɪ",
    "{target} ᴋᴜᴛᴛᴇ ɢᴜʟᴀᴍɪ ᴋʀ 😋",
]

SPAM_MESSAGE_TEMPLATE = """{target} ʀᴀɴᴅɪ-ᴋᴇ ᴩɪʟʟᴏ ᴋɪ ᴄʜᴜᴅᴀɪજ⁀➴જ⁀➴જ⁀➴: ̗̀ 👾😻🎀
{target} ʀᴀɴᴅɪ-ᴋᴇ ᴩɪʟʟᴏ ᴋɪ ᴄʜᴜᴅᴀɪજ⁀➴જ⁀➴જ⁀➴: ̗̀ 👾😻🎀
{target} ʀᴀɴᴅɪ-ᴋᴇ ᴩɪʟʟᴏ ᴋɪ ᴄʜᴜᴅᴀɪજ⁀➴જ⁀➴જ⁀➴: ̗̀ 👾😻🎀
{target} ʀᴀɴᴅɪ-ᴋᴇ ᴩɪʟʟᴏ ᴋɪ ᴄʜᴜᴅᴀɪજ⁀➴જ⁀➴જ⁀➴: ̗̀ 👾😻🎀
{target} ʀᴀɴᴅɪ-ᴋᴇ ᴩɪʟʟᴏ ᴋɪ ᴄʜᴜᴅᴀɪજ⁀➴જ⁀➴જ⁀➴: ̗̀ 👾😻🎀"""


def extract_retry_after(error_str):
    match = re.search(r'retry after (\d+)', error_str.lower())
    if match:
        return int(match.group(1))
    return None


class BotInstance:
    def __init__(self, bot_number, owner_id):
        self.bot_number = bot_number
        self.owner_id = owner_id
        self.active_spam_tasks = {}
        self.active_name_change_tasks = {}
        self.active_reply_tasks = {}
        self.active_reply_targets = {}
        self.pending_replies = {}
        self.chat_delays = {}
        self.chat_threads = {}
        self.locks = {}
    
    def get_lock(self, chat_id):
        if chat_id not in self.locks:
            self.locks[chat_id] = asyncio.Lock()
        return self.locks[chat_id]
    
    def is_owner(self, user_id):
        return user_id == self.owner_id
    
    async def check_owner(self, update):
        user_id = update.effective_user.id
        if not self.is_owner(user_id):
            try:
                await update.message.reply_text(UNAUTHORIZED_MESSAGE)
            except Exception:
                pass
            return False
        return True
    
    async def start(self, update, context):
        if not await self.check_owner(update):
            return
        
        help_text = f"""
𓆩 𝐁𝐎𝐓 {self.bot_number} 𓆪 - 𝐓𝐇𝐄 𝐆𝐑𝐄𝐀𝐓 𝐑𝐊_𝐑𝐀𝐉𝐀 𝐁𝐎𝐓 

𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬:
/target <name> - NC + SPAM together with threads!
/nc <name> - Name change LOOP (with threads)
/spam <target> - Spam LOOP (with threads)
/reply <target> - Reply to every message LOOP!

/delay <seconds> - Set delay (default: 0)
/threads <1-50> - Set threads for NC + SPAM

/stopnc - Stop name change loop
/stopspam - Stop spam loop
/stopreply - Stop reply loop
/stopall - Stop ALL loops

𝐓𝐡𝐫𝐞𝐚𝐝𝐬: 1-50 (𝐚𝐩𝐩𝐥𝐢𝐞𝐬 𝐭𝐨 𝐍𝐂 + 𝐒𝐏𝐀𝐌)
𝐀𝐥𝐥 𝐚𝐜𝐭𝐢𝐨𝐧𝐬 𝐫𝐮𝐧 𝐢𝐧 𝐋𝐎𝐎𝐏𝐒 ⚡
𝐎𝐰𝐧𝐞𝐫 𝐎𝐧𝐥𝐲 🔒
"""
        await update.message.reply_text(help_text)

    async def name_change_loop(self, chat_id, base_name, context, worker_id=1):
        msg_index = 0
        num_messages = len(NAME_CHANGE_MESSAGES)
        success_count = 0
        print(f"[Bot {self.bot_number}] Name change LOOP #{worker_id} started for chat {chat_id}")
        try:
            while True:
                delay = self.chat_delays.get(chat_id, 0)
                try:
                    current_msg = NAME_CHANGE_MESSAGES[msg_index % num_messages]
                    display_name = current_msg.format(target=base_name)
                    await context.bot.set_chat_title(chat_id=chat_id, title=display_name)
                    msg_index += 1
                    success_count += 1
                    if delay > 0:
                        await asyncio.sleep(delay)
                except asyncio.CancelledError:
                    raise
                except RetryAfter as e:
                    wait_time = int(e.retry_after) if isinstance(e.retry_after, (int, float)) else e.retry_after.total_seconds()
                    await asyncio.sleep(wait_time + 0.1)
                except (TimedOut, NetworkError):
                    pass
                except Exception as e:
                    error_str = str(e).lower()
                    retry_after = extract_retry_after(error_str)
                    if retry_after:
                        await asyncio.sleep(retry_after)
                    msg_index += 1
        except asyncio.CancelledError:
            print(f"[Bot {self.bot_number}] Name change LOOP #{worker_id} stopped after {success_count} changes")

    async def spam_loop(self, chat_id, target_name, context, worker_id):
        success_count = 0
        print(f"[Bot {self.bot_number}] Spam LOOP #{worker_id} started for chat {chat_id}")
        try:
            while True:
                delay = self.chat_delays.get(chat_id, 0)
                try:
                    spam_msg = SPAM_MESSAGE_TEMPLATE.format(target=target_name)
                    await context.bot.send_message(chat_id=chat_id, text=spam_msg)
                    success_count += 1
                    if delay > 0:
                        await asyncio.sleep(delay)
                except asyncio.CancelledError:
                    raise
                except RetryAfter as e:
                    wait_time = int(e.retry_after) if isinstance(e.retry_after, (int, float)) else e.retry_after.total_seconds()
                    await asyncio.sleep(wait_time + 0.1)
                except (TimedOut, NetworkError):
                    pass
                except Exception as e:
                    error_str = str(e).lower()
                    retry_after = extract_retry_after(error_str)
                    if retry_after:
                        await asyncio.sleep(retry_after)
        except asyncio.CancelledError:
            print(f"[Bot {self.bot_number}] Spam LOOP #{worker_id} stopped after {success_count} messages")

    async def reply_loop(self, chat_id, target_name, context):
        success_count = 0
        print(f"[Bot {self.bot_number}] Reply LOOP started for chat {chat_id}")
        try:
            while True:
                delay = self.chat_delays.get(chat_id, 0)
                if chat_id in self.pending_replies and self.pending_replies[chat_id]:
                    async with self.get_lock(chat_id):
                        messages_to_reply = self.pending_replies[chat_id].copy()
                        self.pending_replies[chat_id] = []
                    
                    for msg_id in messages_to_reply:
                        try:
                            reply_msg = random.choice(REPLY_MESSAGES).format(target=target_name)
                            await context.bot.send_message(
                                chat_id=chat_id, 
                                text=reply_msg,
                                reply_to_message_id=msg_id
                            )
                            success_count += 1
                            if delay > 0:
                                await asyncio.sleep(delay)
                        except asyncio.CancelledError:
                            raise
                        except RetryAfter as e:
                            wait_time = int(e.retry_after) if isinstance(e.retry_after, (int, float)) else e.retry_after.total_seconds()
                            await asyncio.sleep(wait_time + 0.1)
                        except Exception:
                            pass
                else:
                    await asyncio.sleep(0.01)
        except asyncio.CancelledError:
            print(f"[Bot {self.bot_number}] Reply LOOP stopped after {success_count} replies")

    async def message_collector(self, update, context):
        if not update.message:
            return
        
        chat_id = update.effective_chat.id
        
        if chat_id in self.active_reply_targets:
            msg_id = update.message.message_id
            async with self.get_lock(chat_id):
                if chat_id not in self.pending_replies:
                    self.pending_replies[chat_id] = []
                self.pending_replies[chat_id].append(msg_id)

    async def nc_command(self, update, context):
        if not await self.check_owner(update):
            return
        
        chat = update.effective_chat
        
        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return
        
        if not context.args:
            await update.message.reply_text("Usage: /nc <name>")
            return
        
        base_name = " ".join(context.args)
        chat_id = chat.id
        
        if chat_id in self.active_name_change_tasks:
            old_tasks = self.active_name_change_tasks[chat_id]
            for task in old_tasks:
                task.cancel()
            for task in old_tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass
        
        num_threads = self.chat_threads.get(chat_id, 1)
        tasks = []
        for i in range(num_threads):
            task = asyncio.create_task(self.name_change_loop(chat_id, base_name, context, i+1))
            tasks.append(task)
        
        self.active_name_change_tasks[chat_id] = tasks
        
        await update.message.reply_text(f"[Bot {self.bot_number}] ⚡ Name change LOOP started with {num_threads} threads!")

    async def stop_nc_command(self, update, context):
        if not await self.check_owner(update):
            return
        
        chat_id = update.effective_chat.id
        
        if chat_id in self.active_name_change_tasks:
            tasks = self.active_name_change_tasks[chat_id]
            for task in tasks:
                task.cancel()
            for task in tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            del self.active_name_change_tasks[chat_id]
            await update.message.reply_text(f"[Bot {self.bot_number}] Name change LOOP stopped!")
        else:
            await update.message.reply_text(f"[Bot {self.bot_number}] No active name change loop!")

    async def spam_command(self, update, context):
        if not await self.check_owner(update):
            return
        
        chat = update.effective_chat
        
        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return
        
        if not context.args:
            await update.message.reply_text("Usage: /spam <target>")
            return
        
        target_name = " ".join(context.args)
        chat_id = chat.id
        
        if chat_id in self.active_spam_tasks:
            tasks = self.active_spam_tasks[chat_id]
            for task in tasks:
                task.cancel()
            for task in tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass
        
        num_threads = self.chat_threads.get(chat_id, 1)
        tasks = []
        for i in range(num_threads):
            task = asyncio.create_task(self.spam_loop(chat_id, target_name, context, i+1))
            tasks.append(task)
        
        self.active_spam_tasks[chat_id] = tasks
        await update.message.reply_text(f"[Bot {self.bot_number}] 💣 Spam LOOP started with {num_threads} threads! Running continuously...")

    async def stop_spam_command(self, update, context):
        if not await self.check_owner(update):
            return
        
        chat_id = update.effective_chat.id
        
        if chat_id in self.active_spam_tasks:
            tasks = self.active_spam_tasks[chat_id]
            for task in tasks:
                task.cancel()
            for task in tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            del self.active_spam_tasks[chat_id]
            await update.message.reply_text(f"[Bot {self.bot_number}] Spam LOOP stopped!")
        else:
            await update.message.reply_text(f"[Bot {self.bot_number}] No active spam loop!")

    async def target_command(self, update, context):
        if not await self.check_owner(update):
            return
        
        chat = update.effective_chat
        
        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return
        
        if not context.args:
            await update.message.reply_text("Usage: /target <name>")
            return
        
        target_name = " ".join(context.args)
        chat_id = chat.id
        
        if chat_id in self.active_name_change_tasks:
            old_tasks = self.active_name_change_tasks[chat_id]
            for task in old_tasks:
                task.cancel()
            for task in old_tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass
        
        if chat_id in self.active_spam_tasks:
            tasks = self.active_spam_tasks[chat_id]
            for task in tasks:
                task.cancel()
            for task in tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass
        
        num_threads = self.chat_threads.get(chat_id, 1)
        
        nc_tasks = []
        for i in range(num_threads):
            task = asyncio.create_task(self.name_change_loop(chat_id, target_name, context, i+1))
            nc_tasks.append(task)
        self.active_name_change_tasks[chat_id] = nc_tasks
        
        spam_tasks = []
        for i in range(num_threads):
            task = asyncio.create_task(self.spam_loop(chat_id, target_name, context, i+1))
            spam_tasks.append(task)
        self.active_spam_tasks[chat_id] = spam_tasks
        
        total_threads = num_threads * 2
        await update.message.reply_text(f"[Bot {self.bot_number}] 🎯 TARGET MODE: NC ({num_threads}) + SPAM ({num_threads}) = {total_threads} threads running!")

    async def reply_command(self, update, context):
        if not await self.check_owner(update):
            return
        
        chat = update.effective_chat
        
        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return
        
        if not context.args:
            await update.message.reply_text("Usage: /reply <target>")
            return
        
        target_name = " ".join(context.args)
        chat_id = chat.id
        
        if chat_id in self.active_reply_tasks:
            old_task = self.active_reply_tasks[chat_id]
            old_task.cancel()
            try:
                await old_task
            except asyncio.CancelledError:
                pass
        
        self.active_reply_targets[chat_id] = target_name
        self.pending_replies[chat_id] = []
        
        task = asyncio.create_task(self.reply_loop(chat_id, target_name, context))
        self.active_reply_tasks[chat_id] = task
        
        await update.message.reply_text(f"[Bot {self.bot_number}] 💬 Reply LOOP activated! Replying to every message...")

    async def stop_reply_command(self, update, context):
        if not await self.check_owner(update):
            return
        
        chat_id = update.effective_chat.id
        
        if chat_id in self.active_reply_tasks:
            task = self.active_reply_tasks[chat_id]
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            del self.active_reply_tasks[chat_id]
        
        if chat_id in self.active_reply_targets:
            del self.active_reply_targets[chat_id]
        
        if chat_id in self.pending_replies:
            del self.pending_replies[chat_id]
        
        await update.message.reply_text(f"[Bot {self.bot_number}] Reply LOOP stopped!")

    async def delay_command(self, update, context):
        if not await self.check_owner(update):
            return
        
        if not context.args:
            await update.message.reply_text("Usage: /delay <seconds>")
            return
        
        try:
            delay = float(context.args[0])
            if delay < 0:
                await update.message.reply_text("Delay must be >= 0")
                return
            
            chat_id = update.effective_chat.id
            self.chat_delays[chat_id] = delay
            await update.message.reply_text(f"[Bot {self.bot_number}] Delay set to {delay}s (applies to all loops)")
        except ValueError:
            await update.message.reply_text("Invalid delay value!")

    async def threads_command(self, update, context):
        if not await self.check_owner(update):
            return
        
        if not context.args:
            await update.message.reply_text("Usage: /threads <number>")
            return
        
        try:
            threads = int(context.args[0])
            if threads < 1 or threads > 50:
                await update.message.reply_text("Threads must be between 1 and 50")
                return
            
            chat_id = update.effective_chat.id
            self.chat_threads[chat_id] = threads
            await update.message.reply_text(f"[Bot {self.bot_number}] Threads set to {threads} (applies to NC + SPAM)")
        except ValueError:
            await update.message.reply_text("Invalid threads value!")

    async def stop_all_command(self, update, context):
        if not await self.check_owner(update):
            return
        
        chat_id = update.effective_chat.id
        stopped = []
        
        if chat_id in self.active_name_change_tasks:
            tasks = self.active_name_change_tasks[chat_id]
            for task in tasks:
                task.cancel()
            for task in tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            del self.active_name_change_tasks[chat_id]
            stopped.append("name change loop")
        
        if chat_id in self.active_spam_tasks:
            tasks = self.active_spam_tasks[chat_id]
            for task in tasks:
                task.cancel()
            for task in tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            del self.active_spam_tasks[chat_id]
            stopped.append("spam loop")
        
        if chat_id in self.active_reply_tasks:
            task = self.active_reply_tasks[chat_id]
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            del self.active_reply_tasks[chat_id]
            stopped.append("reply loop")
        
        if chat_id in self.active_reply_targets:
            del self.active_reply_targets[chat_id]
        
        if chat_id in self.pending_replies:
            del self.pending_replies[chat_id]
        
        if stopped:
            await update.message.reply_text(f"[Bot {self.bot_number}] Stopped: {', '.join(stopped)}")
        else:
            await update.message.reply_text(f"[Bot {self.bot_number}] No active loops to stop!")


def create_bot_application(token, bot_number, owner_id):
    application = Application.builder().token(token).build()
    bot_instance = BotInstance(bot_number, owner_id)
    
    application.add_handler(CommandHandler("start", bot_instance.start))
    application.add_handler(CommandHandler("nc", bot_instance.nc_command))
    application.add_handler(CommandHandler("stopnc", bot_instance.stop_nc_command))
    application.add_handler(CommandHandler("spam", bot_instance.spam_command))
    application.add_handler(CommandHandler("stopspam", bot_instance.stop_spam_command))
    application.add_handler(CommandHandler("target", bot_instance.target_command))
    application.add_handler(CommandHandler("reply", bot_instance.reply_command))
    application.add_handler(CommandHandler("stopreply", bot_instance.stop_reply_command))
    application.add_handler(CommandHandler("delay", bot_instance.delay_command))
    application.add_handler(CommandHandler("threads", bot_instance.threads_command))
    application.add_handler(CommandHandler("stopall", bot_instance.stop_all_command))
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, bot_instance.message_collector))
    
    return application


async def run_bot(token, bot_number, owner_id):
    application = create_bot_application(token, bot_number, owner_id)
    
    try:
        await application.initialize()
        await application.start()
        if application.updater:
            await application.updater.start_polling(drop_pending_updates=True)
        print(f"Bot {bot_number} started successfully!")
        
        while True:
            await asyncio.sleep(3600)
    
    except Exception as e:
        print(f"Bot {bot_number} error: {e}")
    finally:
        try:
            if application.updater:
                await application.updater.stop()
            await application.stop()
            await application.shutdown()
        except Exception:
            pass


async def main():
    print(f"Starting {len(BOT_TOKENS)} bots for owner ID: {OWNER_ID}")
    print("All actions (name change, spam, reply) run in LOOPS!")
    
    tasks = []
    for i, token in enumerate(BOT_TOKENS, 1):
        task = asyncio.create_task(run_bot(token, i, OWNER_ID))
        tasks.append(task)
    
    try:
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        print("\nShutting down all bots...")
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBots stopped!")
