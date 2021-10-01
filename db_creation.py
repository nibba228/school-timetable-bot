import sqlite3
import os
from datetime import datetime

DB_NAME = os.environ.get('DB_NAME')

con = sqlite3.connect(f'{DB_NAME}')
cur = con.cursor()

# Create tables
with open('script.sql') as file:
    sql = file.read()
    cur.executescript(sql)


# ---- Week ----
days = [
    (1, 'Понедельник'),
    (2, 'Вторник'),
    (3, 'Среда'), 
    (4, 'Четверг'), 
    (5, 'Пятница')
]

cur.executemany('insert into week (day_id, day_name) values (?, ?)', days)


# ---- Subject ----
subjects_list = [
    'Алгебра',
    'Доп математика',
    'Геометрия',
    'Моделирование',
    'Русский',
    'История',
    'Физика', 
    'Химия',
    'Английский',
    'Литература',
    'Информатика',
    'Доп информатика',
    'Физ-ра'
]

subjects_list = [(subj,) for subj in subjects_list]

subjects = {subjects_list[i][0]: i + 1 for i in range(len(subjects_list))}

cur.executemany('insert into subject (subj_name) values (?)', subjects_list)


# class day_id les_num subj_id time_start time_end
time = [None, ('9:20', '10:05'), ('10:20', '11:05'), ('11:20', '12:05'),
('12:20', '13:05'), ('13:25', '14:10'), ('14:30', '15:15'), ('15:25',
'16:10'), ('16:30', '17:15')] # len = 16


# ---- Monday ----

monday2 = [
    ['11в2', 1, 1, None, None, time[i][0], time[i][1]]
    for i in range(1, len(time) + 1)
    if i <= 6
]


monday2[0][3] = monday2[1][3] = subjects['Алгебра']
monday2[2][3] = monday2[3][3] = subjects['Английский']
monday2[4][3] = monday2[5][3] = subjects['Информатика']

monday2[0][4] = monday2[1][4] = '305'
monday2[2][4] = monday2[3][4] = '406-A'
monday2[4][4] = monday2[5][4] = '400'

monday1 = [
    ['11в1', 1, i, None, None, time[i][0], time[i][1]]
    for i in range(1, len(time) + 1)
    if i <= 6
]

monday1[0][3] = monday1[1][3] = subjects['Информатика']
monday1[2][3] = monday1[3][3] = subjects['Алгебра']
monday1[4][3] = monday1[5][3] = subjects['Физика']

monday1[0][4] = monday1[1][4] = '400'
monday1[2][4] = monday1[3][4] = '305'
monday1[4][4] = monday1[5][4] = '305'

monday = monday1 + monday2 + [['11в', 1, 8, subjects['Доп информатика'], '400', time[8][0], time[8][1]]]


# ---- Tuesday ----

tuesday2 = [
    ['11в2', 2, i, None, None, time[i][0], time[i][1]]
    for i in range(1, len(time) + 1)
    if i <= 4
]

tuesday2[0][3] = tuesday2[1][3] = subjects['Геометрия']
tuesday2[2][3] = tuesday2[3][3] = subjects['Физика']

tuesday2[0][4] = tuesday2[1][4] = '305'
tuesday2[2][4] = tuesday2[3][4] = '311'

tuesday1 = [
    ['11в1', 2, i, None, None, time[i][0], time[i][1]]
    for i in range(1, len(time) + 1)
    if i <= 4
]

tuesday1[0][3] = subjects['Моделирование']
tuesday1[0][4] = '303'
tuesday1[1][3] = subjects['Английский']
tuesday1[1][4] = '401'
tuesday1[2][3] = tuesday1[3][3] = subjects['Геометрия']
tuesday1[2][4] = tuesday1[3][4] = '305'

tuesday = [
    ['11в', 2, 5, subjects['Физ-ра'], 'Большой зал', time[5][0], time[5][1]],
    ['11в', 2, 6, subjects['Литература'], '106', time[6][0], time[6][1]],
    ['11в', 2, 7, subjects['Литература'], '106', time[7][0], time[7][1]]
]

tuesday += (tuesday1 + tuesday2)


