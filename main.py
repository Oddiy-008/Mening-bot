import datetime
import json
import random
import time
import urllib.request

# --- SOZLAMALAR ---
TOKEN = "9273806306:AAHC-HbWWp5hJbZXZssGY1-nk_TDNOCLGig"
ADMIN_ID = 8824238939
CHANNEL_ID = "@Hammasi_Yaxshi_008"

# 18+ yoshdagilar uchun chiroyli osoyishta va falsafiy videolar uchun matnli sarlavhalar
CALM_VIDEOS = [
    (
        "✨ Osoyishta va falsafiy parcha (18+): Ba'zida dunyoning shovqinidan"
        " qochib, faqat o'zing bilan qolish — eng buyuk huzurdir..."
    ),
    (
        "✨ Osoyishta va falsafiy parcha (18+): Haqiqiy go'zallik — bu qalbning"
        " tinchligi va o'ylantiradigan og'ir haqiqatlardir."
    ),
]

# 18+ yoshdagilar uchun kuchli motivatsion kino + anime videolari uchun matnli sarlavhalar
MOTIVATIONAL_VIDEOS = [
    (
        "🔥 Motivatsion Kino & Anime parcha (18+): Yiqilishdan qo'rqma! Asosiysi"
        " — har safar yiqilganda o'rningdan ikki barobar kuchli bo'lib turishdir."
    ),
    (
        "🔥 Motivatsion Kino & Anime parcha (18+): Hayot senga qarshi chiqqanda,"
        " sen unga o'z qoidalaringni o'tkazishni o'rgan."
    ),
]

# Vaqtinchalik xotira
pending_content = {"type": "text", "content": "", "media": None}
last_auto_story_day = ""


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
    print(f"Xatolik: {e}")
    return None


def format_text(text):
  return f"𓆩❤️𓆪 𝑩𝒂𝒓𝒄𝒉𝒂 𝒂𝒌𝒕𝒊𝒗 𝒃𝒐‘𝒍𝒊𝒃 𝒕𝒖𝒓𝒈𝒂𝒏𝒍𝒂𝒓𝒈𝒂: {text} 🖤"


