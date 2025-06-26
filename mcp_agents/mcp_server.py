from mcp.server.fastmcp import FastMCP
import datetime
import os
import pickle
from typing import List
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dotenv import load_dotenv

load_dotenv()
STANDARD_EMAIL = os.getenv('STANDARD_EMAIL', 'kumarsunkaraboina27@gmail.com')

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), 'credentials.json')
TOKEN_FILE = os.path.join(os.path.dirname(__file__), 'token.pickle')

def get_gmail_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES, redirect_uri='http://127.0.0.1:8001/')
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    service = build('gmail', 'v1', credentials=creds)
    return service

mcp = FastMCP("UnifiedCopilotAgent")

@mcp.tool()
def get_recent_emails(user: str, max_results: int = 5) -> str:
    """Fetch recent emails for the user from Gmail inbox."""
    try:
        service = get_gmail_service()
        results = service.users().messages().list(userId='me', maxResults=max_results).execute()
        messages = results.get('messages', [])
        email_summaries = []
        for msg in messages:
            msg_data = service.users().messages().get(userId='me', id=msg['id'], format='metadata').execute()
            snippet = msg_data.get('snippet', '')
            email_summaries.append(snippet)
        if not email_summaries:
            return "No recent emails found."
        return "Recent emails:\n" + "\n".join(email_summaries)
    except Exception as e:
        return f"Error fetching emails: {e}"

@mcp.tool()
def get_upcoming_events(user: str) -> str:
    today = datetime.date.today()
    return f"Upcoming events for {user}:\n- Math Exam on {today + datetime.timedelta(days=2)}\n- Project meeting on {today + datetime.timedelta(days=4)}"

@mcp.tool()
def get_recent_docs(user: str) -> str:
    return f"Recent Google Docs for {user}:\n- Final Year Project Proposal\n- Assignment 3 Submission\n- Meeting Notes"

@mcp.tool()
def get_recent_slides(user: str) -> str:
    return f"Recent Google Slides for {user}:\n- Project Presentation\n- Semester Recap\n- Group Study Plan"

@mcp.tool()
def get_ticket_details(ticket_id: str) -> str:
    return f"JIRA Ticket {ticket_id}:\n- Title: Fix login bug\n- Assigned to: You\n- Due: {datetime.date.today() + datetime.timedelta(days=3)}\n- Status: In Progress"

@mcp.tool()
def ask_question(question: str) -> str:
    return f"I'm your copilot! You asked: '{question}'. I can help with emails, calendar, docs, slides, and JIRA."

if __name__ == "__main__":
    mcp.run(transport='streamable-http') 