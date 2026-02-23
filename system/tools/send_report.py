#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright (c) 2026 Lukas Geiger

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
BACH Report Mailer
Sendet den Recherchebericht per Gmail
"""

import os
import sys
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Scopes für Gmail Send
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Pfade
SCRIPT_DIR = Path(__file__).parent
CRED_DIR = SCRIPT_DIR / "hub" / "_services" / "mail" / "credentials"
CREDENTIALS_FILE = CRED_DIR / "gmail_credentials.json"
TOKEN_FILE = CRED_DIR / "gmail_send_token.json"
REPORT_FILE = SCRIPT_DIR / "data" / "recherchebericht_wuerge_trend.md"

def get_gmail_service():
    """Erstellt Gmail API Service mit Send-Rechten"""
    creds = None

    # Lade existierendes Token
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    # Refresh oder neue Authentifizierung
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)

        # Token speichern
        with open(TOKEN_FILE, 'w', encoding='utf-8') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def send_email(to_email, subject, body_text, body_html=None):
    """Sendet E-Mail via Gmail API"""
    service = get_gmail_service()

    # Message erstellen
    if body_html:
        message = MIMEMultipart('alternative')
        message.attach(MIMEText(body_text, 'plain', 'utf-8'))
        message.attach(MIMEText(body_html, 'html', 'utf-8'))
    else:
        message = MIMEText(body_text, 'plain', 'utf-8')

    message['To'] = to_email
    message['Subject'] = subject

    # Encode
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    # Send
    try:
        result = service.users().messages().send(
            userId='me',
            body={'raw': raw}
        ).execute()
        print(f"✓ Mail erfolgreich versendet! Message ID: {result['id']}")
        return result
    except Exception as e:
        print(f"✗ Fehler beim Versand: {e}")
        raise

def main():
    # Empfänger
    recipient = input("Empfänger-E-Mail: ").strip()
    if not recipient:
        print("Keine E-Mail angegeben. Abbruch.")
        sys.exit(1)

    # Bericht laden
    if not REPORT_FILE.exists():
        print(f"Bericht nicht gefunden: {REPORT_FILE}")
        sys.exit(1)

    with open(REPORT_FILE, 'r', encoding='utf-8') as f:
        report_content = f.read()

    # Mail senden
    print(f"\nVersende Bericht an {recipient}...")
    send_email(
        to_email=recipient,
        subject="Recherchebericht: Würge-Trend (Choking Challenge) auf TikTok",
        body_text=report_content
    )

if __name__ == "__main__":
    main()
