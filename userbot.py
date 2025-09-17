import asyncio
import logging
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
import os
import time
from datetime import datetime

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration - REPLACE WITH YOUR VALUES
API_ID = 'your_api_id_here'  # Get from my.telegram.org
API_HASH = 'your_api_hash_here'  # Get from my.telegram.org
PHONE_NUMBER = 'your_phone_number_here'  # Your phone number with country code
SESSION_NAME = 'userbot_session'

# Initialize the client
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# Global variables for userbot state
auto_reply_enabled = False
auto_reply_message = "I'm currently away. Will get back to you soon!"
command_prefix = "."

# Dictionary to store user-specific settings
user_settings = {}

async def main():
    """Main function to start the userbot"""
    try:
        # Start the client
        await client.start(phone=PHONE_NUMBER)
        
        # Get information about the logged-in user
        me = await client.get_me()
        logger.info(f"Userbot started successfully for {me.first_name} ({me.username})")
        print(f"✅ Userbot is running for: {me.first_name}")
        print(f"📱 Phone: {PHONE_NUMBER}")
        print(f"🆔 User ID: {me.id}")
        print("🔥 Type .help for available commands")
        
        # Keep the client running
        await client.run_until_disconnected()
        
    except Exception as e:
        logger.error(f"Error starting userbot: {e}")
        print(f"❌ Error: {e}")

# Command: Help
@client.on(events.NewMessage(pattern=r'\.help', outgoing=True))
async def help_command(event):
    """Display help message with available commands"""
    help_text = """
🤖 **USERBOT COMMANDS**

**💬 Messaging:**
`.ping` - Check bot response time
`.id` - Get chat/user ID
`.info` - Get chat information
`.count` - Count messages in chat

**🔄 Auto Features:**
`.autoreply on/off` - Toggle auto-reply
`.setreply <message>` - Set auto-reply message
`.afk <reason>` - Set AFK mode

**📁 Media:**
`.download` - Download replied media
`.upload <path>` - Upload file

**🛠 Utilities:**
`.spam <count> <message>` - Send message multiple times
`.del` - Delete replied message
`.edit <text>` - Edit your last message
`.purge` - Delete messages (reply to start)

**ℹ️ Info:**
`.stats` - Show userbot statistics
`.time` - Show current time
`.help` - Show this help menu

**⚠️ Note:** Use commands responsibly!
    """
    
    await event.edit(help_text)
    await asyncio.sleep(10)
    await event.delete()

# Command: Ping
@client.on(events.NewMessage(pattern=r'\.ping', outgoing=True))
async def ping_command(event):
    """Check response time"""
    start_time = time.time()
    msg = await event.edit("🏓 Pinging...")
    end_time = time.time()
    ping_time = (end_time - start_time) * 1000
    
    await msg.edit(f"🏓 **Pong!**\n⚡ Response time: `{ping_time:.2f}ms`")
    await asyncio.sleep(5)
    await msg.delete()

# Command: Get ID
@client.on(events.NewMessage(pattern=r'\.id', outgoing=True))
async def id_command(event):
    """Get chat/user ID"""
    chat = await event.get_chat()
    msg_text = f"🆔 **Chat ID:** `{chat.id}`"
    
    if event.is_reply:
        reply_msg = await event.get_reply_message()
        sender = await reply_msg.get_sender()
        msg_text += f"\n👤 **User ID:** `{sender.id}`"
        if hasattr(sender, 'username') and sender.username:
            msg_text += f"\n📝 **Username:** @{sender.username}"
    
    await event.edit(msg_text)
    await asyncio.sleep(8)
    await event.delete()

# Command: Chat Info
@client.on(events.NewMessage(pattern=r'\.info', outgoing=True))
async def info_command(event):
    """Get detailed chat information"""
    chat = await event.get_chat()
    
    info_text = f"📊 **Chat Information**\n\n"
    info_text += f"🆔 **ID:** `{chat.id}`\n"
    info_text += f"📝 **Title:** `{chat.title if hasattr(chat, 'title') else 'N/A'}`\n"
    info_text += f"👥 **Type:** `{type(chat).__name__}`\n"
    
    if hasattr(chat, 'participants_count'):
        info_text += f"👤 **Members:** `{chat.participants_count}`\n"
    
    if hasattr(chat, 'username') and chat.username:
        info_text += f"🔗 **Username:** @{chat.username}\n"
    
    await event.edit(info_text)
    await asyncio.sleep(10)
    await event.delete()

# Auto-reply feature
@client.on(events.NewMessage(incoming=True))
async def auto_reply_handler(event):
    """Handle auto-reply messages"""
    global auto_reply_enabled, auto_reply_message
    
    if auto_reply_enabled and event.is_private:
        sender = await event.get_sender()
        if not sender.bot:  # Don't reply to bots
            await asyncio.sleep(2)  # Add delay to seem natural
            await event.respond(auto_reply_message)
            logger.info(f"Auto-replied to {sender.first_name}")

# Command: Toggle Auto-reply
@client.on(events.NewMessage(pattern=r'\.autoreply (on|off)', outgoing=True))
async def toggle_autoreply(event):
    """Toggle auto-reply on/off"""
    global auto_reply_enabled
    
    action = event.pattern_match.group(1)
    if action == 'on':
        auto_reply_enabled = True
        await event.edit("✅ **Auto-reply enabled**")
    else:
        auto_reply_enabled = False
        await event.edit("❌ **Auto-reply disabled**")
    
    await asyncio.sleep(3)
    await event.delete()

