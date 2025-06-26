from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from mcp.server.fastmcp import FastMCP
import datetime
import os
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio

app = FastAPI()
mcp = FastMCP("UnifiedCopilotAgent")

# Mount static directory for CSS (if needed)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Gmail API setup
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

load_dotenv()
STANDARD_EMAIL = os.getenv('STANDARD_EMAIL', 'kumarsunkaraboina27@gmail.com')

def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service

# Set up the LLM agent globally
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY") or ""

client = MultiServerMCPClient({
    "copilot": {
        "url": "http://localhost:8000/mcp",
        "transport": "streamable_http"
    }
})
agent = None  # Global placeholder for the LLM agent

@app.on_event("startup")
async def startup_event():
    global agent
    tools = await client.get_tools()
    model = ChatGroq(model="llama-3.3-70b-versatile")
    agent = create_react_agent(model, tools)

# Serve the chatbot UI from templates/chat.html
@app.get("/", response_class=HTMLResponse)
def chat_ui(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/chat")
async def chat_api(message: str = Form(...)):
    global agent
    response = await agent.ainvoke({"messages": [{"role": "user", "content": message}]})
    return JSONResponse({"reply": response['messages'][-1].content})

@mcp.tool()
def get_recent_emails(user: str) -> str:
    """Fetch recent emails for the user from Gmail."""
    try:
        service = get_gmail_service()
        results = service.users().messages().list(userId='me', maxResults=3).execute()
        messages = results.get('messages', [])
        email_summaries = []
        for msg in messages:
            msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
            headers = msg_data.get('payload', {}).get('headers', [])
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
            snippet = msg_data.get('snippet', '')
            email_summaries.append(f"- <b>{subject}</b> from <i>{sender}</i>: {snippet[:100]}...")
        if not email_summaries:
            return "No recent emails found."
        return "Recent emails:<br>" + "<br>".join(email_summaries)
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
    mcp.run(transport='streamable_http')
