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

