from fastapi import FastAPI, Response, Depends
from sqlalchemy.orm import Session
import uuid
from database import get_db
from models import ChatSession

app = FastAPI()

@app.post("/session/")
def create_session(response: Response, db: Session = Depends(get_db)):
    session_id = str(uuid.uuid4())  # Generate a unique session ID
    new_session = ChatSession(session_id=session_id)
    
    db.add(new_session)
    db.commit()

    response.set_cookie(key="session_id", value=session_id, httponly=True)  # Store in cookie
    return {"session_id": session_id}
### Stores the session ID in a cookie so the client doesn’t need to manually enter it.
# httponly=True in set_cookie() - What Does It Mean?
# When you set httponly=True in a cookie:

# ✅ The cookie is only accessible by the server (FastAPI).
# ✅ JavaScript in the browser cannot read or modify the cookie.

# This protects the session ID from:

# Cross-Site Scripting (XSS) attacks where hackers inject JavaScript to steal cookies.
# Client-side tampering (users cannot modify the session ID manually).



from fastapi import Request, HTTPException

@app.post("/chat/")
def chat(request: Request, message: str, db: Session = Depends(get_db)):
    session_id = request.cookies.get("session_id")  # Auto-retrieve session ID

    if not session_id:
        raise HTTPException(status_code=400, detail="Session ID not found. Create a session first.")

    new_chat = Chat(session_id=session_id, message=message)
    db.add(new_chat)
    db.commit()
    
    return {"message": "Message stored successfully", "session_id": session_id}
