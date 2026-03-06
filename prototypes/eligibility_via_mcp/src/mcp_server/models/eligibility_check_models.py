from pydantic import BaseModel
from typing import Union

class Decision(BaseModel):
    eligible: bool
    reason: str

    @classmethod
    def new(cls, eligible: bool, reason: str = ""):
        return cls(eligible=eligible, reason=reason)
    
class NextQuestion(BaseModel):
    step: int
    addendum: str

    @classmethod
    def new(cls, step: int, addendum: str = ""):
        return cls(step=step, addendum=addendum)

class Question(BaseModel):
    question: str
    answers_and_outcomes: dict[str, Union[Decision, NextQuestion]] = {}
    glossary: dict[str, str] = {}

    @classmethod
    def new(cls, question: str):
        return cls(question=question)
    
    def add_answer_and_outcome(self, answer: str, outcome: Union[NextQuestion, Decision]) -> Question:
        self.answers_and_outcomes.update({answer: outcome})
        return self
    
    def add_to_glossary(self, term: str, definition: str) -> Question:
        self.glossary.update({term: definition})
        return self