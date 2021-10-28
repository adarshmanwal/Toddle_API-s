import requests 
import json

URL="http://127.0.0.1:8000/assignment/"

# for create =============+++++
# data={
#     'description': 'first assignment',
#     'published_at': '2021-10-26',
#     'deadline_date': '2021-10-26'
# }

# json_data=json.dumps(data)
# # print("the data is in the qright from =======",json_data)
# r=requests.post(url=URL,data=json_data)
# print(" the data we get====> ",r)
# data=r.json()
# print(data)

# for update===========+++++
def get_Data(id=None):
    data={}
    if id is not None:
        data={'id':id}
    json_data=json.dumps(data) 
    r=requests.get(url=URL,data=json_data)
    data=r.json()
    print(data)

def post_data():
    data={
        'description': '4',
        'published_at': '2021-10-27',
        'deadline_date': '2021-10-28'
    }
    json_data=json.dumps(data)
    r=requests.post(url=URL,data=json_data)
    data=r.json()
    print(data)

def update_data():
    data={
        'id':4,
        'description': 'fourth uppdated assignment',
        'published_at': '2021-10-28',
        'deadline_date': '2021-10-29'
    }
    json_data=json.dumps(data)
    r=requests.put(url=URL,data=json_data)
    data=r.json()
    print(data)


def Delete_data():
    data={
        'id':4,
    }
    json_data=json.dumps(data)
    r=requests.delete(url=URL,data=json_data)
    data=r.json()
    print(data)
# get_Data()
post_data()

# update_data()

# Delete_data()