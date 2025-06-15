import os
import logging
from datetime import datetime
from notion_client import Client
from tito.transcriber.config import NOTION_TOKEN, NOTION_PAGE_ID

notion = Client(auth=NOTION_TOKEN)

def send_transcription_to_notion(transcript: str, context: str = "Meeting"):
    try:
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
        heading_title = f"{timestamp} — {context}"

        toggle_block = notion.blocks.children.append(
            NOTION_PAGE_ID,
            children=[
                {
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{"type": "text", "text": {"content": heading_title}}],
                        "is_toggleable": True
                    }
                }
            ]
        )

        toggle_block_id = toggle_block["results"][0]["id"]

        notion.blocks.children.append(
            toggle_block_id,
            children=[
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {"type": "text", "text": {"content": transcript.strip()}}
                        ]
                    }
                }
            ]
        )

        logging.info("Transcription successfully sent to Notion under toggle block.")

    except Exception as e:
        logging.error(f"Error sending transcription to Notion: {e}", exc_info=True)
