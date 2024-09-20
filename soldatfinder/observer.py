import logging
import os
from datetime import date
from typing import Optional

from dateutil.parser import parse
from dotenv import load_dotenv
from fuzzywuzzy import fuzz
from telethon import TelegramClient, events

from bot import send_message
from soldiers import SoldierRepository

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _match_name_in_message(
    message: str, target_name: str, threshold: int = 70
) -> bool:
    """Check if both first name and surname of
    the target_name are present in the message with a fuzzy match."""
    target_parts = target_name.split()

    if len(target_parts) != 2:
        return False

    first_name, surname = target_parts

    message_words = message.split()

    found_first_name = any(
        fuzz.ratio(word.lower(), first_name.lower()) >= threshold
        for word in message_words
    )
    found_surname = any(
        fuzz.ratio(word.lower(), surname.lower()) >= threshold
        for word in message_words
    )

    return found_first_name and found_surname


def _extract_date_from_message(message: str) -> Optional[date]:
    """Extract date from the message if any."""
    try:
        parsed_date = parse(message, fuzzy=True)
        return parsed_date.date()
    except ValueError:
        return None


def main():
    load_dotenv()

    api_id = os.getenv("TELEGRAM_API_ID")
    api_hash = os.getenv("TELEGRAM_API_HASH")

    if not api_id:
        raise ValueError("Environment variable TELEGRAM_API_ID is not set")

    if not api_hash:
        raise ValueError("Environment variable TELEGRAM_API_HASH is not set")

    try:
        api_id = int(api_id)
    except ValueError:
        raise ValueError(
            "Environment variable TELEGRAM_API_ID must be an integer"
        )

    CHANNELS = [
        -1001845907716,
        -1001542074211,
        -1001923497239,
        -1001666094161,
        -1001676376547,
        -1001909925694,
        -1001285348580,
        -1001837743468,
        -1001689374765,
        -1001453960815,
        -1002061108277,
    ]

    soldier_repository = SoldierRepository()

    client = TelegramClient("session_name", api_id, api_hash)
    client.start()

    @client.on(events.NewMessage(chats=CHANNELS))
    async def my_event_handler(event):
        logger.info(f"Received event: {event}")
        message_text = event.message.message
        soldiers = soldier_repository.get_all()

        # Extract date from message once
        message_date = _extract_date_from_message(message_text)

        for soldier in soldiers:
            try:
                if _match_name_in_message(message_text, soldier.name):
                    message_url = (
                        f"https://t.me/c/{event.message.peer_id.channel_id}/"
                        f"{event.message.id}"
                    )
                    await send_message(
                        soldier.chat_id,
                        f"Similar name found in message: {message_url}",
                    )

                if message_date and soldier.birthdate == message_date:
                    message_url = (
                        f"https://t.me/c/{event.message.peer_id.channel_id}/"
                        f"{event.message.id}"
                    )
                    await send_message(
                        soldier.chat_id,
                        f"Date found in message: {message_url}",
                    )
            except Exception as e:
                logger.error(f"Error processing soldier {soldier.name}: {e}")

    try:
        client.run_until_disconnected()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
