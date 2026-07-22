import subprocess
import telebot

# ⚠️ YAHAN APNI DETAILS BHREIN
BOT_TOKEN = "8852862302:AAEdrxcnG_MzP_KyCAB_UKwHvGtQ1BvnY7c"  # @BotFather se mila hua token
ADMIN_ID = 5638370016  # @userinfobot se mili hui aapki Telegram numeric ID

bot = telebot.TeleBot(BOT_TOKEN)


# /start aur /help command handler
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Aapke paas is bot ko use karne ki permission nahi hai.")
        return

    bot.reply_to(
        message,
        "👋 Welcome Admin!\n\nBash command run karne ke liye type karein: /run",
    )


# Jab user /run command bhejega, toh bot prompt karega
@bot.message_handler(commands=["run"])
def ask_for_command(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Access Denied.")
        return

    # Prompt message
    msg = bot.reply_to(message, "📝 Enter your bash command in your next Input:")

    # Agla input seedhe execute_command function ko bhejega
    bot.register_next_step_handler(msg, execute_command)


# Main function jo command execute karega
def execute_command(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Access Denied.")
        return

    command = message.text
    bot.reply_to(message, f"⏳ Executing: `{command}`...", parse_mode="Markdown")

    try:
        # Subprocess ka use karke command execute karna (30 seconds timeout ke sath)
        result = subprocess.run(
            command, shell=True, text=True, capture_output=True, timeout=30
        )

        output = result.stdout if result.stdout else ""
        error = result.stderr if result.stderr else ""

        response = ""
        if output:
            response += f"📤 Output:\n{output}\n"
        if error:
            response += f"⚠️ Error:\n{error}\n"
        if not response:
            response = "✅ Command executed successfully (No output)."

        # Telegram ki 4096 character limit handle karne ke liye
        if len(response) > 4000:
            bot.reply_to(message, response[:4000])
        else:
            bot.reply_to(message, response)

    except subprocess.TimeoutExpired:
        bot.reply_to(message, "❌ Error: Command execution timed out (30 seconds).")
    except Exception as e:
        bot.reply_to(message, f"❌ Unexpected Error: {str(e)}")


# Bot ko start karne ke liye
print("Bot is starting...")
bot.infinity_polling()
