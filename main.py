from aiogram import types, Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext    
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

from utils.db import Database
from utils.states import Registration, Unreg
from utils.navigation import startapp_keyboard, schedule_keyboard, user_choose

from tools.parsing import Parsing


from config import token
import logging


logging.basicConfig(level=logging.INFO)
bot = Bot(token)
dp = Dispatcher(bot, storage=MemoryStorage())
db = Database('tgbot_db.db')
pr = Parsing()

@dp.message_handler(commands=['start', 'help'])
async def on_start(message: types.Message):
    all_users = db.get_all_user_id()
    if message.from_id not in all_users:
        await bot.send_message(message.chat.id, 'Добро пожаловать!', reply_markup=startapp_keyboard)
    else:
        await bot.send_message(message.chat.id, 'Добро пожаловать!', reply_markup=schedule_keyboard)

@dp.message_handler(text='-Зарегистрироваться⌨️-')
async def pass_registration(message: types.Message):
    await Registration.group_name.set()
    await bot.send_message(message.chat.id, 'Введите имя группы')
@dp.message_handler(state=Registration.group_name)
async def get_reg_response(message: types.Message, state = FSMContext):
    db.add_user(
        user_id=message.from_id,
        user_name =message.from_user.full_name,
        group_name=message.text
        )
    await bot.send_message(message.chat.id, 'Вы успешно зарегистрировались!', reply_markup=schedule_keyboard)
    await state.finish()


@dp.message_handler(text='-Узнать расписание на текущую неделю🕐-')
async def get_week_couples(message: types.Message):

    schedule = pr.request_to_get_week_couples(message=message)
    print(schedule)
    for day in schedule:
        curent_week_day = day[0]['curent_week_day']  
        result_list = []
        for couple in day:
            couple_num = couple['couple_num']
            couple_time = couple['couple_time']
            couple_cabinet = couple['couple_cabinet']
            couple_name = couple['couple_name']
            couple_type = couple['couple_type']
            teacher_name = couple['teacher_name']
            schedule_message = f'\n{couple_num} {couple_time}\nАудитория: {couple_cabinet}\n{couple_name}\n{couple_type}\n\nПреподаватель: {teacher_name}\n'
            result_list.append(schedule_message)
        await message.answer(f'{curent_week_day}\n{" ".join(result_list)}')
    


@dp.message_handler(text='-Узнать расписание на сегодня🕐-')
async def get_todat_couples_func(message: types.Message):
    mess = pr.get_today_couples(message)
    if mess is None:
        await message.answer("Сегодня выходной")
    for m in mess:
        await message.answer(m)


@dp.message_handler(text='-Узнать расписание на завтра🕐-')
async def get_tommorow_couples_func(message: types.Message):
    mess = pr.get_tomorrow_couples(message)
    if mess is None:
        await message.answer("Сегодня выходной")
    for m in mess:
        await message.answer(m)


@dp.message_handler(text='-Следующая пара🕐-')
async def test_func(message: types.Message):
    mess = pr.get_next_couple(message)
    if mess is None:
        await message.answer("Сегодня выходной")
    await message.answer(mess)


@dp.message_handler(text='-Выйти❌-')
async def unreg_user(message: types.Message):
    await Unreg.user_answer.set()
    await message.answer('Данное действие удалит ваши данные из базы, вы уверены, что хотите продолжить?', reply_markup=user_choose)
@dp.message_handler(state=Unreg.user_answer)
async def unreg_user_handler(message: types.Message, state=FSMContext):
    if message.text == 'Да':
        db.delete_user_by_id(message.from_id)
        await bot.send_message(message.from_id, 'Вы успешно удалены, введите /start, если хотите зарегестрироваться',reply_markup=ReplyKeyboardRemove())
        await state.finish()
    elif message.text == 'Нет':
        await bot.send_message(message.from_id,'Действие отмененно', reply_markup=schedule_keyboard)
        await state.finish()



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)