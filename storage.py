import json
from pathlib import Path
from datetime import datetime
from typing import Mapping, Any
import hashlib
import models

def hash_pii(value: str) -> str:
    """Hashes a string using SHA256"""
    return hashlib.sha256(str(value).encode()).hexdigest()

RESULTS_PATH = Path("data/survey.ndjson")

def save_survey(submission: models.SurveySubmission):
    submission_dict = submission.dict()

    if not submission_dict.get('submission_id'):
        now = datetime.utcnow()
        date_hour_str = now.strftime('%Y%m%d%H')
        id_source = submission.email + date_hour_str
        submission_dict['submission_id'] = hash_pii(id_source)

    submission_dict['email'] = hash_pii(submission_dict['email'])
    submission_dict['age'] = hash_pii(submission_dict['age'])

    append_json_line(submission_dict)

def append_json_line(record: Mapping[str, Any]) -> None:
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with RESULTS_PATH.open("a", encoding="utf-8") as f:
        f.write(
            json.dumps(
                record,
                ensure_ascii=False,
                default=lambda o: o.isoformat() if isinstance(o, datetime) else o
            ) + "\n"
        )
