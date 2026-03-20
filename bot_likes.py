import telebot
from telebot import types
import threading
import time
import requests
from black9 import EnC_AEs 
from byte import Auth_Chat

# --- الإعدادات ---
TOKEN = "8680591745:AAGo5QK7VB8md0h5k_vKW7ivhnHEMghwBn4"
ADMIN_ID = 6967812019
bot = telebot.TeleBot(TOKEN)

# متغيير لمتابعة حالة الهجوم
stats = {"success": 0, "total": 0}

def send_like_logic(acc_line, target_id):
    try:
        # هنا تضع كود تسجيل الدخول واللايك الخاص بك
        # نستخدم طلب POST للسيرفر كما في ملفاتك
        url = "https://client.ind.freefiremobile.com/social/like"
        # ... (تكملة منطق التشفير والارسال)
        time.sleep(0.1) # محاكاة وقت الطلب
        return True
    except:
        return False

def attack_manager(message, target_id, accounts):
    stats["success"] = 0
    stats["total"] = len(accounts)
    
    # رسالة البداية مع أزرار تعطل أثناء العمل
    sent_msg = bot.send_message(message.chat.id, f"<b>🚀 جاري بدء الهجوم على:</b> <code>{target_id}</code>\n<b>📊 التقدم:</b> 0/{stats['total']}", parse_mode="HTML")

    def run_attack():
        for i, acc in enumerate(accounts):
            if send_like_logic(acc, target_id):
                stats["success"] += 1
            
            # تحديث الرسالة كل 5 حسابات لتجنب حظر التلغرام (Flood)
            if (i + 1) % 5 == 0 or (i + 1) == stats["total"]:
                try:
                    bot.edit_message_text(
                        chat_id=message.chat.id,
                        message_id=sent_msg.message_id,
                        text=f"<b>⚡ هجوم لايكات قيد التنفيذ...</b>\n\n<b>🎯 الهدف:</b> <code>{target_id}</code>\n<b>📈 تم بنجاح:</b> {stats['success']}/{stats['total']}",
                        parse_mode="HTML"
                    )
                except: pass

        bot.send_message(message.chat.id, f"<b>✅ تم اكتمال الهجوم بنجاح!</b>\n<b>إجمالي اللايكات:</b> {stats['success']}", parse_mode="HTML")

    threading.Thread(target=run_attack).start()

# --- معالجة الأوامر ---

@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id != ADMIN_ID: return
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("🚀 إرسال لايكات", callback_data="setup_attack")
    btn2 = types.InlineKeyboardButton("📊 فحص الحسابات", callback_data="check_accs")
    markup.add(btn1, btn2)
    
    bot.send_message(message.chat.id, "<b>مرحباً بك RoMboo في لوحة التحكم 🛠️</b>", parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "setup_attack":
        msg = bot.send_message(call.message.chat.id, "<b>ارسل الآن الـ ID المراد تفجيره باللايكات:</b>", parse_mode="HTML")
        bot.register_next_step_handler(msg, process_id)

def process_id(message):
    target_id = message.text
    try:
        with open("accounts.txt", "r") as f:
            accounts = f.readlines()
        attack_manager(message, target_id, accounts)
    except FileNotFoundError:
        bot.reply_to(message, "❌ ملف الحسابات accounts.txt غير موجود")

print("Bot is running...")
bot.infinity_polling()
