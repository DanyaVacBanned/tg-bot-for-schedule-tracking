from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton



startapp_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
reg_button = KeyboardButton('-Зарегистрироваться⌨️-')
startapp_keyboard.add(reg_button)

schedule_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
week_schedule = KeyboardButton('-Узнать расписание на текущую неделю🕐-')
today_schedule = KeyboardButton('-Узнать расписание на сегодня🕐-')
tomorrow_schedule = KeyboardButton('-Узнать расписание на завтра🕐-')
next_schedule = KeyboardButton('-Следующая пара🕐-')
unreg_button = KeyboardButton('-Выйти❌-')
schedule_keyboard.add(week_schedule).add(today_schedule).add(tomorrow_schedule).add(next_schedule).add(unreg_button)

user_choose = ReplyKeyboardMarkup(resize_keyboard=True)
yes_btn = KeyboardButton('Да')
no_btn = KeyboardButton('Нет')
user_choose.add(yes_btn, no_btn)
