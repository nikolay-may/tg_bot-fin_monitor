from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from adapters.repository import SQLAlchemyRepository
from lexicon.lexicon import LEXICON
from keyboards.inline_buttons import create_inline_kb
from db.db_contrrol import show_all_table, drop_tables

router = Router()


class ControlWorkStok(StatesGroup):
    create_new_list_stok = State()
    edit_list_stok = State()
    remove_stok = State()


@router.callback_query(F.data == "create_new_lst_stoks")
async def request_new_table_name(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="Отправьте в сообщении имя новой таблице в формате - table_ИмяТаблицы"
    )
    await state.set_state(ControlWorkStok.create_new_list_stok)
    await callback.answer()


@router.callback_query(F.data == "edit_lst_stoks")
async def edit_lst_stk(callback: CallbackQuery, state: FSMContext):
    btn = [record for record in await show_all_table()]
    state.set_data(table_name=[*btn])
    await callback.message.answer(
        text=LEXICON["choise_lst_to_edit"],
        reply_markup=create_inline_kb(
            2,
            *btn,
        ),
    )
    await state.set_state(ControlWorkStok.edit_list_stok)
    await callback.answer()  # session/repositiory  delete/update record  for stoks


@router.callback_query(F.data == "FirstBand")
async def actions_for_stok_lst(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text=state.get_data(),
        reply_markup=create_inline_kb(
            2,
            "add_to_list",
            "remove_in_list",
        ),
    )
    await callback.answer()


@router.callback_query(F.data == "remove_lst_stoks")
async def remove_lst_stk(callback: CallbackQuery):
    await drop_tables()
    await callback.answer()  # session/repositiory  delete stoks table


@router.callback_query(F.data == "hlaf_year_report")
async def create_hlaf_year_report(callback: CallbackQuery):
    await callback.answer()  # create and reciev report


@router.callback_query(F.data == "year_report")
async def create_year_report(callback: CallbackQuery):
    await callback.answer()  # create and reciev report


@router.callback_query(F.data == "all_time_report")
async def create_all_time_report(callback: CallbackQuery):
    await callback.answer()  # create and reciev report
