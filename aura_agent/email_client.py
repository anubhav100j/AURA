import base64
import email
from googleapiclient.errors import HttpError
import google.generativeai as genai

def list_emails(service, count=5):
    """
    Lists the most recent emails in the user's inbox.
    Returns a list of messages, each with 'id', 'subject', and 'from'.
    """
    try:
        results = service.users().messages().list(userId="me", labelIds=["INBOX"], maxResults=count).execute()
        messages = results.get("messages", [])

        email_list = []
        if not messages:
            return "No new messages found."
        else:
            for message in messages:
                msg = service.users().messages().get(userId="me", id=message["id"], format="metadata").execute()
                headers = msg["payload"]["headers"]
                subject = next(header["value"] for header in headers if header["name"] == "Subject")
                sender = next(header["value"] for header in headers if header["name"] == "From")
                email_list.append({"id": msg["id"], "subject": subject, "from": sender})
            return email_list
    except HttpError as error:
        return f"An error occurred: {error}"

def get_email_body(payload):
    """
    Recursively extracts the text/plain body from an email payload.
    """
    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain":
                data = part["body"]["data"]
                return base64.urlsafe_b64decode(data).decode("utf-8")
            # Recurse into multipart/alternative to find the plain text part
            if "parts" in part:
                body = get_email_body(part)
                if body:
                    return body
    elif payload["mimeType"] == "text/plain":
        data = payload["body"]["data"]
        return base64.urlsafe_b64decode(data).decode("utf-8")
    return ""

def read_email(service, message_id):
    """
    Reads a single email by its message ID.
    Returns the email's subject, sender, and body.
    """
    try:
        msg = service.users().messages().get(userId="me", id=message_id, format="full").execute()
        payload = msg["payload"]
        headers = payload["headers"]

        subject = next(header["value"] for header in headers if header["name"] == "Subject")
        sender = next(header["value"] for header in headers if header["name"] == "From")

        body = get_email_body(payload)

        if not body:
            body = msg.get("snippet", "No content found.")

        return {"subject": subject, "from": sender, "body": body}
    except HttpError as error:
        return f"An error occurred: {error}"

def summarize_text(text_to_summarize):
    """
    Uses the Gemini API to summarize a given block of text.
    """
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"Please summarize the following text in a few sentences:\n\n{text_to_summarize}"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Could not summarize the text: {e}"