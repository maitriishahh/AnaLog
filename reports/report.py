from analytics.analyze import new_logs, get_total_requests,get_total_user_requests, get_unique_user_request, most_active_user, get_most_accessed_point, get_unique_endpoints, analyze_severity, calc_error_percent, filtered_users, find_suspicious_activity, most_error_endpoint, most_error_user

def generate_report():
    total_requests = get_total_requests(new_logs)
    user_requests = get_total_user_requests(new_logs)

    unique_users = get_unique_user_request(new_logs)
    active_user, active_count = most_active_user(user_requests)

    most_accessed = get_most_accessed_point(new_logs)
    unique_endpoints = get_unique_endpoints(new_logs)

    severity_counts = analyze_severity(new_logs)
    error_count = severity_counts['ERROR']
    error_percent = calc_error_percent(total_requests, error_count)

    error_users = list(filtered_users)
    suspicious_users = find_suspicious_activity(new_logs)

    # print("=" * 40)
    # print("        SERVER LOG ANALYSIS")
    # print("=" * 40)
    #
    # print(f"\nTotal requests       : {total_requests}")
    # print(f"Unique users         : {len(unique_users)}")
    # print(f"Unique endpoints     : {len(unique_endpoints)}")
    #
    # print("\n--------- SEVERITY ---------")
    # print(f"INFO                 : {severity_counts['INFO']}")
    # print(f"WARNING              : {severity_counts['WARNING']}")
    # print(f"ERROR                : {severity_counts['ERROR']}")
    # print(f"Error percentage     : {error_percent}")
    #
    # print("\n--------- USERS ---------")
    # print(f"Most active user     : {active_user}")
    # print(f"Requests             : {active_count}")
    #
    # print("\nUsers with >3 errors:")
    # for user, count in error_users:
    #     print(f"- {user} ({count} errors)")
    #
    # print("\n--------- ENDPOINTS ---------")
    # print(f"Most accessed        : {most_accessed}")
    # print(f"Unique endpoints     : {len(unique_endpoints)}")
    # print(f"Most error-prone     : {most_error_endpoint(new_logs)}")
    #
    # print("\n--------- SUSPICIOUS ---------")
    # for user, details in suspicious_users.items():
    #     print(f"\n{user}")
    #     if 'err_percent' in details:
    #         print(f"- Error rate: {details['err_percent']}%")
    #     print("Reasons:")
    #     for reason in details['reason']:
    #         print(f"- {reason}")
    #
    # print("\n" + "=" * 40)

    return ({"total_requests":total_requests,
            "unique_users":len(unique_users),
            "unique_endpoints":len(unique_endpoints),
            "severity":{"info":severity_counts['INFO'],"warning":severity_counts['WARNING'],"error":severity_counts['ERROR'],"error_percentage":error_percent},
            "users":{"most_active_user":active_user, "requests":active_count},
            "endpoints":{"most_accessed":most_accessed,"unique_endpoints":len(unique_endpoints),"most_error_prone":most_error_endpoint(new_logs)},
            "suspicious_users":suspicious_users})

