import json
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

llm = ChatOpenAI(model="gpt-4o", temperature=0.0)



def extract_email_content(email: dict) -> dict:
    print("IN EXTRACT EMAIL CONTENT 🚀")
    subject = email.get('subject', '')
    body = email.get('body', '')[:1500]  # Limit to first 1500 characters
    date = email.get('date', '')


    system_msg = SystemMessage(content=(
        "You are an AI assistant that extracts structured job application details from an email. "
        "Given the subject and body, return ONLY JSON with the following keys: "
        "\"company\", \"job_title\", \"submission_date\". "
        "The \"submission_date\" should be extracted from the email if present; otherwise, use the email’s date or current date. "
        "Do NOT include code fences or extra text."
    ))


    human_message = HumanMessage(content=(
        f"Subject: {subject}\n"
        f"Body: {body}\n"
        f"Date: {date}\n"
    ))

    response = llm.invoke([system_msg, human_message])
    content = response.content.strip()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        data = {"company": "", "job_title": "", "submission_date": date}

    return data
