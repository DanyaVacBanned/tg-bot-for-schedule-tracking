import requests
from fake_useragent import UserAgent
from aiogram import types
from utils.db import Database
from bs4 import BeautifulSoup as b
import datetime

class Parsing:
    def __init__(self) -> None:
        self.db = Database('tgbot_db.db')

    def request_to_get_week_couples(self,message: types.Message):
        ua = UserAgent()
        group_name = self.db.get_user_group_by_id(message.from_id)
        headers = {
            'User-Agent':ua.random
            }
        r = requests.get(f'https://rasp.pgups.ru/search?title={group_name}&by=group', headers=headers)
        print(r)
        soup = b(r.text, 'lxml')
        this_week = soup.find('span',{'id':'kt_dashboard_daterangepicker_date'}).text
        if this_week == 'Нечетная неделя':
            odd = 1
        else:
            odd = 0
        
        a = soup.find('a',{'class':'kt-link'})
        r = requests.get(f"{a.get('href')}?odd={odd}", headers=headers)
        print(r)
        soup = b(r.text, 'lxml')
        all_days = soup.find_all('table', {'class':'table m-table mb-5'})

        result = []
        for day in all_days:

            curent_day = []
            tr = day.find_all('tr')
            if tr == []:
                break
            try:
                curent_week_day = day.find('h4').text.strip()
            except:
                pass
            for row in tr:

                try:
                    couple_num = row.find('div',{'class':'text-center align-middle'}).text.strip()
                    couple_time = row.find('div',{'class':'text-center kt-shape-font-color-4'}).text.strip()
                    try:
                        couple_cabinet = row.find('div',{'class':'text-center mt-2'}).text.strip()
                    except:
                        couple_cabinet = 'Аудитория не указана'
                    couple_name = row.find('span',{'class':'mr-1'}).text.strip()
                    couple_type = row.find('span',class_='badge-pill').text.strip()
                    try:
                        teacher_name = row.find_all('a',{'class':'kt-link'})[1].text.strip()
                    except:
                        teacher_name = 'Преподаватель не назначен'
                except:
                    pass
                curent_day.append(
                    {
                    'curent_week_day':curent_week_day,
                    'couple_num':couple_num,
                    'couple_time':couple_time,
                    'couple_cabinet':couple_cabinet,
                    'couple_name':couple_name,
                    'couple_type':couple_type,
                    'teacher_name':teacher_name,
                    }
                    )
                
            result.append(curent_day)
            
        return result
    


    def get_today_couples(self, message: types.Message):
        week_day_number = message.date.weekday()
        if week_day_number in [5,6]:
            return None
        week = ['Понедельник', 'Вторник', 'Среда','Четверг','Пятница','Cуббота','Воскресенье']
        result = []
        req = self.request_to_get_week_couples(message=message)
        for day in req:
            if day[0]['curent_week_day'] == week[week_day_number]:
                for couple in day:
                    couple_num = couple['couple_num']
                    couple_time = couple['couple_time']
                    couple_cabinet = couple['couple_cabinet']
                    couple_name = couple['couple_name']
                    couple_type = couple['couple_type']
                    teacher_name = couple['teacher_name']
                    schedule_message = f'{week[week_day_number]}\n{couple_num} {couple_time}\nАудитория: {couple_cabinet}\n{couple_name}\n{couple_type}\n\nПреподаватель: {teacher_name}\n'
                    result.append(schedule_message)
                return result
            else:
                continue
        return f'Сегодня {week[week_day_number].lower()}, пар нет!'

    def get_tomorrow_couples(self, message: types.Message):
        week_day_number = message.date.weekday()+1
        if week_day_number in [5,6]:
            return None
        result = []
        week = ['Понедельник', 'Вторник', 'Среда','Четверг','Пятница','Cуббота','Воскресенье']
        req = self.request_to_get_week_couples(message=message)
        for day in req:
            if day[0]['curent_week_day'] == week[week_day_number]:
                for couple in day:
                    couple_num = couple['couple_num']
                    couple_time = couple['couple_time']
                    couple_cabinet = couple['couple_cabinet']
                    couple_name = couple['couple_name']
                    couple_type = couple['couple_type']
                    teacher_name = couple['teacher_name']
                    schedule_message = f'{week[week_day_number]}\n{couple_num} {couple_time}\nАудитория: {couple_cabinet}\n{couple_name}\n{couple_type}\n\nПреподаватель: {teacher_name}\n'
                    result.append(schedule_message)
                return result
            else:
                continue
        return f'завтра {week[week_day_number].lower()}, пар нет!'
    

    def get_next_couple(self, message: types.Message):
        
        curent_time = datetime.datetime.strptime(str(message.date), '%Y-%m-%d %H:%M:%S').time()
        print(curent_time)
        week_day_number = message.date.weekday()
        if week_day_number in [5,6]:
            return None
        week = ['Понедельник', 'Вторник', 'Среда','Четверг','Пятница','Cуббота','Воскресенье']
        req = self.request_to_get_week_couples(message=message)
        for day in req:
            if day[0]['curent_week_day'] == week[week_day_number]:
                for couple in day:
                    start_time = datetime.datetime.strptime(couple['couple_time'].split()[0], "%H:%M").time()
                    end_time = datetime.datetime.strptime(couple['couple_time'].split()[2], '%H:%M').time()
                    couple_num = couple['couple_num']
                    couple_time = couple['couple_time']
                    couple_cabinet = couple['couple_cabinet']
                    couple_name = couple['couple_name']
                    couple_type = couple['couple_type']
                    teacher_name = couple['teacher_name']
                    if (curent_time <= start_time):
                        schedule_message = f'{week[week_day_number]}\n{couple_num} {couple_time}\nАудитория: {couple_cabinet}\n{couple_name}\n{couple_type}\n\nПреподаватель: {teacher_name}\n'
                        return schedule_message









    
