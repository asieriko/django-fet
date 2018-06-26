import gspread
from oauth2client.service_account import ServiceAccountCredentials
from timetabledata.models import Data, Teacher

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
client_file = '/home/asier/Hezkuntza/python-hezkuntza/django-fet/client_id.json'
creds = ServiceAccountCredentials.from_json_keyfile_name(client_file, scope)
client = gspread.authorize(creds)

SNAME = "15OemBxVJY7zK4oZ7ydDvctLKxS9ypnQ87laIehLYLbA"
teachersheetname = 'ComplementariasYRestricciones'
SURL = 'https://docs.google.com/spreadsheets/d/1ti3QH2y0U4IVaPRgVhinrCgQBIsAoBQIXzr3IsBP5SQ'


def loadDriveData():
    # use creds to create a client to interact with the Google Drive API
    creds = ServiceAccountCredentials.from_json_keyfile_name(client_file, scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key(SNAME).sheet1

    # Extract and print all of the values
    rlist = sheet.get_all_records()

    errors = []
    for row in rlist:
        try:
            if row["Irakaslea"] == '':
                #print(row)
                continue
            Data.objects.create_data(row)

        except Exception as inst:
            print(inst)
            print(row)
            errors.append([inst, row])

    return rlist, errors

    #{'': 21,
    #'Lehenengoa': 628,
    #'Helbidea': '"https://docs.google.com/spreadsheets/d/1ti3QH2y0U4IVaPRgVhinrCgQBIsAoBQIXzr3IsBP5SQ"',
    #'Mintegia': 'Bio Geo',
    #'Irakaslea': 'Eugenio Miranda',
    #'Orduak': 2,
    #'Aula': '1_3A',
    #'Loturak': '',
    #'Oharrak': '',
    #'Kopurua': 49,
    #'Taldea': '3A',
    #'Maila': '3.DBH',
    #'Tipo': 'independiente',
    #'Eredua': 'AG',
    #'OharrakMintegitik': '',
    #'Ikasgaia': 'Bio Geo',
    #'AgrupacionEDUCA': ''}


def loadDriveTeachers():
    # use creds to create a client to interact with the Google Drive API
    creds = ServiceAccountCredentials.from_json_keyfile_name(client_file, scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key(SNAME).worksheet(teachersheetname)

    # Extract and print all of the values
    rlist = sheet.get_all_records()

    errors = []
    for row in rlist:
        print(row)
        try:
            if row["Irakaslea"] == '':
                #print(row)
                continue
            Teacher.objects.update_teacher(row)

        except Exception as inst:
            print(inst)
            print(row)
            errors.append([inst, row])

    return rlist, errors


    #{'': '',
    #'Irakaslea': 'Mariaje Ruiz',
    #'Zaintza_Kop': 1,
    #'NumHoras': 20,
    #'Z1': 1,
    #'Z12': 0,
    #'Max_Dias_Sem': '',
    #'Max_intervalo_dia': '',
    #'CompTutoría': 3,
    #'compensacion_gt_20': 0,
    #'HorasContrato': 20,
    #'Complementarias': '',
    #'Reducción': 0,
    #'Max_horas_dia': '',
    #'Edificios': 1,
    #'HorasTutoria': 3,
    #'Mas_It_Sem': 1,
    #'Max_huecos_semana': '',
    #'Z2': 0,
    #'Max_huecos_días': ''}
#