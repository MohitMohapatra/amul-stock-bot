"""
Amul Stock Monitor — checks once and exits.
All config is read from environment variables (set as GitHub Secrets).
"""

import os
import logging
import smtplib
import requests
from email.mime.text import MIMEText
from datetime import datetime
from bs4 import BeautifulSoup

# ── CONFIG (set these as GitHub Secrets / env vars) ───────────────────────────

PRODUCT_URL     = os.environ.get("AMUL_PRODUCT_URL") or \
    "https://shop.amul.com/en/product/amul-chocolate-whey-protein-34-g-or-pack-of-60-sachets"
SENDER_EMAIL    = os.environ["AMUL_SENDER_EMAIL"]
SENDER_PASSWORD = os.environ["AMUL_SENDER_PASSWORD"]   # Gmail App Password
RECEIVER_EMAIL  = os.environ["AMUL_RECEIVER_EMAIL"]

OUT_OF_STOCK_PHRASES = [
    "out of stock",
    "sold out",
    "not available",
    "currently unavailable",
    "notify me",
]

# ── LOGGING ───────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
)
log = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

# ── CORE ──────────────────────────────────────────────────────────────────────

def check_stock() -> tuple[bool, str]:
    response = requests.get(PRODUCT_URL, headers=HEADERS, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")
    page_text = soup.get_text(separator=" ").lower()
    title = soup.title.string.strip() if soup.title else PRODUCT_URL

    for phrase in OUT_OF_STOCK_PHRASES:
        if phrase in page_text:
            return False, title

    add_to_cart = soup.find(
        lambda tag: tag.name in ("button", "a")
        and "add to cart" in (tag.get_text() or "").lower()
        and not tag.get("disabled")
    )
    return bool(add_to_cart), title


def send_email(subject: str, body: str) -> None:
    msg = MIMEText(body, "plain")
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
        smtp.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())

    log.info("Email sent to %s", RECEIVER_EMAIL)


def main() -> None:
    log.info("Checking: %s", PRODUCT_URL)
    in_stock, title = check_stock()

    if in_stock:
        log.info("IN STOCK: %s", title)
        send_email(
            subject="Amul Product is IN STOCK!",
            body=(
                f"The product is now available.\n\n"
                f"Product : {title}\n"
                f"Link    : {PRODUCT_URL}\n"
                f"Time    : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                "Hurry before it sells out again!"
            ),
        )
    else:
        log.info("Out of stock: %s", title)


if __name__ == "__main__":
    main()
