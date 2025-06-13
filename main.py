
from dotenv import load_dotenv
import os
from typing import Annotated, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
from typing_extensions import TypedDict
from agents.email_reader import fetch_today_emails
from agents.email_classifier import classify_email





def main():
    load_dotenv()
    emails = fetch_today_emails()
    print(f"📧 Found {len(emails)} emails for today.")
    for email in emails:
        result = classify_email(email)
        print(f"\n📧 Subject: {email['subject']}")
        print(f"✅ Is Job Application? {result['is_job_application']}")
        print(f"💡 Reason: {result['reason']}")



if __name__ == "__main__":
    main()