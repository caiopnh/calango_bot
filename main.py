import os, logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)
TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = int(os.environ["CHAT_ID"])
ARQUIVO = "palavras.txt"

def carregar_palavras():
    try:
        with open(ARQUIVO, 'r', encoding='utf-8') as f:
            return [l.strip().lower() for l in f if l.strip()]
    except:
        return []

def salvar_palavras(lista):
    with open(ARQUIVO, 'w', encoding='utf-8') as f:
        for p in lista:
            f.write(p + '\n')

palavras_chave = carregar_palavras()

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        nova = ' '.join(context.args).lower()
        if nova not in palavras_chave:
            palavras_chave.append(nova)
            salvar_palavras(palavras_chave)
            await update.message.reply_text(f'✅ "{nova}" adicionada.')
        else:
            await update.message.reply_text(f'⚠️ "{nova}" já estava.')
async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        it = ' '.join(context.args).lower()
        if it in palavras_chave:
            palavras_chave.remove(it)
            salvar_palavras(palavras_chave)
            await update.message.reply_text(f'🗑️ "{it}" removida.')
        else:
            await update.message.reply_text(f'❌ "{it}" não estava.')
async def lista(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if palavras_chave:
        await update.message.reply_text("📋 Lista:\n• " + "\n• ".join(palavras_chave))
    else:
        await update.message.reply_text("📭 Lista vazia.")

async def filtrar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != CHAT_ID or not update.message.text:
        return
    txt = update.message.text.lower()
    if any(p in txt for p in palavras_chave):
        await context.bot.send_message(chat_id=CHAT_ID, text=f'🔎 Promoção:\n{update.message.text}')

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    handlers = [CommandHandler("add", add), CommandHandler("remove", remove),
                CommandHandler("lista", lista), MessageHandler(filters.TEXT & (~filters.COMMAND), filtrar)]
    for h in handlers:
        app.add_handler(h)
    logging.info("🤖 CalangoBot no grau!")
    app.run_polling()
