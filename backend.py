from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
import openai
from typing import Optional
import sqlite3
import bcrypt

app = FastAPI(title="Python Optimizer AI Backend", version="2.0.0")

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (username TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- Models ---
class User(BaseModel):
    username: str
    password: str

class CodeReviewRequest(BaseModel):
    code: str
    model: str = "gpt-4o"

class CodeReviewResponse(BaseModel):
    result: str

# --- Helpers ---
def get_user(username: str):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    return user

def get_ai_response(api_key: str, model: str, system_msg: str, prompt: str):
    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        return response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Endpoints ---
@app.post("/signup")
async def signup(user: User):
    if get_user(user.username):
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (?, ?)", (user.username, hashed))
    conn.commit()
    conn.close()
    return {"message": "User created successfully"}

@app.post("/login")
async def login(user: User):
    db_user = get_user(user.username)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if bcrypt.checkpw(user.password.encode('utf-8'), db_user[1].encode('utf-8')):
        return {"username": user.username, "status": "authenticated"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/optimize", response_model=CodeReviewResponse)
async def optimize_python(request: CodeReviewRequest, authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="API Key required")
    
    # Reject non-python code (simple check, enhanced by prompt)
    if "def " not in request.code and "import " not in request.code and "print(" not in request.code:
         # This is a weak check, but we will enforce it in the system prompt too.
         pass

    api_key = authorization.replace("Bearer ", "") if authorization.startswith("Bearer ") else authorization

    system_msg = """You are a Python Performance Architect. 
    REJECT any code that is NOT Python. If the code is not Python, return: "ERROR: This engine only supports Python optimization."
    If it IS Python, provide:
    1. A 'Pre-Optimization' analysis of Big O complexity.
    2. The fully optimized code block (using generators, list comprehensions, built-ins, or better algorithms).
    3. A 'Post-Optimization' analysis.
    4. Detailed explanation of changes.
    Use Markdown."""

    prompt = f"Optimize this Python code:\n\n```python\n{request.code}\n```"
    
    result = get_ai_response(api_key, request.model, system_msg, prompt)
    
    if "ERROR: This engine only supports Python optimization" in result:
        raise HTTPException(status_code=400, detail="Non-Python code detected. This engine is Python-only.")

    return CodeReviewResponse(result=result)

@app.get("/health")
async def health_check():
    return {"status": "active", "engine": "Python-Turbo AI v2.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