# ---- Wednesday ----
wednesday = [
    ['11в', 3, 1, subjects['Химия'], '305', time[1][0], time[1][1]],
    ['11в', 3, 2, subjects['Химия'], '305', time[2][0], time[2][1]],
    ['11в', 3, 7, subjects['Русский'], '106', time[7][0], time[7][1]]
]

wednesday2 = [
    ['11в2', 3, 3, subjects['Алгебра'], '204', time[3][0], time[3][1]],
    ['11в2', 3, 4, subjects['Алгебра'], '204', time[4][0], time[4][1]],
    ['11в2', 3, 5, subjects['Физика'], '311', time[5][0], time[5][1]],
    ['11в2', 3, 6, subjects['Физика'], '311', time[6][0], time[6][1]],
    ['11в2', 3, 8, subjects['Доп математика'], '204', time[8][0], time[8][1]]
]

wednesday1 = [
    ['11в1', 3, 3, subjects['Алгебра'], '305', time[3][0], time[3][1]],
    ['11в1', 3, 4, subjects['Алгебра'], '305', time[4][0], time[4][1]],
    ['11в1', 3, 5, subjects['Информатика'], '400', time[5][0], time[5][1]],
    ['11в1', 3, 6, subjects['Информатика'], '400', time[6][0], time[6][1]],
    ['11в1', 3, 8, subjects['Доп математика'], '305', time[8][0], time[8][1]]
]

wednesday += (wednesday1 + wednesday2)

# ---- Thursday ----

thursday = [
    ['11в', 4, 5, subjects['Русский'], '305', time[5][0], time[5][1]],
    ['11в', 4, 6, subjects['Русский'], '305', time[6][0], time[6][1]],
    ['11в', 4, 7, subjects['История'], '305', time[7][0], time[7][1]]
]

thursday2 = [
    ['11в2', 4, 1, subjects['Физика'], '311', time[1][0], time[1][1]],
    ['11в2', 4, 2, subjects['Физика'], '311', time[2][0], time[2][1]],
    ['11в2', 4, 3, subjects['Алгебра'], '208', time[3][0], time[3][1]],
    ['11в2', 4, 4, subjects['Геометрия'], '208', time[4][0], time[4][1]]
]

thursday1 = [
    ['11в1', 4, 1, subjects['Английский'], '305', time[1][0], time[1][1]],
    ['11в1', 4, 2, subjects['Физика'], '305', time[2][0], time[2][1]],
    ['11в1', 4, 3, subjects['Алгебра'], '305', time[3][0], time[3][1]],
    ['11в1', 4, 4, subjects['Геометрия'], '305', time[4][0], time[4][1]]
]

thursday += (thursday1 + thursday2)

# ---- Friday ----

friday = [
    ['11в', 5, 3, subjects['Физ-ра'], 'Большой зал', time[3][0], time[3][1]],
    ['11в', 5, 4, subjects['История'], '305', time[4][0], time[4][1]],
    ['11в', 5, 5, subjects['Литература'], '106', time[5][0], time[5][1]],
    ['11в', 5, 6, subjects['Русский'], '106', time[6][0], time[6][1]]
]

friday2 = [
    ['11в2', 5, 1, subjects['Информатика'], '400', time[1][0], time[1][1]],
    ['11в2', 5, 2, subjects['Информатика'], '400', time[2][0], time[2][1]],
    ['11в2', 5, 7, subjects['Моделирование'], '303', time[7][0], time[7][1]]
]

friday1 = [
    ['11в1', 5, 1, subjects['Физика'], '305', time[1][0], time[1][1]],
    ['11в1', 5, 2, subjects['Физика'], '305', time[2][0], time[2][1]],
    ['11в1', 5, 7, subjects['Английский'], '401', time[7][0], time[7][1]]
]

friday += (friday1 + friday2)

# -----------------------

week_days = [monday, tuesday, wednesday, thursday, friday]
week = []
for day in week_days:
    week_day = []
    for lesson in day:
        week_day.append(tuple(lesson))
    week += week_day


cur.executemany(
    '''
    insert into lesson(class, day_id, les_num, subj_id, room, time_start, time_end)
    values (?, ?, ?, ?, ?, ?, ?)
    ''', week
)

con.commit()
cur.close()
con.close()