import requests
from bs4 import BeautifulSoup
import json
import os
import json
import time
import random
import csv

def login():
    mobile_agent = (
        'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; SCH-I535 '
        'Build/KOT49H) AppleWebKit/534.30 (KHTML, like Gecko) '
        'Version/4.0 Mobile Safari/534.30'
    )
    s.headers.update({
        'User-Agent': mobile_agent,
        'X-RestLi-Protocol-Version': '2.0.0'
    })
    response = s.get('https://www.linkedin.com/login/')
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_param = soup.find('input', {'name': 'loginCsrfParam'})['value']
    payload = {
        'session_key': my_login['email'],
        'session_password': my_login['password'],
        'isJsEnabled': 'false',
        'loginCsrfParam': csrf_param
    }
    response = s.post(
        'https://www.linkedin.com/checkpoint/lg/login-submit?loginSubmitSource=GUEST_HOME',
        data=payload, 
        allow_redirects=False
    )
    print(f'Status: {response.status_code} - {"Login realizado sucesso" if response.status_code == 303 else "Login não realizado"}')
    return response.status_code

def logout():
    response = s.get('https://www.linkedin.com/logout/')
    print(s.cookies['csrfToken'])
    print(f'Status: {response.status_code} - {"Logout realizado sucesso" if response.status_code == 303 else "Logout não realizado"}')

def profile(username):
    path = f'in/{username}'
    url = f'https://www.linkedin.com/{path}'
    while True:
        response = s.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            try:
                enterprise = (soup.find('span', attrs={'class': 'member-current-company'}).text).replace('\n', '').replace(' ', '')
            except:
                enterprise = 'Não informado'
            job = (soup.find('dd', attrs={'class': 'medium'}).text).replace('\n', '')
            break
        elif response.status_code == 400:
            return {
                'code': 400
            }
    return {
        'code': 200,
        'job':job, 
        'enterprise':enterprise,
    }

def candidates(file='candidatos.txt'):
    archive = f'{local}/{file}'
    txt = open(archive, 'r')
    list_txt = txt.readlines()
    for people in list_txt:
        id = people.split('/')[4]
        info = profile(id)
        if info['code'] == 200:
            data = [
                id,
                info["job"],
                info["enterprise"]
            ]
            print(f'\nID: {id}\nJob: {info["job"]}\nEnterprise: {info["enterprise"]}\n')
        elif info['code'] == 400:
            data = {
                id,
                'Error: 400 Bad Request'
            }
            print(f'\nError: 400 Bad Request\nID: {id}\n')
        write_csv(data)

def candidate(id):
    info = profile(id)
    if info['code'] == 200:
        data = [
            id,
            info["job"],
            info["enterprise"]
        ]
        print(f'\nid: {id}\nJob: {info["job"]}\nEnterprise: {info["enterprise"]}\n')
    elif info['code'] == 400:
        data = {
            id,
            'Error: 400 Bad Request'
        }
        print(f'\nError: 400 Bad Request\nID: {id}\n')
    write_csv(data)

def verify_csv():
    archive = f'{local}/candidatos.csv'
    if os.path.exists(archive):
        return True
    else:
        return False

def write_csv(data):
    verify = verify_csv()
    archive = f'{local}/candidatos.csv'
    if verify == False:
        create_csv = open(archive, 'w')
        create_csv.close()
    with open(archive, 'a', newline='\n') as csv_file:
        csv_reader = csv.writer(csv_file, delimiter=';')
        csv_reader.writerow(data)

my_login = {
    #'email': 'recrutadoreficiente@gmail.com',
    #'password': 'Paris#123'
    'email': 'farias.mts@outlook.com',
    'password': 'Eleven12'
}
local = os.path.dirname(os.path.realpath(__file__))
s = requests.Session() 
code = login()
if code == 303:
    #candidate('thisfarias')
    candidates()

