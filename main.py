from telegram.ext import ApplicationBuilder

TOKEN = "seu_token_aqui"

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.run_polling()