# Command: Set Auto-reply Message
@client.on(events.NewMessage(pattern=r'\.setreply (.+)', outgoing=True))
async def set_autoreply_message(event):
    """Set custom auto-reply message"""
    global auto_reply_message
    
    auto_reply_message = event.pattern_match.group(1)
    await event.edit(f"✅ **Auto-reply message set to:**\n`{auto_reply_message}`")
    await asyncio.sleep(5)
    await event.delete()

# Command: AFK Mode
@client.on(events.NewMessage(pattern=r'\.afk(?: (.+))?', outgoing=True))
async def afk_command(event):
    """Set AFK mode with optional reason"""
    global auto_reply_enabled, auto_reply_message
    
    reason = event.pattern_match.group(1) or "I'm currently AFK"
    auto_reply_message = f"🔄 **AFK Mode**\n{reason}\n\n_Last seen: {datetime.now().strftime('%H:%M:%S')}_"
    auto_reply_enabled = True
    
    await event.edit("✅ **AFK mode activated**")
    await asyncio.sleep(3)
    await event.delete()

# Command: Spam Messages
@client.on(events.NewMessage(pattern=r'\.spam (\d+) (.+)', outgoing=True))
async def spam_command(event):
    """Send message multiple times"""
    try:
        count = int(event.pattern_match.group(1))
        message = event.pattern_match.group(2)
        
        if count > 20:  # Limit spam count
            await event.edit("⚠️ **Spam limit: 20 messages maximum**")
            return
        
        await event.delete()
        
        for i in range(count):
            await event.respond(message)
            await asyncio.sleep(1)  # Delay between messages
            
    except ValueError:
        await event.edit("❌ **Invalid format!** Use: `.spam <count> <message>`")

# Command: Delete Message
@client.on(events.NewMessage(pattern=r'\.del', outgoing=True))
async def delete_command(event):
    """Delete replied message"""
    if event.is_reply:
        reply_msg = await event.get_reply_message()
        await reply_msg.delete()
        await event.delete()
    else:
        await event.edit("❌ **Reply to a message to delete it**")
        await asyncio.sleep(3)
        await event.delete()

# Command: Edit Last Message
@client.on(events.NewMessage(pattern=r'\.edit (.+)', outgoing=True))
async def edit_command(event):
    """Edit your last message"""
    new_text = event.pattern_match.group(1)
    
    async for message in client.iter_messages(event.chat_id, from_user='me', limit=10):
        if message.id != event.id:
            try:
                await message.edit(new_text)
                await event.edit("✅ **Message edited successfully**")
                await asyncio.sleep(2)
                await event.delete()
                return
            except Exception as e:
                await event.edit(f"❌ **Error editing message:** `{str(e)}`")
                return
    
    await event.edit("❌ **No recent message found to edit**")

# Command: Download Media
@client.on(events.NewMessage(pattern=r'\.download', outgoing=True))
async def download_command(event):
    """Download replied media file"""
    if not event.is_reply:
        await event.edit("❌ **Reply to a media message to download**")
        return
    
    reply_msg = await event.get_reply_message()
    if not reply_msg.media:
        await event.edit("❌ **No media found in replied message**")
        return
    
    await event.edit("📥 **Downloading...**")
    
    try:
        # Create downloads directory
        if not os.path.exists('downloads'):
            os.makedirs('downloads')
        
        file_path = await reply_msg.download_media('downloads/')
        await event.edit(f"✅ **Downloaded successfully!**\n📁 **Path:** `{file_path}`")
        
    except Exception as e:
        await event.edit(f"❌ **Download failed:** `{str(e)}`")

# Command: Get Current Time
@client.on(events.NewMessage(pattern=r'\.time', outgoing=True))
async def time_command(event):
    """Display current time"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await event.edit(f"🕐 **Current Time:** `{current_time}`")
    await asyncio.sleep(5)
    await event.delete()

# Command: Count Messages
@client.on(events.NewMessage(pattern=r'\.count', outgoing=True))
async def count_command(event):
    """Count messages in current chat"""
    await event.edit("🔢 **Counting messages...**")
    
    try:
        count = 0
        async for message in client.iter_messages(event.chat_id):
            count += 1
            if count % 1000 == 0:  # Update every 1000 messages
                await event.edit(f"🔢 **Counting messages... {count}**")
        
        await event.edit(f"📊 **Total messages in this chat:** `{count}`")
        
    except Exception as e:
        await event.edit(f"❌ **Error counting messages:** `{str(e)}`")

# Command: Purge Messages
@client.on(events.NewMessage(pattern=r'\.purge', outgoing=True))
async def purge_command(event):
    """Delete messages from replied message to current"""
    if not event.is_reply:
        await event.edit("❌ **Reply to a message to start purging from**")
        return
    
    reply_msg = await event.get_reply_message()
    messages_to_delete = []
    
    async for message in client.iter_messages(event.chat_id, min_id=reply_msg.id - 1):
        if message.id >= reply_msg.id:
            messages_to_delete.append(message)
    
    await event.edit(f"🗑 **Deleting {len(messages_to_delete)} messages...**")
    
    try:
        await client.delete_messages(event.chat_id, messages_to_delete)
        # The purge command message will also be deleted
    except Exception as e:
        await event.edit(f"❌ **Error purging messages:** `{str(e)}`")

# Error handler
@client.on(events.NewMessage)
async def error_handler(event):
    """Handle any errors that occur"""
    try:
        # This is just a placeholder for error handling
        pass
    except Exception as e:
        logger.error(f"Unhandled error: {e}")

if __name__ == '__main__':
    print("🚀 Starting Telegram Userbot...")
    print("⚠️  Make sure to replace API_ID, API_HASH, and PHONE_NUMBER with your actual values!")
    print("📱 You'll need to enter the verification code sent to your phone.")
    
    try:
        # Run the userbot
        client.loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\n⏹ Userbot stopped by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
    finally:
        print("👋 Goodbye!")
