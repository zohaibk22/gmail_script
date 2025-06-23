from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv
import json

load_dotenv()

llm = ChatOpenAI(model="gpt-4o", temperature=0.0)

def classify_email(email:dict) -> dict:
    print("IN CLASSIFY EMAIL CONTENT 🚀")
    subject = email.get("subject", "")
    body = email.get("body", "")[:1000]

    system_msg = SystemMessage(content=(
        "You're an email assistant. Determine whether an email is about a job application submission. It can be the submission itself. As long as it is a job application I submitted. Do not consider emails that are about job offers, interviews, or any other job-related topics. Focus only on the submission of a job application.\n\n"
        "Respond with JSON like: {\"is_job_application\": true/false, \"reason\": \"...\"}. Do not add any other text"
    ))


    user_msg = HumanMessage(content=f"Subject: {subject}\n\nBody: {body}")
    
    response = llm.invoke([system_msg, user_msg])
    print(f"Response: {response.content}")
    try:
        result = json.loads(response.content)
      
    except Exception as e:
        result = {"is_job_application": False, "reason": "Could not parse response"}


    return result