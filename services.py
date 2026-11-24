from pydantic import Field
from core import InputModel

SCHEMA = ""


class DocumentInput(InputModel):
    title: str = Field(min_length=1, max_length=150)
    text: str = Field(min_length=1, max_length=40000)


class Question(InputModel):
    question: str = Field(min_length=1, max_length=2000)


class Service:
    def __init__(self, db):
        self.db = db


def seed(db, kb):
    if db.one("SELECT COUNT(*) AS TOTAL FROM documents")["TOTAL"] == 0:
        kb.add("alice", "Expense policy",
               "Expense reimbursement requires an itemized receipt and manager approval. Submit expenses within 30 days. Meals are capped at 1500 rupees per day. International travel requires prior written approval.")
        kb.add("bob", "Private team note",
               "The confidential launch codename is violet-orbit. This note is visible only to Bob.")
