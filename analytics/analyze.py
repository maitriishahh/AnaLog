import time
from fastapi import Request
from datetime import datetime
def get_total_requests(lst):
    return len(lst)

def get_total_user_requests(lst):
    total_user_req = {}
    for log in lst:
        user = log['user_id']
        if user is not None:
            if user in total_user_req:
                total_user_req[user]+=1
            else:
                total_user_req[user] = 1
    return total_user_req

def most_active_user(dct):
    count = 0
    user = None
    for k,v in dct.items():
        if v > count:
            count = v
            user = k
    return user, count

def get_unique_user_request(lst):
    unique_users = set()
    for log in lst:
        user = log['user_id']
        if user is not None:
            unique_users.add(user)
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
    endpoints = set()
    for log in lst:
        endpoints.add(log['endpoint'])
    return endpoints

# get_ep = [i['endpoint'] for i in new_logs]
# print(get_ep)

def analyze_severity(lst):
    severity_count = {}
    for log in lst:
        level = log['level']
        if level in severity_count:
            severity_count[level]+=1
        else:
            severity_count[level] = 1
    return severity_count

def calc_error_percent(total_req, error_count):
    if total_req == 0:
        return 0

    error_percentage = (error_count/total_req)*100
    return error_percentage

def most_error_user(lst):
    error_users = {}
    for log in lst:
        error_level = log['level']
        error_user = log['user_id']
        if error_level == 'ERROR' and error_user is not None:
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

def group_severity(lst):
    groups = {}
    for log in lst:
        level = log['level']
        if level not in groups:
            groups[level] = []
        groups[level].append(log)
    return groups

def most_error_endpoint(lst):
    endpoint_error = {}
    most_error_ep = None
    highest_count = 0
    for log in lst:
        error_level = log['level']
        error_ep = log['endpoint']
        if error_level == 'ERROR':
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
    err_counts = most_error_user(lst)
    total_user_reqs = get_total_user_requests(lst)
    for user, user_err in err_counts.items():
        user_req = total_user_reqs[user]
        err_percent = round((user_err / user_req) * 100,2)
        sus_user = {'reason': []}
        if user_err > 3:
            sus_user['reason'].append('More than 3 errors')
        if err_percent > 50:
            sus_user['err_percent'] = err_percent
            sus_user['reason'].append('Error rate above 50%')
        if sus_user['reason']:
            users[user] = sus_user
    return users

def slow_request(lst):
    slow_reqs = []
    for log in lst:
        if log['response_time'] > 1000:
            slow_reqs.append(log)
    return slow_reqs

def slow_endpoints(lst):
    slow_eps = {}
    highest_time = 0
    slowest_ep = None
    for log in lst:
        if log['response_time'] > 1000:
            endpoint = log['endpoint']
            if endpoint in slow_eps:
                slow_eps[endpoint]+=1
            else:
                slow_eps[endpoint]=1
            if log['response_time'] > highest_time:
                highest_time = log['response_time']
                slowest_ep = log
    return slow_eps, slowest_ep, highest_time
