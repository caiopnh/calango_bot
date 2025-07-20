import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

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

def start(update, context):
    update.message.reply_text("🤖 Bot iniciado!")

def add(update, context):
    nova = " ".join(context.args).lower()
    if nova and nova not in palavras_chave:
        palavras_chave.append(nova)
        salvar_palavras()
        update.message.reply_text(f"✅ Palavra '{nova}' adicionada.")
    else:
        update.message.reply_text("⚠️ Palavra inválida ou já existe.")

def remove(update, context):
    remover = " ".join(context.args).lower()
    if remover in palavras_chave:
        palavras_chave.remove(remover)
        salvar_palavras()
        update.message.reply_text(f"🗑️ Palavra '{remover}' removida.")
    else:
        update.message.reply_text("❌ Palavra não encontrada.")

def lista(update, context):
    if palavras_chave:
        update.message.reply_text("📋 Palavras:\n• " + "\n• ".join(palavras_chave))
    else:
        update.message.reply_text("📭 Lista está vazia.")

def filtrar(update, context):
    texto = update.message.text.lower()
    if any(p in texto for p in palavras_chave):
        context.bot.send_message(chat_id=CHAT_ID, text=f"📢 Promoção:\n\n{update.message.text}")

if __name__ == '__main__':
    palavras_chave = carregar_palavras()

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("add", add))
    dp.add_handler(CommandHandler("remove", remove))
    dp.add_handler(CommandHandler("lista", lista))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, filtrar))

    updater.start_polling()
    updater.idle()
