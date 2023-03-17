import json

passwords = []


with open('passwords.txt', 'r', encoding='UTF-8') as pw:
    for i in pw:
        n = i.split('\n')[0]
        if n != '':
            pw.append(n)

with open('passwords.json', 'w', encoding='UTF-8') as pwjson:
    json.dump(passwords, pwjson)