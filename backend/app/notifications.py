"""Email and WhatsApp notification stubs. Configure SMTP/WhatsApp (e.g. Twilio) for real sending."""
from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .models import User

logger = logging.getLogger(__name__)


def send_email(to_email: str, subject: str, body: str) -> bool:
    """Send email. Uses SMTP if configured (e.g. SMTP_HOST), otherwise logs."""
    smtp_host = os.environ.get("SMTP_HOST")
    if smtp_host:
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            msg = MIMEMultipart()
            msg["Subject"] = subject
            msg["From"] = os.environ.get("SMTP_FROM", "ecotrack@localhost")
            msg["To"] = to_email
            msg.attach(MIMEText(body, "plain"))
            with smtplib.SMTP(smtp_host, int(os.environ.get("SMTP_PORT", "25"))) as s:
                if os.environ.get("SMTP_STARTTLS"):
                    s.starttls()
                if os.environ.get("SMTP_USER"):
                    s.login(os.environ["SMTP_USER"], os.environ.get("SMTP_PASSWORD", ""))
                s.send_message(msg)
            logger.info("Email sent to %s", to_email)
            return True
        except Exception as e:
            logger.warning("Email send failed to %s: %s", to_email, e)
            return False
    logger.info("[Email stub] To=%s Subject=%s Body=%s", to_email, subject, body[:100])
    return True


def send_whatsapp(phone: str, message: str) -> bool:
    """Send WhatsApp. Uses Twilio if configured (TWILIO_*), otherwise logs."""
    phone = (phone or "").strip()
    if not phone:
        return False
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    from_whatsapp = os.environ.get("TWILIO_WHATSAPP_FROM")
    if account_sid and auth_token and from_whatsapp:
        try:
            from twilio.rest import Client
            client = Client(account_sid, auth_token)
            client.messages.create(
                body=message,
                from_=from_whatsapp,
                to=f"whatsapp:{phone}" if not phone.startswith("whatsapp:") else phone,
            )
            logger.info("WhatsApp sent to %s", phone)
            return True
        except Exception as e:
            logger.warning("WhatsApp send failed to %s: %s", phone, e)
            return False
    logger.info("[WhatsApp stub] To=%s Message=%s", phone, message[:80])
    return True


def send_activity_reminders(
    users: List["User"],
    project_name: str,
    activity_date: str,
    task_summary: str,
) -> None:
    """Send email and WhatsApp to each user about activities for the given date."""
    subject = f"NRPT: Activities for {activity_date} — {project_name}"
    body = f"Activities scheduled for {activity_date} in project {project_name}:\n\n{task_summary}\n\n— NRPT"
    seen_emails = set()
    seen_phones = set()
    for u in users:
        if u.email and u.email not in seen_emails:
            send_email(u.email, subject, body)
            seen_emails.add(u.email)
        if u.whatsapp_phone and u.whatsapp_phone not in seen_phones:
            send_whatsapp(u.whatsapp_phone, f"Ecotrack: Activities for {activity_date} — {project_name}\n\n{task_summary[:200]}")
            seen_phones.add(u.whatsapp_phone)


def send_defect_reminders(
    users: List["User"],
    project_name: str,
    defect_summary: str,
) -> None:
    """Send email and WhatsApp to each user about open defects assigned to them."""
    subject = f"Ecotrack: Defect reminders — {project_name}"
    body = f"Open defects requiring attention in project {project_name}:\n\n{defect_summary}\n\n— Ecotrack"
    seen_emails = set()
    seen_phones = set()
    for u in users:
        if u.email and u.email not in seen_emails:
            send_email(u.email, subject, body)
            seen_emails.add(u.email)
        if u.whatsapp_phone and u.whatsapp_phone not in seen_phones:
            send_whatsapp(u.whatsapp_phone, f"Ecotrack: Defect reminders — {project_name}\n\n{defect_summary[:200]}")
            seen_phones.add(u.whatsapp_phone)
