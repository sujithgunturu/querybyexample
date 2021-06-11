import json

db_list = []

def get(value):
    for data in db_list:
        flag = True
        for k, v in value.items():
            if isinstance(v, dict):
                for i_k, i_v in v.items():
                    try:
                        if data[k][i_k] != i_v:
                            flag = False
                            continue
                    except:
                        pass
            elif isinstance(v, list):
                for i in v:
                    if i not in data["list"]:
                        flag = False
                        continue
            elif data.get(k) != v:
                flag = False
                continue
        # If a match is present, printing that data
        if flag:
            data = json.dumps(data, separators=(',', ':'))
            print(data)


def add(value):
    db_list.append(value)
from copy import deepcopy
def delete(value):
    global db_list
    tempdb = deepcopy(db_list)
    
    for data in tempdb:
        flag = True
        for k, v in value.items():
            if isinstance(v, dict):
                for i_k, i_v in v.items():
                    try:
                        if data[k].get(i_k) != i_v:
                            flag = False
                            continue
                    except:
                         continue   
            if isinstance(v, list):
                for i in v:
                    if i not in data["list"]:
                        flag = False
                        continue
            elif data.get(k) != v:
                flag = False
                continue
        if flag and data in db_list:
            db_list.remove(data)
    
def get_inputs(entire_command):
    if not entire_command:
        return
    ind = entire_command.index('{')
    command, value = entire_command[:ind-1], json.loads(entire_command[ind:])
    if command == 'get':
        get(value)
    elif command == 'add':
        add(value)
    elif command == 'delete':
        delete(value)
    else:
        return
import sys as sys
for line in sys.stdin:
    get_inputs(line)