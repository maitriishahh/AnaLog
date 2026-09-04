from db.session import SessionLocal
from analytics.ingest import ingest_data

from analytics.analyze import get_total_requests,get_total_user_requests, get_unique_user_request, most_active_user, get_most_accessed_point, get_unique_endpoints, analyze_severity, calc_error_percent, find_suspicious_activity, most_error_endpoint, most_error_user, slow_request, slow_endpoints


def generate_report():
    ingest_data()
    db = SessionLocal()
    try:
        total_requests = get_total_requests(db)
        user_requests = get_total_user_requests(db)

        unique_users = get_unique_user_request(db)
        active_user, active_count = most_active_user(user_requests)

        most_accessed = get_most_accessed_point(db)
        unique_endpoints = get_unique_endpoints(db)

        severity_counts = analyze_severity(db)
        error_count = severity_counts.get('ERROR',0)
        error_percent = round(calc_error_percent(total_requests, error_count),2)
        most_error_ep = most_error_endpoint(db)

        error_users = list(most_error_user(db).items())
        suspicious_users = find_suspicious_activity(db)

        slow_requests = slow_request(db)
        slow_eps, slowest_request, highest_time = slow_endpoints(db)

        if slowest_request is not None:
            slowest_request_data = {
                "endpoint": slowest_request.endpoint,
                "response_time": slowest_request.response_time
            }
        else:
            slowest_request_data = None
    finally:
        db.close()

    return {
        "request_analytics": {
            "total_requests": total_requests,
            "most_accessed_endpoint": most_accessed,
            "unique_endpoints":unique_endpoints
        },

        "user_analytics": {
            "unique_users": unique_users,
            "most_active_user": active_user,
            "most_active_user_requests": active_count,
            "suspicious_users": suspicious_users
        },

        "error_analytics": {
            "info": severity_counts.get("INFO", 0),
            "warning": severity_counts.get("WARNING", 0),
            "error": severity_counts.get("ERROR", 0),
            "error_percentage": f"{error_percent}%",
            "most_error_user": error_users,
            "most_error_prone_endpoint": most_error_ep
        },

        "performance_analytics": {
            "total_slow_requests": len(slow_requests),
            "slow_endpoints": slow_eps,
            "slowest_request": slowest_request_data
        }
    }

