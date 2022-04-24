import os
import pwd
import grp
import configparser
import datetime as dt

config = configparser.ConfigParser()
config.read('project.ini')

try:
    output_path = config['PATHS']['OUTPUT_PATH']
except KeyError:
    output_path = os.getcwd()

print(output_path)

def system_accounts():
    try:
        inp = '\nUsers : Groups\n\n'
        users = []
        user_gid = {}
        for p in pwd.getpwall():
            users.append(p[0])
            user_gid[p[0]] = p[3]

        try:
            if config['FILTER_ACCOUNTS']['sortAccountsCriteria'] == 'name':
                users.sort()
        except:
            pass

        try:
            if config['FILTER_ACCOUNTS']['sortAccountsReverse'] == 'True':
                users.reverse()
        except:
            pass

        lines=0
        try:
            lines = config['FILTER_ACCOUNTS']['linesOfAccountsData']
        except:
            pass
        
        if not lines == 'All':
            lines = int(lines)

            for user in users:
                if(lines == 0):
                    break
                inp += (user + ' - ' + grp.getgrgid(user_gid[user])[0] +'\n')
                lines-=1
            print(inp)
        else: 
            for user in users:
                inp += (user + ' - ' + grp.getgrgid(user_gid[user])[0] +'\n') 
            print(inp)
        return inp
    except Exception as e:
        print("ERROR!")
        print(e)
    pass

def system_logs():
    try:
        start_time_str = config['FILTER_LOGS']['logTimeFrom']
        end_time_str = config['FILTER_LOGS']['logTimeTo']
        max_lines = config['FILTER_LOGS']['logMaxLines']
        log_type = config['FILTER_LOGS']['logCriteria']
        rev = config['FILTER_LOGS']['sortLogsReverse']
    except Exception as e:
        print(e)
        raise(Exception('Logs Config Not Valid !'))

    os.system(f'tail -n{max_lines} /var/log/{log_type} >> {os.getcwd()}/temp.txt')

    logs = open('temp.txt','r').readlines()
    start_time = dt.datetime.strptime(start_time_str,'%b %d %H:%M:%S')
    end_time = dt.datetime.strptime(end_time_str,'%b %d %H:%M:%S')
    
    result = []
    for line in logs:
        timestamp_str = line[:15]
        timestamp = dt.datetime.strptime(timestamp_str,'%b %d %H:%M:%S')
        if timestamp >= start_time and timestamp <= end_time:
            result.append(line)

    if rev == 'True':
        result.reverse()

    for i in result:
        print(i)
    
    os.remove('temp.txt')

    return result

def generate_report():
    pass

if __name__ == '__main__':
    menu = open('menu.txt','r').read()
    while True:
        print(menu)
        inp = input()
        if not inp:
            print("Bye!")
            exit()
        inp = int(inp)

        if inp == 1:
            system_accounts()

        if inp == 2:
            system_logs()

        if inp == 3:
            generate_report()