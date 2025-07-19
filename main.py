import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = int(os.environ["CHAT_ID"])
ARQUIVO = "palavras.txt"

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
            palavras_ch
