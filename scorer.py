from questions import QUESTIONS

import re

def _norm(text: str) -> str:
    # lowercase, drop punctuation, collapse whitespace so "Eight washers,  six dryers." still matches
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", (text or "").lower())).strip()

def judge(question, expects, answer, result) -> bool:
    if not expects or not answer:
        return False
    options = expects if isinstance(expects, list) else expects.split("|")
    return any(_norm(o) in _norm(answer) for o in options if o.strip())


