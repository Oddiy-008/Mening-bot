import datetime
import json
import random
import urllib.request

# --- SOZLAMALAR ---
TOKEN = "9273806306:AAHC-HbWWp5hJbZXZssGYl-nk_TDNOCLGIg"  # O'z bot tokeningizni yozing
ADMIN_ID = 8824238939  # O'z Telegram ID raqamingizni yozing
CHANNEL_ID = "@Hammasi_Yaxshi_008"  # Kanal username"ingiz

# Tasdiqlashni kutayotgan vaqtinchalik ma'lumot
pending_content = {"type": "text", "content": "", "media": None}


def send_telegram(method, data):
  url = f"https://api.telegram.org/bot{TOKEN}/{method}"
  req = urllib.request.Request(
      url,
      data=json.dumps(data).encode("utf-8"),
      headers={"Content-Type": "application/json"},
  )
  try:
    with urllib.request.urlopen(req, timeout=10) as response:
      return json.loads(response.read().decode("utf-8"))
  except Exception as e:
    print(f"API xatoligi ({method}): {e}")
    return None


# Oddiy matnni chiroyli maxsus shriftga o'tkazish
def convert_to_fancy_font(text):
  normal = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
  fancy = "𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃𝓐𝓑𝓒𝘿𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩"
  trans = str.maketrans(normal, fancy)
  return text.translate(trans)


# Internetdan qayg'uli / motivatsion so'zlarni olish
def fetch_quote_from_internet():
  try:
    url = "https://api.quotable.io/random"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=5) as response:
      data = json.loads(response.read().decode("utf-8"))
      english_text = data.get("content", "Life is tough, but keep pushing forward.")
      return convert_to_fancy_font(english_text)
  except Exception:
    fallback = [
        "𝓢𝓲𝓷𝓸𝓿𝓵𝓪𝓻 𝓲𝓷𝓼𝓸𝓷𝓷𝓲 𝓬𝓱𝓲𝓭𝓪𝓶𝓵𝓲 𝓿𝓪 𝓴𝓾𝓬𝓱𝓵𝓲 𝓺𝓲𝓵𝓲𝓫 𝓽𝓪𝓻𝓫𝓲𝔂𝓪𝓵𝓪𝔂𝓭𝓲.",
        "𝓨𝓸𝓵𝓰'𝓲𝔃𝓵𝓲𝓴 𝓫𝓪𝔃𝓪𝓷 𝓸'𝔃𝓲𝓷𝓰𝓷𝓲 𝓽𝓸𝓹𝓲𝓼𝓱 𝓾𝓬𝓱𝓾𝓷 𝓮𝓷𝓰 𝔂𝓪𝔁𝓼𝓱𝓲 𝓯𝓾𝓻𝓼𝓪𝓽.",
        "𝓞'𝓽𝓶𝓲𝓼𝓱𝓷𝓲 𝓸'𝔃𝓰𝓪𝓻𝓽𝓲𝓻𝓲𝓫 𝓫𝓸'𝓵𝓶𝓪𝔂𝓭𝓲, 𝓪𝓶𝓶𝓸 𝓴𝓮𝓵𝓪𝓳𝓪𝓴 𝓱𝓪𝓵𝓲 𝓸'𝓃 𝓺𝓸'𝓵𝓲𝓷𝓰𝓭𝓪.",
    ]
    return random.choice(fallback)


# Vaqtga qarab tabrik tayyorlash
def get_time_greeting():
  now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5)))
  hour = now.hour
  if 5 <= hour < 12:
    return "𝓧𝓪𝔂𝓻𝓵𝓲 𝓽𝓸𝓷𝓰, 𝓺𝓪𝓭𝓻𝓵𝓲 𝓭𝓸'𝓼𝓽𝓲𝓶!"
  elif 12 <= hour < 18:
    return "𝓚𝓾𝓷𝓲𝓷𝓰𝓲𝔃 𝔃𝓪𝔂𝓻𝓵𝓲 𝓿𝓪 𝔃𝓪𝔃𝓶𝓾𝓷𝓵𝓲 𝓸'𝓽𝓼𝓲𝓷!"
  else:
    return "𝓧𝓪𝔂𝓻𝓵𝓲 𝓴𝓮𝓬𝓱, 𝓸𝓼𝓸𝔂𝓲𝓼𝓱𝓽𝓪𝓵𝓲𝓴 𝓽𝓲𝓵𝓪𝔂𝓶𝓪𝓷."


# Internetdan video havolasini olish
def get_internet_video():
  # Internetdagi ochiq va xavfsiz video namunalari havolalari
  sample_videos = [
      "https://www.w3schools.com/html/mov_bbb.mp4",
  ]
  return random.choice(sample_videos)


