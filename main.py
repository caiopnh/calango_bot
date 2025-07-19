import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = int(os.environ["CHAT_ID"])
ARQUIVO = "palavras.txt"

# 🔄 Auxiliares
def carregar_palavras():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, 'r', encoding='utf-8') as f:
        return [linha.strip().lower() for linha in f if linha.strip()]

def salvar_palavras(lista):
    with open(ARQUIVO, 'w', encoding='utf-8') as f:
        for palavra in lista:
            f.write(palavra + '\n')

palavras_chave = carregar_palavras()

# ✅ Comandos
async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        nova = ' '.join(context.args).lower()
        if nova not in palavras_chave:
            palavras_chave.append(nova)
            salvar_palavras(palavras_chave)
            await update.message.reply_text(f'✅ "{nova}" adicionada à lista.')
        else:
            await update.message.reply_text(f'⚠️ "{nova}" já está na lista.')

async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        item = ' '.join(context.args).lower()
        if item in palavras_chave:
            palavras_chave.remove(item)
            salvar_palavras(palavras_chave)
            await update.message.reply_text(f'🗑️ "{item}" removida da lista.')
        else:
            await update.message.reply_text(f'❌ "{item}" não está na lista.')

async def lista(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if palavras_chave:
        texto = '\n• ' + '\n• '.join(palavras_chave)
        await update.message.reply_text(f'📋 Lista de palavras:{texto}')
    else:
        await update.message.reply_text('📭 Lista está vazia.')

# 🔎 Filtro automático
async def filtrar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != CHAT_ID:
        return
    texto = update.message.text.lower()
    if any(p in texto for p in palavras_chave):
        await context.bot.send_message(chat_id=CHAT_ID, text=f'🔎 Promoção encontrada:\n\n{update.message.text}')

# ▶️ Bot start
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("remove", remove))
    app.add_handler(CommandHandler("lista", lista))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), filtrar))
    print("🤖 CalangoBot tá no grau!")
    app.run_polling()
