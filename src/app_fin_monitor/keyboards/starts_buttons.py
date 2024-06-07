from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lexicon.lexicon import LEXICON

def get_start_actions() -> ReplyKeyboardMarkup:
    kb_actions = ReplyKeyboardBuilder()
    kb_actions.button(text=LEXICON['to_stoks'])
    kb_actions.button(text=LEXICON['to_create_report'])
    kb_actions.adjust(1)
    return kb_actions.as_markup(resize_ketboard=True, one_time_keyboard=True)
