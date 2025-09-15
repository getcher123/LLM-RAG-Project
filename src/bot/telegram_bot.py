from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

import httpx
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)


AUDIO_API_BASE = os.getenv("AUDIO_API_BASE", "http://127.0.0.1:8001")
TRANSCRIBER_API_BASE = os.getenv("TRANSCRIBER_API_BASE", "http://127.0.0.1:8000")


@dataclass
class Session:
    url: Optional[str] = None


CHOICE_SEND_MP3 = "send_mp3"
CHOICE_TRANSCRIBE = "transcribe"
CHOICE_BOTH = "both"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Hi! Send me a YouTube link to process."
    )


async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (update.message.text or "").strip()
    if not text:
        return
    # Naive URL check
    if not (text.startswith("http://") or text.startswith("https://")):
        await update.message.reply_text("Please send a valid URL.")
        return

    context.user_data["session"] = Session(url=text)
    kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Send MP3", callback_data=CHOICE_SEND_MP3),
            InlineKeyboardButton("Transcribe only", callback_data=CHOICE_TRANSCRIBE),
            InlineKeyboardButton("Both", callback_data=CHOICE_BOTH),
        ]
    ])
    await update.message.reply_text("What would you like to do?", reply_markup=kb)


async def on_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    choice = query.data
    sess: Session = context.user_data.get("session") or Session()
    if not sess.url:
        await query.edit_message_text("No URL found in session. Please send a link again.")
        return

    url = sess.url
    await query.edit_message_text(f"Working on it: {choice}…")

    mp3_path: Optional[str] = None
    transcript_text: Optional[str] = None

    # Download MP3 internally
    if choice in (CHOICE_SEND_MP3, CHOICE_BOTH, CHOICE_TRANSCRIBE):
        try:
            async with httpx.AsyncClient(timeout=120) as client:
                r = await client.post(f"{AUDIO_API_BASE}/audio/save", json={"url": url})
                r.raise_for_status()
                mp3_path = r.json().get("path")
        except Exception as e:
            await query.message.reply_text(f"Audio save failed: {e}")
            return

    # If requested, run transcription
    if choice in (CHOICE_TRANSCRIBE, CHOICE_BOTH):
        try:
            async with httpx.AsyncClient(timeout=300) as client:
                r = await client.post(
                    f"{TRANSCRIBER_API_BASE}/transcribe/path",
                    params={"file_path": mp3_path, "out_dir": "data/transcripts_raw"},
                )
                r.raise_for_status()
                payload = r.json().get("payload") or {}
                transcript_text = payload.get("full_text") or "<no text>"
        except Exception as e:
            await query.message.reply_text(f"Transcription failed: {e}")
            return

    # Send outputs
    if choice in (CHOICE_SEND_MP3, CHOICE_BOTH) and mp3_path:
        try:
            with open(mp3_path, "rb") as fh:
                await query.message.reply_audio(audio=fh, caption="Here is your MP3")
        except Exception as e:
            await query.message.reply_text(f"Failed to send audio: {e}")

    if choice in (CHOICE_TRANSCRIBE, CHOICE_BOTH) and transcript_text:
        await query.message.reply_text(transcript_text[:4000])  # Telegram message limit safe guard


def run_bot() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    app.add_handler(CallbackQueryHandler(on_choice))
    app.run_polling()


if __name__ == "__main__":
    run_bot()

