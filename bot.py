import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8721157106:AAFudCgf3l8_93ortZKgz7q1EWUknZlzl2o"

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send video and choose:\n/480p /720p /1080p")

# SAVE VIDEO
async def save_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.video.get_file()
    await file.download_to_drive("input.mp4")

    context.user_data["video"] = "input.mp4"
    await update.message.reply_text("✅ Video saved. Choose resolution")

# CHANGE RESOLUTION
def change_resolution(input_file, output_file, res):
    os.system(f"ffmpeg -i {input_file} -vf scale=-2:{res} {output_file}")

# PROCESS
async def process(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "video" not in context.user_data:
        await update.message.reply_text("❌ Send video first")
        return

    res = update.message.text.replace("/", "")
    output_file = f"output_{res}.mp4"

    await update.message.reply_text("⏳ Processing...")

    change_resolution("input.mp4", output_file, res)

    with open(output_file, "rb") as vid:
        await update.message.reply_video(video=vid)

# MAIN
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler(["480p", "720p", "1080p"], process))
app.add_handler(MessageHandler(filters.VIDEO, save_video))

app.run_polling()
