# from datetime import datetime
# from module.mongoDB.get_mongodb import get_data_mongo

# def main():
#     try:
#         get_data_mongo()
#     except Exception as e:
#         print(e)

# main()

import yaml
import requests
from datetime import datetime, timedelta, date

from model.model_mongo import connect_mongodb

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

CONFIG_FILE = "./config.yaml"
# CONFIG_FILE = "./config.yaml"

 
try:
    file_stream = open(CONFIG_FILE, "r", encoding='utf-8')
    # Load configuration into config
    Config = yaml.load(file_stream, Loader=Loader)
    file_stream.close()
except Exception as e:
    print("Read configuration file error:", e)
    exit(1)

def get_data_mongo():
    try:
        cluster = connect_mongodb()
        db = cluster["healthscore"]
        collection = db["summary_alert_data"]
        # datetoday = datetime.now().strftime("%Y-%m-%d")
        datetoday = str(date.today())
        yesterday = str(date.today() - timedelta(days=1))
        ### Query Date
        select_query_today = collection.find({"date":str(datetoday)})
        select_query_yesterday = collection.find({"date": str(yesterday)})

        result_today = list(select_query_today)
        result_yesterday = list(select_query_yesterday)

        # project_name = []
        
        # topic_today = "\U0001F7E2" + " Summary Alert " + datetoday + " \U0001F7E2"
        # topic_yesterday = "\U0001F7E2" + " Summary Alert " + yesterday + " \U0001F7E2"
        project_today = "\n" + "Daily Alert Report" + "\n"
        # project_yesterday = topic_yesterday + "\n"
        seq = 0
        count_today = 0
        count_yesterday = 0
        # count_diff = abs(len(result_today) - len(result_yesterday))
        # count_max = max(len(result_today), len(result_yesterday))
        message = ""
        list_today = []
        list_yesterday = []
        list_str_eq = []
        
        for i in result_today:
            try:
                list_today.append(i['project'])
                list_str_eq.append([i['project'], i['date_time'].strftime("%Y-%m-%d %H:%M:%S")])
                # print(i['date_time'])
            except Exception as e:
                print(e)
            # seq+=1
            # message = str(seq) +". " + i['project']
            # project_today += message + "\n"

        for j in result_yesterday:
            list_yesterday.append(j['project'])

        list_notmath = returnNotMatch(list_yesterday ,list_today)
        not_math_yesterday = list_notmath[0]
        not_math_today = list_notmath[1]
        # list_notmath = str(list_notmath).strip("[[[' '' , '' '']]]")   
        count_for_loop = 0
        time_stamp = ""
        for k in list_today:
            if k in list_yesterday and k not in list_notmath:
                if k in list_str_eq[count_for_loop][0]:
                        seq+=1
                        message = str(seq) +". "+"Bot Name : " + k 
                        time_stamp = "         Timestamp : " + list_str_eq[count_for_loop][1]
                        project_today += message +"\n" + "   \U0001F7E2" + " Status : running" + "\n" + time_stamp + "\n"
                        count_for_loop+=1
            
            else:
                # if k in not_math_today:
                    seq+=1
                    message = str(seq) +". " +"Bot Name : " + not_math_today[count_today]
                    time_stamp = "         Timestamp : " + list_str_eq[count_for_loop][1]
                    project_today += message  + "\n" + "   \U0001F534" + " Status : stop" +"\n" + time_stamp + "\n"
                    count_today+=1
                # for i in list_notmath:
                #     message = str(seq) +". " + i + " \U0001F534"
                #     project_today += message + "\n"
        # project_today += str(seq+1) +". " + list_notmath + " \U0001F534"
        
        for i in list_yesterday:
            if i in not_math_yesterday:
                seq+=1
                message = str(seq) +". " +"Bot Name : " + not_math_yesterday[count_yesterday]
                time_stamp = "          Timestamp : " + list_str_eq[count_for_loop][1]
                project_today += message + "\n" + "   \U0001F534" + " Status : stop" +"\n" + time_stamp + "\n"
                count_yesterday+=1
        seq=0
        count_for_loop = 0
        # print(type(result_yesterday[0]['project']))
        
        ## Alert Diff 
        # if count_diff != 0:
        #     project_today += "Alert Diff : " + str(list_notmath).strip("[[[' ' , ' ']]]") + "\n"
        # else:
        #     project_today += "Alert Diff : " + str(count_diff) + "\n"
        # send_to_line(project_today)
        print(project_today)
        # print(list_notmath)
        # print(not_math_yesterday)
    except Exception as e:
        print(e)

line_token = Config['line']['token']

def send_to_line(project_today):
    try:
        msg = project_today
        url = 'https://notify-api.line.me/api/notify'
        token = line_token
        headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
        requests.post(url, headers=headers, data = {'message':msg})
        # print(msg)
    except Exception as e:
        print(e)


def returnNotMatch(list_yesterday, list_today):
    return [[i for i in list_yesterday if i not in list_today],[i for i in list_today if i not in list_yesterday]]



get_data_mongo()