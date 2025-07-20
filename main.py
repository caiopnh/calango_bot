import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID_ENV = os.getenv("CHAT_ID")
try:
    CHAT_ID = int(CHAT_ID_ENV) if CHAT_ID_ENV is not None else None
except ValueError:
    CHAT_ID = None

palavras_chave = []

ARQUIVO = "palavras.txt"

def carregar_palavras():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return [linha.strip().lower() for linha in f]
    return []

def salvar_palavras():
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        for palavra in palavras_chave:
            f.write(palavra + "\n")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot iniciado e pronto pra filtrar promoções!")

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nova = " ".join(context.args).lower()
    if nova and nova not in palavras_chave:
        palavras_chave.append(nova)
        salvar_palavras()
        await update.message.reply_text(f"✅ Palavra '{nova}' adicionada.")
    else:
        await update.message.reply_text("⚠️ Palavra inválida ou já existente.")

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
        texto = "\n• " + "\n• ".join(palavras_chave)
        await update.message.reply_text(f"📋 Palavras cadastradas:{texto}")
    else:
        await update.message.reply_text("📭 Lista está vazia.")

async def filtrar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower()
    if CHAT_ID is None:
        # Evitar erro caso CHAT_ID não esteja configurado
        return
    if any(p in texto for p in palavras_chave):
        await context.bot.send_message(chat_id=CHAT_ID, text=f"📢 Promoção:\n\n{update.message.text}")

if __name__ == '__main__':
    palavras_chave = carregar_palavras()

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("remove", remove))
    app.add_handler(CommandHandler("lista", lista))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, filtrar))

    app.run_polling()
