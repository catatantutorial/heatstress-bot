from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

TOKEN = os.getenv("TOKEN") 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bot Heat Stress Broiler Aktif\n\n"
        "Format:\n"
        "/cek umur suhu rh angin\n\n"
        "Contoh:\n"
        "/cek 28 31 75 2.5"
    )

async def cek(update: Update, context: ContextTypes.DEFAULT_TYPE):

    umur = int(context.args[0])
    suhu = float(context.args[1])
    rh = float(context.args[2])
    angin = float(context.args[3])

    thi = suhu - ((0.55 - (0.55 * rh / 100)) * (suhu - 14.5))
    suhu_efektif = suhu - (1.2 * angin)

    if suhu_efektif < 25:
        status = "✅ Nyaman"
    elif suhu_efektif < 28:
        status = "⚠️ Heat Stress Ringan"
    elif suhu_efektif < 30:
        status = "⚠️ Heat Stress Sedang"
    else:
        status = "🚨 Heat Stress Berat"

    pesan = f"""
🐔 HASIL ANALISIS

Umur : {umur} hari
Suhu : {suhu} °C
RH : {rh} %
Angin : {angin} m/s

THI : {thi:.1f}
Suhu Efektif : {suhu_efektif:.1f} °C

Status :
{status}
"""

    await update.message.reply_text(pesan)

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("cek", cek))

print("Bot Aktif...")
app.run_polling()
