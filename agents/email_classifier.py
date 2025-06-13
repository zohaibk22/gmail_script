from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o", temperature=0.0)

def classify_email(email:dict) -> dict:
    subject = email.get("subject", "")
    body = email.get("body", "")[:1000]

    system_msg = SystemMessage(content=(
        "You're an email assistant. Determine whether an email is about a job application submission. "
        "Respond with JSON like: {\"is_job_application\": true/false, \"reason\": \"...\"}"
    ))



    user_msg = HumanMessage(content=f"""
Subject: {subject}
Body:
{body}
""")
    
    response = llm.invoke([system_msg, user_msg])
    print(f"Response: {response}")
    try:
        result = eval(response.content)
        print("DID YOU GET HERE?")
    except:
        print("IN EXCEPT")
        result = {"is_job_application": False, "reason": "Could not parse response"}


    return result