from db.models import Log
from sqlalchemy import func

def get_total_requests(db):
    return db.query(func.count(Log.id)).scalar()


def get_total_user_requests(db):
    results = db.query(
        Log.user_id,
        func.count(Log.id)
    ).filter(
        Log.user_id.isnot(None)
    ).group_by(
        Log.user_id
    ).all()

    return dict(results)


def most_active_user(dct):
    count = 0
    user = None

    for k, v in dct.items():
        if v > count:
            count = v
            user = k

    return user, count


def get_unique_user_request(db):
    return db.query(
        func.count(func.distinct(Log.user_id))
    ).filter(
        Log.user_id.isnot(None)
    ).scalar()


def get_most_accessed_point(db):
    result = db.query(
        Log.endpoint,
        func.count(Log.id).label("count")
    ).group_by(
        Log.endpoint
    ).order_by(
        func.count(Log.id).desc()
    ).first()

    if result:
        return result.endpoint

    return None


def get_unique_endpoints(db):
    return db.query(
        func.count(func.distinct(Log.endpoint))
    ).scalar()


def analyze_severity(db):
    results = db.query(
        Log.level,
        func.count(Log.id)
    ).group_by(
        Log.level
    ).all()

    return dict(results)


def calc_error_percent(total_req, error_count):
    if total_req == 0:
        return 0

    error_percentage = (error_count / total_req) * 100
    return error_percentage


def most_error_user(db):
    results = db.query(
        Log.user_id,
        func.count(Log.id).label("error_count")
    ).filter(
        Log.level == "ERROR",
        Log.user_id.isnot(None)
    ).group_by(
        Log.user_id
    ).all()

    return dict(results)


def filter_users(tup):
    k, v = tup

    if v > 3:
        return True

    return False


def group_severity(db):
    results = db.query(
        Log.level,
        func.count(Log.id)
    ).group_by(
        Log.level
    ).all()

    return dict(results)


def most_error_endpoint(db):
    result = db.query(
        Log.endpoint,
        func.count(Log.id).label("error_count")
    ).filter(
        Log.level == "ERROR"
    ).group_by(
        Log.endpoint
    ).order_by(
        func.count(Log.id).desc()
    ).first()

    if result:
        return result.endpoint

    return None


def find_suspicious_activity(db):
    users = {}

    err_counts = most_error_user(db)
    total_user_reqs = get_total_user_requests(db)

    for user, user_err in err_counts.items():
        user_req = total_user_reqs[user]

        err_percent = round(
            (user_err / user_req) * 100,
            2
        )

        sus_user = {
            "reason": []
        }

        if user_err > 3:
            sus_user["reason"].append(
                "More than 3 errors"
            )

        if err_percent > 50:
            sus_user["err_percent"] = err_percent
            sus_user["reason"].append(
                "Error rate above 50%"
            )

        if sus_user["reason"]:
            users[user] = sus_user

    return users


def slow_request(db):
    return db.query(Log).filter(
        Log.response_time > 1000
    ).all()


def slow_endpoints(db):
    results = db.query(
        Log.endpoint,
        func.count(Log.id).label("slow_count")
    ).filter(
        Log.response_time > 1000
    ).group_by(
        Log.endpoint
    ).all()

    slow_eps = dict(results)

    slowest = db.query(Log).filter(
        Log.response_time > 1000
    ).order_by(
        Log.response_time.desc()
    ).first()

    if slowest:
        highest_time = slowest.response_time
    else:
        highest_time = 0

    return slow_eps, slowest, highest_time