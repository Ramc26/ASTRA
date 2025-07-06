# tools/whatsapp.py

import os
import json
import urllib.parse
import webbrowser
from dotenv import load_dotenv

load_dotenv()

# Load contacts dict from .env
_contacts_raw = os.getenv("CONTACTS", "{}")
CONTACTS = json.loads(_contacts_raw)

def send_whatsapp_link(name: str, message: str) -> str:
    """
    Build a WhatsApp click-to-chat URL for the given contact name and message.
    """
    if name not in CONTACTS:
        raise KeyError(f"Contact '{name}' not found in CONTACTS.")

    phone = CONTACTS[name].lstrip("+")
    text = urllib.parse.quote(message, safe="")
    url = f"https://api.whatsapp.com/send?phone={phone}&text={text}"
    return url

def open_whatsapp(name: str, message: str) -> str:
    """
    Generate the WhatsApp URL and open it in the default web browser.
    Returns the URL that was opened.
    """
    url = send_whatsapp_link(name, message)
    webbrowser.open(url)      
    return url


# print(open_whatsapp("Ram", "Hello"))