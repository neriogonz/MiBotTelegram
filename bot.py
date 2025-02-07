import telebot
import requests
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# 🔹 Configurar las claves de API (Reemplázalas con tus valores reales)
TELEGRAM_TOKEN = "7698297231:AAFYCNpxACW7bHFvErdA5NVNGZqBsEdJb-E"
TOGETHER_AI_KEY = "d2da8540307f65c3738f26ac4d671b19f59a9b0fabcd6b9211f327ad88bd264e"  # API Key de Together AI

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# 🔹 Función para hacer consultas a Mistral 7B
def mistral_response(prompt):
    url = "https://api.together.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {TOGETHER_AI_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistralai/Mistral-7B-Instruct-v0.1",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 200
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response_data = response.json()
        return response_data["choices"][0]["message"]["content"]
    except Exception:
        return "😕 Ocurrió un error al procesar tu solicitud. Inténtalo más tarde."

# 🔹 Generar botones de opciones
def menu_principal():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    btn1 = KeyboardButton("🤖 ¿Qué es la Inteligencia Artificial?")
    btn2 = KeyboardButton("📚 ¿Cómo funciona el bot?")
    btn3 = KeyboardButton("💡 Consejos para usar IA")
    btn4 = KeyboardButton("🚀 Probar la IA con una pregunta")
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    return markup

# 🔹 Comando /start con botones interactivos
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 
                     "👋 ¡Hola! Soy **Nerio - Tu Aliado Inteligente 🚀**.\n\n"
                     "💡 Envíame cualquier pregunta y te responderé usando IA.\n\n"
                     "🔹 **Elige una opción para comenzar:**", 
                     reply_markup=menu_principal())

# 🔹 Comando /help
@bot.message_handler(commands=['help'])
def help_message(message):
    bot.reply_to(message, "📝 **Cómo usar Nerio - Tu Aliado Inteligente 🚀:**\n\n"
                          "💡 Simplemente elige una opción del menú o envíame una pregunta y te responderé con IA.\n\n"
                          "Ejemplos:\n"
                          "🔹 ¿Qué es la inteligencia artificial?\n"
                          "🔹 Dame 3 consejos para ser más productivo.\n"
                          "🔹 Explícame la teoría de la relatividad en términos simples.\n\n"
                          "🚀 ¡Pruébalo ahora!")

# 🔹 Comando /info
@bot.message_handler(commands=['info'])
def info_message(message):
    bot.reply_to(message, "🤖 **Sobre mí:**\n"
                          "Soy **Nerio - Tu Aliado Inteligente 🚀**, un bot de inteligencia artificial basado en **Mistral 7B**.\n\n"
                          "🧠 **Modelo:** Mistral 7B\n"
                          "📡 **Fuente:** Together AI\n"
                          "💡 **Gratis para uso público**\n\n"
                          "💬 Envíame cualquier pregunta y te responderé.")

# 🔹 Responder a los botones del menú
@bot.message_handler(func=lambda message: message.text in [
    "🤖 ¿Qué es la Inteligencia Artificial?",
    "📚 ¿Cómo funciona el bot?",
    "💡 Consejos para usar IA",
    "🚀 Probar la IA con una pregunta"
])
def handle_buttons(message):
    if message.text == "🤖 ¿Qué es la Inteligencia Artificial?":
        bot.send_message(message.chat.id, 
                         "🧠 **La Inteligencia Artificial (IA) es la capacidad de una máquina para imitar la inteligencia humana.**\n\n"
                         "Se usa en asistentes virtuales, reconocimiento facial, chatbots y mucho más. 🚀")
    elif message.text == "📚 ¿Cómo funciona el bot?":
        bot.send_message(message.chat.id, 
                         "🤖 **Este bot usa IA para responder preguntas en tiempo real.**\n\n"
                         "✅ **Usamos Mistral 7B**, un modelo avanzado de lenguaje.\n"
                         "✅ **Procesamos cada mensaje y generamos respuestas naturales.**")
    elif message.text == "💡 Consejos para usar IA":
        bot.send_message(message.chat.id, 
                         "💡 **Consejos para aprovechar la IA:**\n"
                         "🔹 Sé claro con tus preguntas.\n"
                         "🔹 Pide explicaciones paso a paso.\n"
                         "🔹 Usa la IA para aprender nuevas cosas. 🚀")
    elif message.text == "🚀 Probar la IA con una pregunta":
        bot.send_message(message.chat.id, "✍️ Escríbeme cualquier pregunta y te responderé con IA. 😊")

# 🔹 Manejo de mensajes normales (Modo conversación)
@bot.message_handler(func=lambda message: True)
def chat_with_mistral(message):
    response = mistral_response(message.text)
    bot.reply_to(message, response)

# 🔹 Mantener el bot activo
bot.polling()
