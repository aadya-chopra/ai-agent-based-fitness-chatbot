# src/agent.py

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferWindowMemory

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("⚠️ GROQ_API_KEY not found in .env file")

# 1. System Prompt
SYSTEM_PROMPT = """
You are a professional, motivating, and safety-conscious Fitness and Nutrition Coach named 'GroqFit'.
Your goal is to help users set and achieve their fitness goals, providing personalized advice on workouts, diet, and recovery.
ALWAYS maintain a positive and encouraging tone.
Crucially, you are NOT a medical professional. If a user asks for medical advice, tell them: 
"I am a fitness coach, not a medical doctor. Please consult a qualified physician for medical advice."
"""

# 2. Select Groq Model (change here if needed)
MODEL_NAME = "llama-3.3-70b-versatile"  # ✅ valid Groq model

# 3. Define the LLM
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model=MODEL_NAME,
    temperature=0
)

# 4. Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)

# 5. Memory (remembers last 5 turns)
memory = ConversationBufferWindowMemory(k=5, memory_key="history", return_messages=True)

# 6. Response Function
def get_agent_response(user_input: str):
    history_data = memory.load_memory_variables({})['history']
    chain = prompt | llm
    inputs = {"input": user_input, "history": history_data}

    try:
        response = chain.invoke(inputs)
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

    memory.save_context({"input": user_input}, {"output": response.content})
    return response.content

# 7. CLI Testing
if __name__ == "__main__":
    print("Welcome to GroqFit! Ask me anything about fitness or diet.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        print(f"GroqFit: {get_agent_response(user_input)}")
