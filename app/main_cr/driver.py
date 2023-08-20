import requests
import json
from json import JSONEncoder
import datetime
from init_auth_strava_vars import *
import dateutil.parser as d_parser

def date_conv(text):
    date = d_parser.parse(text)
    return str(date.isoformat())

def time_conv(inte):
    time = datetime.timedelta(seconds=inte)
    return str(time)

def meters_conv(inte):
    miles = inte*0.000621371
    return miles

with open('app/main_cr/strava_tokens.json') as json_file:
    strava_tokens = json.load(json_file)
    bearer = strava_tokens.get('access_token')
    #close file?

class Effort:
    def __init__(self, name):
        self.effort_number = effort_number
        self.effort_id = effort_id
        self.segment_name = segment_name
        self.activity_date_time = activity_date_time
        self.activity_id = activity_id
    pass     

class DateTimeEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()

print('\n'+'CYCLING CAMP REPORTER'+'\n')
segment_id = input('please enter segment ID: ')
print('\n')
start_date = input('please enter start date (year-mo-dy): ')
print('\n')
end_date = input('please enter end date (year-mo-dy): ')
print('\n')
per_page = input('please enter results per page (Strava may reject request if too large): ')

conv_start_date = date_conv(start_date)
conv_end_date = date_conv(end_date)

response = requests.get('https://www.strava.com/api/v3/segment_efforts?segment_id=', params = {'segment_id': segment_id,'start_date_local': conv_start_date,'end_date_local': conv_end_date,'per_page': per_page}, headers={'Content-type':'application/json','Authorization': 'Bearer ' + bearer})
y = response.json()

seg_efforts_lst = []
act_count = 0
for activity in y:
    effort_number = str(act_count+1)
    effort_id = y[act_count]['id']
    segment_name = y[act_count]['name']
    activity_date_time = str(y[act_count]['start_date_local'])
    activity_id = str(y[act_count]['activity']['id'])
    print('\n')
    print('effort number: ' + effort_number)
    print('effort ID: ' + str(effort_id))
    print('segment name: ' + segment_name)
    print('activity date/time: ' + activity_date_time)
    print('activity ID: ' + activity_id)
    
    Effort(effort_number)
    seg_efforts_lst.append(Effort(effort_number))
    act_count += 1

print('\n')
seg_efforts_user_lst = input('to obtain effort data, please input the effort number(s) seperated by a space: ')
seg_efforts_user_lst = seg_efforts_user_lst.split(' ')
print('\n')

final_effort_list = []
for effort in seg_efforts_lst:
    if str(effort.effort_number) in seg_efforts_user_lst:
        final_effort_list.append(effort)
        print('effort ID: ' + str(effort.effort_id) + ' ready for insertion OR viewing')
        print('\n')

user = input('view and insert all listed efforts into database? (y): ')        

dic_list = []
if user == 'y' or 'Y':
    for effort in final_effort_list:
        seg_effort = effort.effort_id
        response = requests.get('https://www.strava.com/api/v3/segment_efforts/' + str(seg_effort), headers = {'Content-type':'application/json','Authorization': 'Bearer ' + bearer})
        y = response.json()

        effort__id = (str(y.get('id')))
        effort__name = (y.get('name'))
        athlete__username = (str(y.get('athlete')['username']))
        segment__name = (y.get('segment')['name'])
        segment__id = (str(y.get('segment')['id']))
        start__date_time = y.get('start_date_local')
        conv__elap_time = time_conv(y.get('elapsed_time'))
        conv__movi_time = time_conv(y.get('moving_time'))
        conv_effo_dist = meters_conv(y.get('distance'))
        conv__effo_dist = format(conv_effo_dist,'.2f')
        conv_segm_dist = meters_conv(y.get('segment')['distance'])
        conv__segm_dist = format(conv_segm_dist,'.2f')
        average__watts = (str(y.get('average_watts')))
        average__heartrate = str(y.get('average_heartrate'))
        max__heartrate = (str(y.get('max_heartrate')))

        new_data = {'effort id':effort__id,'effort name':effort__name,'athlete username':athlete__username,'segment name':segment__name,'segment id':segment__id,'start date/time': start__date_time,'elapsed time':conv__elap_time,'moving time':conv__movi_time,'effort distance':conv__effo_dist,'segment distance':conv__segm_dist,'average watts':average__watts,'average heartrate':average__heartrate,'max heartrate':max__heartrate}
        dic_list.append(new_data)

json_list = []
for dic in dic_list:
    json_list.append(json.dumps(dic))
print('\n') 

load_list = []
for j in json_list:
    load_list.append(json.loads(j))
print('\n') 

books_fixture = []
for i, entry in enumerate(load_list):
    book = {
        'model': 'cr_db.Ride',
        'pk': i+1,
        'fields': {
            'effort_id': entry['effort id'],
            'effort_name': entry['effort name'],
            'athlete_username': entry['athlete username'],
            'segment_name': entry['segment name'],
            'segment_id': entry['segment id'],
            'start_date_time': entry['start date/time'],
            'elapsed_time': entry['elapsed time'],
            'moving_time': entry['moving time'],
            'effort_distance': entry['effort distance'],
            'segment_distance': entry['segment distance'],
            'average_watts': entry['average watts'],
            'average_heart_rate': entry['average heartrate'],
            'max_heart_rate': entry['max heartrate']
        }
    }
    books_fixture.append(book)    

print(json.dumps(books_fixture, indent=4))

with open('app/main_cr/efforts.json', 'w') as f:
    json.dump(books_fixture, f, indent=4)         