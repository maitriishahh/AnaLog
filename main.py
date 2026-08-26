from logs import logs

def parse_logs(raw_logs):
    final_logs = []
    for log in raw_logs:
        cleaned_logs = []
        logs_dict = {}
        log = log.split('|')
        for j in log:
            cleaned_logs.append(j.strip())
        date, time = cleaned_logs[0].split(' ')
        logs_dict['date'] = date
        logs_dict['time'] = time
        logs_dict['severity'] = cleaned_logs[1]
        logs_dict['user'] = cleaned_logs[2]
        logs_dict['endpoint'] = cleaned_logs[3]
        final_logs.append(logs_dict)
    return final_logs
new_logs = parse_logs(logs)

def get_total_requests(lst):
    # count_req = 0
    # for i in lst:
    #     count_req+=1
    # return count_req
    return len(lst)

total = get_total_requests(new_logs)

def get_total_user_requests(lst):
    total_user_req = {}
    for log in lst:
        user = log['user']
        if user in total_user_req:
            total_user_req[user]+=1
        else:
            total_user_req[user] = 1
    return total_user_req

total_user_reqs = get_total_user_requests(new_logs)

def most_active_user(dct):
    count = 0
    user = None
    for k,v in dct.items():
        if v > count:
            count = v
            user = k
    return user, count

def get_unique_user_request(lst):
    unique_user_req = {}
    unique_users = set()
    for log in lst:
        user = log['user']
        unique_users.add(user)
        if user in unique_user_req:
            unique_user_req[user]+=1
        else:
            unique_user_req[user] = 1
    return unique_users

def get_most_accessed_point(lst):
    most_endpoints = {}
    highest_count = 0
    most_accessed_point = None
    for log in lst:
        ep = log['endpoint']
        if ep in most_endpoints:
            most_endpoints[ep]+=1
        else:
            most_endpoints[ep]=1
    for k,v in most_endpoints.items():
        if v > highest_count:
            highest_count = v
            most_accessed_point = k
    return most_accessed_point

def get_unique_endpoints(lst):
    unique_ep = {}
    endpoints = set()
    for log in lst:
        ep = log['endpoint']
        endpoints.add(ep)
        if ep in unique_ep:
            unique_ep[ep] += 1
        else:
            unique_ep[ep] = 1
    return endpoints

# get_ep = [i['endpoint'] for i in new_logs]
# print(get_ep)

def analyze_severity(lst):
    severity_count = {}
    for log in lst:
        sc = log['severity']
        if sc in severity_count:
            severity_count[sc]+=1
        else:
            severity_count[sc] = 1
    return severity_count

severity = analyze_severity(new_logs)
errors = severity['ERROR']

def calc_error_percent(total_req, error_count):
    error_percentage = (error_count/total_req)*100
    return f'{int(error_percentage)}%'

def most_error_user(lst):
    error_users = {}
    for log in lst:
        error_sev = log['severity']
        error_user = log['user']
        if error_sev == 'ERROR':
            if error_user in error_users:
                error_users[error_user]+=1
            else:
                error_users[error_user]=1
    return error_users

def filter_users(tup):
    k,v = tup
    if v>3:
        return True
    return False

filtered_users = filter(filter_users,most_error_user(new_logs).items())

def group_severity(lst):
    groups = {}
    for log in lst:
        type_severity = log['severity']
        if type_severity not in groups:
            groups[type_severity] = []
        groups[type_severity].append(log)
    return groups

def most_error_endpoint(lst):
    endpoint_error = {}
    most_error_ep = None
    highest_count = 0
    for log in lst:
        error_sev = log['severity']
        error_ep = log['endpoint']
        if error_sev == 'ERROR':
            if error_ep in endpoint_error:
                endpoint_error[error_ep]+=1
            else:
                endpoint_error[error_ep]=1
    for k,v in endpoint_error.items():
        if v > highest_count:
            highest_count = v
            most_error_ep = k
    return most_error_ep

def find_suspicious_activity(lst):
    users = {}
    err_counts = most_error_user(new_logs)
    for log in lst:
        user = log['user']
        user_req = total_user_reqs[user]
        if user in err_counts:
            user_err = err_counts[user]
            err_percent = (user_err / user_req) * 100
            if user not in users:
                sus_user = {'reason': []}
                if user_err > 3:
                    sus_user['reason'].append('More than 3 errors')
                    users[user] = sus_user
                if err_percent > 50:
                    sus_user['err_percent'] = err_percent
                    sus_user['reason'].append('Error rate above 50%')
                    users[user] = sus_user
    return users

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

    print("=" * 40)
    print("        SERVER LOG ANALYSIS")
    print("=" * 40)

    print(f"\nTotal requests       : {total_requests}")
    print(f"Unique users         : {len(unique_users)}")
    print(f"Unique endpoints     : {len(unique_endpoints)}")

    print("\n--------- SEVERITY ---------")
    print(f"INFO                 : {severity_counts['INFO']}")
    print(f"WARNING              : {severity_counts['WARNING']}")
    print(f"ERROR                : {severity_counts['ERROR']}")
    print(f"Error percentage     : {error_percent}")

    print("\n--------- USERS ---------")
    print(f"Most active user     : {active_user}")
    print(f"Requests             : {active_count}")

    print("\nUsers with >3 errors:")
    for user, count in error_users:
        print(f"- {user} ({count} errors)")

    print("\n--------- ENDPOINTS ---------")
    print(f"Most accessed        : {most_accessed}")
    print(f"Unique endpoints     : {len(unique_endpoints)}")
    print(f"Most error-prone     : {most_error_endpoint(new_logs)}")

    print("\n--------- SUSPICIOUS ---------")
    for user, details in suspicious_users.items():
        print(f"\n{user}")
        if 'err_percent' in details:
            print(f"- Error rate: {details['err_percent']}%")
        print("Reasons:")
        for reason in details['reason']:
            print(f"- {reason}")

    print("\n" + "=" * 40)

generate_report()