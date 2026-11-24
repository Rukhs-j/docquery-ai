from fastapi import Depends, UploadFile, File
from core import User, Problem, current_user
from factory import make_application
from services import SCHEMA, Service, DocumentInput, Question, seed


def register(app, db, kb, service):
    @app.get("/api/documents")
    def documents(user: User = Depends(current_user)):
        return kb.list(user.username)

    @app.post("/api/documents")
    def add(body: DocumentInput, user: User = Depends(current_user)):
        return kb.add(user.username, body.title, body.text)

    @app.post("/api/documents/upload")
    def upload(file: UploadFile = File(...), user: User = Depends(current_user)):
        name = file.filename or ""
        if not name.lower().endswith((".txt", ".md")):
            raise Problem(400, "Upload UTF-8 .txt or .md files; PDF parsing is not included")
        raw = file.file.read(40001)
        if len(raw) > 40000:
            raise Problem(400, "File must be at most 40000 bytes")
        try:
            content = raw.decode("utf-8-sig")
        except UnicodeDecodeError as error:
            raise Problem(400, "File must contain valid UTF-8 text") from error
        return kb.add(user.username, name, content)

    @app.delete("/api/documents/{document_id}")
    def delete(document_id: str, user: User = Depends(current_user)):
        kb.delete(user.username, document_id)
        return {"deleted": True}

    @app.post("/api/ask")
    def ask(body: Question, user: User = Depends(current_user)):
        return kb.ask(user.username, body.question)

    @app.post("/api/search")
    def search(body: Question, user: User = Depends(current_user)):
        return kb.search(user.username, body.question)


def create_app(db_path=None, ai_mode=None, enable_worker=True, ai_client=None):
    return make_application("DocQuery AI Python", SCHEMA, register, seed, Service,
                            db_path, ai_mode, enable_worker, ai_client)


app = create_app()
