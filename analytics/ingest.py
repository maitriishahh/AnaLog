import json
from db.models import Log
from db.session import SessionLocal
from sqlalchemy.exc import SQLAlchemyError

def ingest_data():
    final_logs = []
    required_fields = [
        "timestamp",
        "level",
        "user_id",
        "method",
        "endpoint",
        "status_code",
        "response_time"
    ]

    with open("logs.jsonl","r") as file:
        db = SessionLocal()
        for log in file:
            log = log.strip() #removes extra whitespace
            if not log: #skips empty lines
                continue
            try:
                new = json.loads(log) #json to python dict
                if all(field in new for field in required_fields):
                    new['response_time'] = round(float(new['response_time']),2)
                    final_logs.append(new)
                    log_entry = Log(
                        timestamp=new["timestamp"],
                        level=new["level"],
                        user_id=new["user_id"],
                        method=new["method"],
                        endpoint=new["endpoint"],
                        status_code=new["status_code"],
                        response_time=new["response_time"]
                    )

                    existing_logs = db.query(Log).filter(
                        Log.timestamp == new["timestamp"],
                        Log.user_id == new["user_id"],
                        Log.method == new["method"],
                        Log.endpoint == new["endpoint"],
                        Log.status_code == new["status_code"],
                        Log.response_time == new["response_time"]
                    ).first()
                    if existing_logs is None:
                        db.add(log_entry)
                else:
                    print('Invalid log skipped - required field is missing')

            except (json.JSONDecodeError, ValueError): #skips lines that have invalid json
                print("Invalid log skipped - invalid json")
        try:
            db.commit()
        except SQLAlchemyError:
            db.rollback()
        finally:
            db.close()

    return final_logs
