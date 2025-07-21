# 🔌 Flask para manter ativo no Render
from flask import Flask
import threading

app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return 'Bot rodando!'

threading.Thread(target=app_flask.run, kwargs={"host": "0.0.0.0", "port": 10000}).start()

# 🤖 Telegram Bot
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))
ARQUIVO = "palavras.txt"
palavras_chave = []

def carregar_palavras():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return [linha.strip().lower() for linha in f]
    return []

def salvar_palavras():
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        for palavra in palavras_chave:
            f.write(palavra + "\n")

# Comandos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 CalangoBot pronto no grau!")

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nova = " ".join(context.args).lower()
    if nova and nova not in palavras_chave:
        palavras_chave.append(nova)
        salvar_palavras()
        await update.message.reply_text(f"✅ Palavra '{nova}' adicionada.")
    else:
        await update.message.reply_text("⚠️ Palavra inválida ou já existe.")

async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    remover = " ".join(context.args).lower()
    if remover in palavras_chave:
        palavras_chave.remove(remover)
        salvar_palavras()
        await update.message.reply_text(f"🗑️ Palavra '{remover}' removida.")
    else:
        await update.message.reply_text("❌ Palavra não encontrada.")

async def lista(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if palavras_chave:
        await update.message.reply_text("📋 Palavras:\n• " + "\n• ".join(palavras_chave))
    else:
        await update.message.reply_text("📭 Lista está vazia.")

# 🔎 Filtro em mensagens normais
async def filtrar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower()
    if any(p in texto for p in palavras_chave):
        await context.bot.send_message(chat_id=CHAT_ID, text=f"📢 Promoção:\n\n{update.message.text}")

# 🔎 Filtro em posts de canal
async def filtrar_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.channel_post:
        texto = update.channel_post.text.lower()
        if any(p in texto for p in palavras_chave):
            await context.bot.send_message(chat_id=CHAT_ID, text=f"📢 Promoção:\n\n{texto}")

# ▶️ Start do Bot
if __name__ == "__main__":
    palavras_chave = carregar_palavras()
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("remove", remove))
    app.add_handler(CommandHandler("lista", lista))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, filtrar))
    app.add_handler(MessageHandler(filters.UpdateType.CHANNEL_POST, filtrar_post))

    print("🤖 CalangoBot no grau!")
    app.run_polling()
