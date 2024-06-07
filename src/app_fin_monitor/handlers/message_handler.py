from aiogram import Router, F
from aiogram.filters import Command
from lexicon import LEXICON
from aiogram.types import Message
from keyboards.starts_buttons import get_start_actions
from keyboards.inline_buttons import create_inline_kb
from db.db_contrrol import create_single_table

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(LEXICON["start"], reply_markup=get_start_actions())


@router.message(F.text == LEXICON["to_stoks"])
async def answer_list_tiker(message: Message):
    await message.answer(
        LEXICON["choise_action"],
        reply_markup=create_inline_kb(
            2,
            "create_new_lst_stoks",
            "edit_lst_stoks",
            "remove_lst_stoks",
        ),
    )


@router.message(F.text == LEXICON["to_create_report"])
async def answer_create_report(message: Message):
    await message.answer(
        LEXICON["choise_report"],
        reply_markup=create_inline_kb(
            2,
            "hlaf_year_report",
            "year_report",
            "all_time_report",
        ),
    )


@router.message(F.text.startswith("table_"))
async def create_new_table_lst_stk(message: Message):
    table_name = message.text.split("_")[-1]
    await create_single_table(table_name)
    await message.answer(text="Создано")
