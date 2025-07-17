import os
import threading
from flask import Flask
from telethon import TelegramClient, events

# 🔐 Dados da API (variáveis de ambiente)
api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
client = TelegramClient('minha_sessao', api_id, api_hash)

# 📁 Caminho do arquivo com as palavras-chave
ARQUIVO_PALAVRAS = 'palavras.txt'

# 🔄 Funções auxiliares
def carregar_palavras():
    if not os.path.exists(ARQUIVO_PALAVRAS):
        return []
    with open(ARQUIVO_PALAVRAS, 'r', encoding='utf-8') as f:
        return [linha.strip().lower() for linha in f if linha.strip()]

def salvar_palavras(lista):
    with open(ARQUIVO_PALAVRAS, 'w', encoding='utf-8') as f:
        for palavra in lista:
            f.write(palavra + '\n')

palavras_chave = carregar_palavras()

# 📡 Web server para UptimeRobot
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot está rodando! 🟢"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

threading.Thread(target=run_flask).start()

# 📨 ID do grupo/canal de destino
chat_destino = -4835304978 # substitua se precisar

# 📬 Mensagens recebidas
@client.on(events.NewMessage)
async def handler(event):
    global palavras_chave
    msg = event.message.message.strip()

    if msg.startswith('/add '):
        nova = msg[5:].lower()
        if nova not in palavras_chave:
            palavras_chave.append(nova)
            salvar_palavras(palavras_chave)
            await event.reply(f'✅ Produto "{nova}" adicionado na lista.')
        else:
            await event.reply(f'⚠️ O produto "{nova}" já está na lista.')

    elif msg.startswith('/remove '):
        remover = msg[8:].lower()
        if remover in palavras_chave:
            palavras_chave.remove(remover)
            salvar_palavras(palavras_chave)
            await event.reply(f'🗑️ Produto "{remover}" removido da lista.')
        else:
            await event.reply(f'❌ O produto "{remover}" não está na lista.')

    elif msg.startswith('/lista'):
        if palavras_chave:
            lista = '\n• ' + '\n• '.join(palavras_chave)
            await event.reply(f'📋 Produtos cadastrados:\n{lista}')
        else:
            await event.reply('📭 A lista está vazia.')

    else:
        texto = msg.lower()
        if any(p in texto for p in palavras_chave):
            print(f"🔎 Promoção encontrada em: {msg}")
            await event.message.forward_to(chat_destino)

# ▶️ Executar bot
with client:
    print("Bot rodando, ouvindo comandos e filtrando promoções...")
    client.run_until_disconnected()