def main():
  global last_auto_story_day
  print(
      "Bot 18+ jiddiy video va matn rejimida avtomatik tarzda ishga tushdi..."
  )
  offset = 0
  last_post_time = 0

  while True:
    try:
      # Kechki soat 19:30 da avtomatik VIDEO chiqarish tekshiruvi
      now = datetime.datetime.now()
      current_date_str = now.strftime("%Y-%m-%d")

      if (
          now.hour == 19
          and now.minute >= 30
          and last_auto_story_day != current_date_str
      ):
        last_auto_story_day = current_date_str

        # 1 kun osoyishta falsafa video matni, 1 kun motivatsion kino/anime video matni
        day_of_year = now.timetuple().tm_yday
        if day_of_year % 2 == 0:
          chosen_caption = random.choice(CALM_VIDEOS)
        else:
          chosen_caption = random.choice(MOTIVATIONAL_VIDEOS)

        formatted_story = format_text(chosen_caption)
        pending_content["type"] = "text"  # Yoki tayyor video bo'lsa video type qo'yiladi
        pending_content["content"] = formatted_story

        keyboard = {
            "inline_keyboard": [[
                {"text": "✅ Ruxsat berish", "callback_data": "approve"},
                {"text": "❌ Rad qilish", "callback_data": "reject"},
            ]]
        }
        send_telegram(
            "sendMessage",
            {
                "chat_id": ADMIN_ID,
                "text": (
                    "⏰ Kechki 19:30 vaqti keldi! Kunlik 18+ avtomatik"
                    " kontent tayyor:\n\n"
                    + formatted_story
                    + "\n\nKanalga tashlaymizmi?"
                ),
                "reply_markup": json.dumps(keyboard),
            },
        )

      updates = send_telegram("getUpdates", {"offset": offset, "timeout": 30})
      if updates and "result" in updates:
        for update in updates["result"]:
          offset = update["update_id"] + 1

          # Tugmalar bosilganda (Callback)
          if "callback_query" in update:
            callback = update["callback_query"]
            cb_chat_id = callback["message"]["chat"]["id"]
            data = callback["data"]
            message_id = callback["message"]["message_id"]

            if data == "approve":
              if pending_content["type"] == "text":
                send_telegram(
                    "sendMessage",
                    {
                        "chat_id": CHANNEL_ID,
                        "text": pending_content["content"],
                    },
                )
              elif pending_content["type"] == "video":
                send_telegram(
                    "sendVideo",
                    {
                        "chat_id": CHANNEL_ID,
                        "video": pending_content["media"],
                        "caption": pending_content["content"],
                    },
                )
              elif pending_content["type"] == "photo":
                send_telegram(
                    "sendPhoto",
                    {
                        "chat_id": CHANNEL_ID,
                        "photo": pending_content["media"],
                        "caption": pending_content["content"],
                    },
                )

              send_telegram(
                  "sendMessage",
                  {
                      "chat_id": cb_chat_id,
                      "text": (
                          "✅ Tasdiqlandi va kanalga muvaffaqiyatli"
                          " yuborildi!"
                      ),
                  },
              )
              last_post_time = time.time()

            elif data == "reject":
              send_telegram(
                  "sendMessage",
                  {
                      "chat_id": cb_chat_id,
                      "text": "❌ Post rad etildi.",
                  },
              )

            send_telegram(
                "editMessageReplyMarkup",
                {"chat_id": cb_chat_id, "message_id": message_id, "reply_markup": {"inline_keyboard": []}},
            )

          # Foydalanuvchidan xabar kelganda
          if "message" in update:
            message = update["message"]
            chat_id = message["chat"]["id"]
            text = message.get("text", "")

            if text == "/start":
              send_telegram(
                  "sendMessage",
                  {
                      "chat_id": chat_id,
                      "text": (
                          "Salom! Bot 18+ jiddiy va sifatli kontent rejimida"
                          " ishlamoqda. Menga istalgan matn, rasm yoki video"
                          " yuboring, uni dizaynga solib, sizdan ruxsat"
                          " so'rayman."
                      ),
                  },
              )
            elif chat_id == ADMIN_ID:
              # 2.5 soatlik oraliq tekshiruvi (9000 soniya)
              current_time = time.time()
              if current_time - last_post_time < 9000 and last_post_time != 0:
                left_minutes = int(
                    (9000 - (current_time - last_post_time)) / 60
                )
                send_telegram(
                    "sendMessage",
                    {
                        "chat_id": chat_id,
                        "text": (
                            f"⏳ Sal kuting! Har bir kontent orasida 2.5 soat"
                            f" o'tishi kerak. Yana {left_minutes} daqiqa"
                            " qoldi."
                        ),
                    },
                )
                continue

              keyboard = {
                  "inline_keyboard": [[
                      {"text": "✅ Ruxsat berish", "callback_data": "approve"},
                      {"text": "❌ Rad qilish", "callback_data": "reject"},
                  ]]
              }

              if "text" in message:
                formatted = format_text(message["text"])
                pending_content["type"] = "text"
                pending_content["content"] = formatted

                send_telegram(
                    "sendMessage",
                    {
                        "chat_id": ADMIN_ID,
                        "text": (
                            "Quyidagi xabar tayyorlandi, kanalga tashlaymizmi?\n\n"
                            + formatted
                        ),
                        "reply_markup": json.dumps(keyboard),
                    },
                )

              elif "video" in message:
                caption = message.get("caption", "")
                formatted_cap = format_text(caption) if caption else ""
                pending_content["type"] = "video"
                pending_content["media"] = message["video"]["file_id"]
                pending_content["content"] = formatted_cap

                send_telegram(
                    "sendVideo",
                    {
                        "chat_id": ADMIN_ID,
                        "video": pending_content["media"],
                        "caption": (
                            "Quyidagi video tayyor:\n"
                            + formatted_cap
                            + "\n\nKanalga tashlaymizmi?"
                        ),
                        "reply_markup": json.dumps(keyboard),
                    },
                )

              elif "photo" in message:
                caption = message.get("caption", "")
                formatted_cap = format_text(caption) if caption else ""
                pending_content["type"] = "photo"
                pending_content["media"] = message["photo"][-1]["file_id"]
                pending_content["content"] = formatted_cap

                send_telegram(
                    "sendPhoto",
                    {
                        "chat_id": ADMIN_ID,
                        "photo": pending_content["media"],
                        "caption": (
                            "Quyidagi rasm tayyor:\n"
                            + formatted_cap
                            + "\n\nKanalga tashlaymizmi?"
                        ),
                        "reply_markup": json.dumps(keyboard),
                    },
                )

    except Exception as e:
      print(f"Xatolik tsikli: {e}")
      time.sleep(3)


if __name__ == "__main__":
  main()


