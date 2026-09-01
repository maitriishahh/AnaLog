from logs import logs
from analytics.parse import parse_logs

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


def analysis():
    return (get_total_requests(new_logs),
    get_total_user_requests(new_logs),
    most_active_user(new_logs),
    get_unique_user_request(new_logs),
    get_most_accessed_point(new_logs),
    get_unique_endpoints(new_logs),
    analyze_severity(new_logs),
    calc_error_percent(total, errors),
    most_error_user(new_logs),
    filter_users(new_logs),
    most_error_endpoint(new_logs),
    group_severity(new_logs),
    find_suspicious_activity(new_logs))