# Botni ishga tushirish va uzluksiz himoya
def run_bot():
  global pending_content
  offset = 0
  print("Bot muvaffaqiyatli ishga tushdi va himoyalandi!")
  while True:
    try:
      url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset={offset}&timeout=30"
      req = urllib.request.Request(url)
      with urllib.request.urlopen(req, timeout=35) as response:
        res = json.loads(response.read().decode("utf-8"))
        if res.get("ok"):
          for update in res.get("result", []):
            offset = update["update_id"] + 1

            # 1. Tugma bosilganda (Approve / Cancel)
            if "callback_query" in update:
              cq = update["callback_query"]
              cq_id = cq["id"]
              data = cq["data"]
              chat_id = cq["message"]["chat"]["id"]
              msg_id = cq["message"]["message_id"]

              if chat_id == ADMIN_ID:
                if data == "approve":
                  if pending_content["type"] == "text":
                    send_telegram(
                        "sendMessage",
                        {
                            "chat_id": CHANNEL_ID,
                            "text": pending_content["content"],
                            "parse_mode": "HTML",
                        },
                    )
                  elif pending_content["type"] == "video":
                    if pending_content.get("file_id"):
                      send_telegram(
                          "sendVideo",
                          {
                              "chat_id": CHANNEL_ID,
                              "video": pending_content["file_id"],
                              "caption": pending_content["content"],
                              "parse_mode": "HTML",
                          },
                      )
                    elif pending_content.get("video_url"):
                      send_telegram(
                          "sendVideo",
                          {
                              "chat_id": CHANNEL_ID,
                              "video": pending_content["video_url"],
                              "caption": pending_content["content"],
                              "parse_mode": "HTML",
                          },
                      )

                  send_telegram(
                      "answerCallbackQuery",
                      {
                          "callback_query_id": cq_id,
                          "text": "Kanalga muvaffaqiyatli tashlandi!",
                      },
                  )
                  send_telegram(
                      "editMessageText",
                      {
                          "chat_id": chat_id,
                          "message_id": msg_id,
                          "text": (
                              "✅ Ruxsat berildi! Kontent kanalga"
                              " chiqarildi."
                          ),
                      },
                  )
                elif data == "cancel":
                  send_telegram(
                      "answerCallbackQuery",
                      {
                          "callback_query_id": cq_id,
                          "text": "Rad etildi.",
                      },
                  )
                  send_telegram(
                      "editMessageText",
                      {
                          "chat_id": chat_id,
                          "message_id": msg_id,
                          "text": (
                              "❌ Rad etildi. Kanalga hech narsa tashlanmadi."
                          ),
                      },
                  )

            # 2. Xabar kelganda (Admin video tashlasa yoki /start yuborsa)
            elif "message" in update:
              msg = update["message"]
              chat_id = msg["chat"]["id"]

              if chat_id == ADMIN_ID:
                # Agar admin o'zi botga video tashlasa
                if "video" in msg:
                  file_id = msg["video"]["file_id"]
                  greeting = get_time_greeting()
                  quote = fetch_quote_from_internet()
                  full_text = f"{greeting}\n\n{quote}"

                  pending_content = {
                      "type": "video",
                      "content": full_text,
                      "file_id": file_id,
                  }

                  send_telegram(
                      "sendVideo",
                      {
                          "chat_id": ADMIN_ID,
                          "video": file_id,
                          "caption": (
                              "🎬 O'zingiz tashlagan video (Tasdiqlaysizmi?):\n\n"
                              + full_text
                          ),
                          "parse_mode": "HTML",
                          "reply_markup": {
                              "inline_keyboard": [
                                  [
                                      {
                                          "text": "✅ Ruxsat berish",
                                          "callback_data": "approve",
                                      },
                                      {
                                          "text": "❌ Rad etish",
                                          "callback_data": "cancel",
                                      },
                                  ]
                              ]
                          },
                      },
                  )

                # Agar admin matn yuborsa (masalan /start)
                elif "text" in msg:
                  text = msg["text"]
                  if text.startswith("/start"):
                    # Tasodifiy ravishda yo matn yoki internetdan video tanlaydi
                    choice = random.choice(["text", "internet_video"])
                    greeting = get_time_greeting()
                    quote = fetch_quote_from_internet()
                    full_text = f"{greeting}\n\n{quote}"

                    if choice == "text":
                      pending_content = {
                          "type": "text",
                          "content": full_text,
                      }
                      send_telegram(
                          "sendMessage",
                          {
                              "chat_id": ADMIN_ID,
                              "text": (
                                  "💬 Internetdan olingan matnli post"
                                  f" (Tasdiqlaysizmi?):\n\n{full_text}"
                              ),
                              "parse_mode": "HTML",
                              "reply_markup": {
                                  "inline_keyboard": [
                                      [
                                          {
                                              "text": "✅ Ruxsat berish",
                                              "callback_data": "approve",
                                          },
                                          {
                                              "text": "❌ Rad etish",
                                              "callback_data": "cancel",
                                          },
                                      ]
                                  ]
                              },
                          },
                      )
                    else:
                      vid_url = get_internet_video()
                      pending_content = {
                          "type": "video",
                          "content": full_text,
                          "video_url": vid_url,
                      }
                      send_telegram(
                          "sendVideo",
                          {
                              "chat_id": ADMIN_ID,
                              "video": vid_url,
                              "caption": (
                                  "🌐 Internetdan olingan video post"
                                  f" (Tasdiqlaysizmi?):\n\n{full_text}"
                              ),
                              "parse_mode": "HTML",
                              "reply_markup": {
                                  "inline_keyboard": [
                                      [
                                          {
                                              "text": "✅ Ruxsat berish",
                                              "callback_data": "approve",
                                          },
                                          {
                                              "text": "❌ Rad etish",
                                              "callback_data": "cancel",
                                          },
                                      ]
                                  ]
                              },
                          },
                      )
    except Exception as e:
      print(f"Xatolik yuz berdi: {e}")


if __name__ == "__main__":
  run_bot()

