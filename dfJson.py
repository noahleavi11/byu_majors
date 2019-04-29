from bs4 import BeautifulSoup
import requests
import pandas as pd
import json

def req_num(str1):
    req = ""
    for i in str1:
        if i.isdigit():
            req = i
            break
    return (str1.find(req) + 1)

def find_element(children_list,name):
    """
    Find element in children list
    if exists or return none
    """
    for i in children_list:
        if i["name"] == name:
            return i
    #If not found return None
    return None

def add_node(path,nest):
    """
    The path is a list.  Each element is a name that corresponds
    to a level in the final nested dictionary.
    """

    #Get first name from path
    this_name = path.pop(0)

    #Does the element exist already?
    element = find_element(nest["children"], this_name)

    #If the element exists, we can use it, otherwise we need to create a new one
    if element:

        if len(path)>0:
            add_node(path, element)

    #Else it does not exist so create it and return its children
    else:

        if len(path) == 0:
            nest["children"].append({"name": this_name})
        else:
            #Add new element
            nest["children"].append({"name": this_name, "children":[]})

            #Get added element
            element = nest["children"][-1]

            #Still elements of path left so recurse
            add_node(path, element)



data = requests.get('http://catalog.byu.edu/physical-and-mathematical-sciences/statistics/statistics-data-science-bs')
soup_stat = BeautifulSoup(data.text, "html.parser")

requirements = soup_stat.find("div", { "class" : "program-requirements-container pr-level-1"} )

#create dictionary used to store major requirements with the value of course requirements
stat_requirements = {}
num = 0

df = pd.DataFrame(columns=['main_req','course_req'])
#dfObj = dfObj.append({'User_ID': 23, 'UserName': 'Riti', 'Action': 'Login'}, ignore_index=True)
for block in soup_stat.select(".program-requirements-group"):
    new_requirement = ""
    for req in block.select(".pr-instructions-depth-1"):
        req_index = req_num(req.text)
        new_requirement = req.text[0].upper() + req.text[1:req_index] + ":" + req.text[req_index:]
    for lecture in block.find_all("div", {"class" : "pr-link"}):
        new_course = lecture.text
        df = df.append({'main_req':new_requirement, 'course_req':new_course}, ignore_index=True)

d = {"name": "Stats:Data Science",
"children": []}

levels = ["main_req","course_req"]
for row in df.iterrows():
    r = row[1]
    path = list(r[levels])
    add_node(path,d)

print(json.dumps(d, sort_keys=False,
              indent=2))
