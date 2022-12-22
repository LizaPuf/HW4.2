import re
from pprint import pprint
import csv


PHONE_REGEX = r"[7|8]\s?\(?(?P<area>\d{3})\)?[\- ]?(?P<number>[\d\- ]{7,10})(?P<ext>\(?доб. \d{4}?\)?)?"

employees = {}

with open("phonebook_raw.csv") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
for line in contacts_list[1:]:
    print(line)
    lastname, firstname, surname, organization, position, phone, email, *_ = line
    print(position)
    phone_number=''
    match =  re.search(PHONE_REGEX, phone)
    if match:
        area_code = match.group('area')
        number = match.group('number').strip().replace('-','')
        number = f"{number[0:3]}-{number[3:5]}-{number[5:]}"
        extension = match.group('ext') or ''
        extension = re.sub(r'[\(\)\s]?', '', extension)
        phone_number = f"+7({area_code}){number}{' '*bool(extension)}{extension}"
        '''
        print(phone_number)
        '''
    if not all([lastname, firstname, surname]):
        if not surname and ' ' in firstname:
            firstname, surname = firstname.split(' ')
        if not surname and not firstname:
            try:
                lastname, firstname, surname = lastname.split(' ')
            except ValueError:
                lastname, firstname = lastname.split(' ')

    print(lastname, firstname, surname, sep=',')

    if (lastname, firstname) not in employees:
        employees[(lastname, firstname)] = {}
    if surname:
        employees[(lastname, firstname)]['surname'] = surname
    if organization:
        employees[(lastname, firstname)]['organization'] = organization
    if position:
        employees[(lastname, firstname)]['position'] = position
    if phone_number:
        employees[(lastname, firstname)]['phone'] = phone_number
    if email:
        employees[(lastname, firstname)]['email'] = email


pprint(employees)
# '''
# "[7|8]\s?\(?(?P<area>\d{3})\)?[\- ]?(?P<number>[\d\- ]{7,10})(?P<ext>\(?доб. \d{4}?\)?)?"gm
# '''
employees_list =[['lastname','firstname','surname','organization','position','phone','email'],]
for (lastname, firstname), employees_data in employees.items():
    employee_record = [lastname, firstname, employees_data['surname'], employees_data['organization'], employees_data.get('position'), employees_data['phone'], employees_data.get('email')]
    employees_list.append(employee_record)

with open("phonebook.csv", "w") as f:
    datawriter = csv.writer(f, delimiter=',')
    # Вместо contacts_list подставьте свой список
    datawriter.writerows(employees_list)