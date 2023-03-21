from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from generator import anekdot_gen

bot = Bot('6233348578:AAEZzlelRQGlhYlFeWqt0RVaN3tgaYkBius')
dp = Dispatcher(bot, storage=MemoryStorage())

class FSMadmin(StatesGroup):
    text = State()

@dp.message_handler(state = '*', commands=['start'])
async def start(message: types.Message):
    await message.answer('Привет. Я умею только продолжать анек после команды: /gen')

@dp.message_handler(commands=['gen'])
async def gen(message: types.Message):
    await message.answer('Напиши начало анекдота:')
    await FSMadmin.text.set()

@dp.message_handler(state = FSMadmin.text)
async def gen_state(message: types.Message, state: FSMContext):
    anekdot_st= message.text
    anekdot = anekdot_gen(anekdot_st)
    anekdot.generation()
    await message.answer(anekdot.anek_ed)
    await message.answer('Привет. Если хочешь продолжить еще один анек, пиши: /gen')
    await state.finish() 


@dp.message_handler()
async def error(message: types.Message):
    await message.answer('Команда не существует')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

#Простенький бот, позволяющий пользоваться функционалом нейронки в асинхронном режиме