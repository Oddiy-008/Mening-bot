import datetime
import json
import time
import urllib.request
import urllib.error
import ssl
import html

# SSL sertifikatini tekshirish
try:
    import certifi
    SSL_CONTEXT = ssl.create_default_context(
        cafile=certifi.where()
    )
except ImportError:
    SSL_CONTEXT = ssl.create_default_context()


# BOT SOZLAMALARI
TOKEN = "9273806306:AAHC-HbWWp5hJbZXZssGYl-nk_TDNOCLGIg"  # Bot tokenini shu yerga yoz
OWNER_ID = 8824238939
CHANNEL_ID = "@hammasi_yaxshi"

BASE_URL = f"https://api.telegram.org/bot{TOKEN}/"


# CHIROYLI SHRIFT
def beautiful_text(text):
    result = ""

    for char in text:
        if "A" <= char <= "Z":
            result += chr(ord(char) - ord("A") + 0x1D4D0)
        elif "a" <= char <= "z":
            result += chr(ord(char) - ord("a") + 0x1D4EA)
        else:
            result += char

    return result


# TELEGRAM BILAN ALOQA
def telegram(method, data):
    request = urllib.request.Request(
        BASE_URL + method,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    with urllib.request.urlopen(
        request,
        timeout=40,
        context=SSL_CONTEXT
    ) as response:
        result = json.loads(response.read().decode("utf-8"))

    if not result.get("ok"):
        raise Exception(result.get("description"))

    return result["result"]


# VAQTGA MOS SALOMLASHISH
def get_time_greeting():
    hour = datetime.datetime.now().hour

    if 5 <= hour < 12:
        text = "🌅 Xayrli tong! Kuningiz go'zal o'tsin!"
    elif 12 <= hour < 18:
        text = "☀️ Xayrli kun! Tushingiz xayrli o'tsin!"
    elif 18 <= hour < 23:
        text = "🌙 Xayrli kech! Kechangiz osoyishta o'tsin!"
    else:
        text = "🌌 Tun tinchligi hamroh bo'lsin!"

    return beautiful_text(text)


# KANALGA XABAR JOYLASH
def post_to_channel(text):
    greeting = get_time_greeting()
    styled_text = beautiful_text(text)

    message = (
        f"{html.escape(greeting)}\n\n"
        f"<b>{html.escape(styled_text)}</b>"
    )

    telegram("sendMessage", {
        "chat_id": CHANNEL_ID,
        "text": message,
        "parse_mode": "HTML"
    })


# BOT ISHI
def run_bot():
    offset = 0

    print("Bot muvaffaqiyatli ishga tushdi!")

    telegram("deleteWebhook", {
        "drop_pending_updates": False
    })

    while True:
        try:
            updates = telegram("getUpdates", {
                "offset": offset,
                "timeout": 30
            })

            for update in updates:
                offset = update["update_id"] + 1

                if "message" not in update:
                    continue

                msg = update["message"]

                # FAQAT KANAL EGASI
                if msg.get("from", {}).get("id") != OWNER_ID:
                    continue

                if "text" not in msg:
                    continue

                text = msg["text"].strip()

                if text == "/start":
                    telegram("sendMessage", {
                        "chat_id": OWNER_ID,
                        "text": beautiful_text(
                            "Bot tayyor! Istagan matningizni yuboring."
                        )
                    })
                    continue

                if text.startswith("/") or not text:
                    continue

                # KANALGA YUBORISH
                post_to_channel(text)

                telegram("sendMessage", {
                    "chat_id": OWNER_ID,
                    "text": beautiful_text(
                        "Xabaringiz kanalga joylandi!"
                    )
                })

        except urllib.error.HTTPError as e:
            if e.code == 409:
                print(
                    "409 xato: Bot boshqa joyda ham ishlayapti. "
                    "Boshqa nusxasini to'xtating."
                )
                time.sleep(30)
            else:
                print("HTTP xatolik:", e)
                time.sleep(5)

        except Exception as e:
            print("Xatolik:", e)
            time.sleep(5)


if __name__ == "__main__":
    if not TOKEN:
        print("Bot tokenini kiriting!")
    else:
        run_bot()
