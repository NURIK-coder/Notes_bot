from typing import List

import requests
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton, CallbackQuery
from aiogram import html

from app.notes.models import Note
from app.buttons.inline import page, update_btn
from app.buttons.reply import note_list_create_btn
from app.states import NotesState, NoteUpdateState, NoteState
import io

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(f'Hello, {message.from_user.full_name}', reply_markup=note_list_create_btn)


# @router.message(F.text.endswith('list'))
# async def notes_handler(message: Message, state: FSMContext):
#     notes = requests.get('http://127.0.0.1:8000/notes/list/').json()
#     text = ''
#     for i in notes['results']:
#         text += f'''
# ID: {i['id']}
# Title: {i['title']}
# Description: {i['description']}
# -------------------------------------------'''
#     await state.update_data(notes=notes['results'])
#     await message.answer(text, reply_markup=page)
#     pg = 1
#     await state.update_data(page=pg)
#
#     await state.set_state(NotesState.note_id)
#
#
#
# @router.callback_query(F.data == 'next')
# async def next_page(call: CallbackQuery, state: FSMContext):
#     dt = await state.get_data()
#     get_page = dt['page']
#     get_page += 1
#     data = requests.get(f'http://127.0.0.1:8000/notes/list/?page={get_page}').json()
#
#     await state.update_data(page=get_page)
#
#     # print(data)
#     text = ''
#     for i in data['results']:
#         text += f"""
# ID: {i['id']}
# Title: {i['title']}
# Description: {i['description']}
# -------------------------------------------
# """
#     # print(text)
#     await call.message.answer(text, reply_markup=page)
#
#
# @router.callback_query(F.data == 'previous')
# async def previous_page(call: CallbackQuery, state: FSMContext):
#     dt = await state.get_data()
#     pg = dt['page']
#     if pg <= 1:
#         await call.message.answer('This is the first page!')
#     pg -= 1
#
#     data = requests.get(f'http://127.0.0.1:8000/notes/list/?page={pg}').json()
#     text = ''
#     for i in data['results']:
#         text += f"""
# ID: {i['id']}
# Title: {i['title']}
# Description: {i['description']}
# -------------------------------------------
#     """
#     await call.message.answer(text, reply_markup=page)
#
#
# @router.message(F.text.endswith('create'))
# async def note_create_handler(message: Message, state: FSMContext):
#     await message.answer('The title of the Note:', reply_markup=ReplyKeyboardRemove())
#     await state.set_state(NotesState.title)
#
#
# @router.message(NotesState.title)
# async def title(message: Message, state: FSMContext):
#     title = message.text
#     await state.update_data(title=title)
#
#     await message.answer('Note description: ')
#     await state.set_state(NotesState.description)
#
#
# @router.message(NotesState.description)
# async def description(message: Message, state: FSMContext):
#     description = message.text
#     await state.update_data(description=description)
#
#     dt = await state.get_data()
#     # body = {
#     #     'title': dt['title'],
#     #     'description': dt['description']
#     # }
#
#     await Note.create(title=dt['title'], content=dt['description'])
#     await message.answer('Success!')
#     await state.clear()
#
#
# @router.message(NotesState.note_id)
# async def note_detail(message: Message, state: FSMContext):
#     note_id = message.text
#     if not note_id.isdigit():
#         await message.answer('Enter a number!')
#     note_id = int(note_id)
#     data = requests.get(f'http://127.0.0.1:8000/notes/{note_id}').json()
#     text = ''
#     text += f'''
# ID: {data['id']}
# Title: {data['title']}
# Description: {data['description']}
# '''
#     await message.answer(text, reply_markup=update_btn)
#     await state.update_data(note_id=note_id)
#     await state.set_state(NotesState.note_id)
#
#
# @router.callback_query(F.data == 'updt')
# async def update_note(call: CallbackQuery, state: FSMContext):
#     note_data = await state.get_data()
#     note_id = note_data['note_id']
#     requests.patch(f'http://127.0.0.1:8000/notes/update/{note_id}')
#     await call.message.answer('Note title: ')
#     await state.set_state(NoteUpdateState.title)
#
#
# @router.message(NoteUpdateState.title)
# async def updated_title(message: Message, state: FSMContext):
#     title = message.text
#     await state.update_data(title=title)
#     await message.answer('Note description: ')
#     await state.set_state(NoteUpdateState.description)
#
#
# @router.message(NoteUpdateState.description)
# async def updated_desciption(message: Message, state: FSMContext):
#     description = message.text
#     await state.update_data(description=description)
#     await message.answer("Note status: (If you want to change it enter 'Done')")
#     await state.set_state(NoteUpdateState.status)
#
#
# @router.message(NoteUpdateState.status)
# async def update_status(message: Message, state: FSMContext):
#     if message.text == 'Done':
#         status = True
#         await state.update_data(status=status)
#         await message.answer("Note Photo(if you want to change it send photo")
# await state.set_state(NoteUpdateState.photo)
# else:
#     await message.answer("Note Photo(if you want to change it send photo:")
#     await state.set_state(NoteUpdateState.photo)


# @router.message(NoteUpdateState.photo)
# async def photo(message: Message, state: FSMContext):
#     dt = await state.get_data()
#     note_id = dt['note_id']
#     if message.photo:
#         photo = message.photo[-1]
#         photo_tg_file = await message.bot.get_file(file_id=photo.file_id)
#         buffered_file = io.BytesIO()
#         await message.bot.download_file(file_path=photo_tg_file.file_path, destination=buffered_file)
#         filename = photo_tg_file.file_path.split('/')[1]
#         files = {
#             'photo': buffered_file.read()
#         }
#         buffered_file.seek(0)
#
#         requests.patch(f'http://127.0.0.1:8000/notes/update/{note_id}', files=files, data=dt)
#         await message.answer('Success!')
#     else:
#         requests.patch(f'http://127.0.0.1:8000/notes/update/{note_id}', data=dt)
#         await message.answer('Success!')


######################################


@router.message(F.text == 'Note create')
async def create_note(message: Message, state: FSMContext):
    await message.answer('Note title:')
    await state.set_state(NoteState.title)
    # note = await Note.create(title='first', content='First content')
    # print(note.id, note.title, note.content)
    # await message.answer('Note has been created!')
@router.message(NoteState.title)
async def title(message: Message, state:FSMContext):
    title = message.text
    await state.update_data(title=title)
    await message.answer('Note context: ')
    await state.set_state(NoteState.context)

@router.message(NoteState.context)
async def description(message: Message, state: FSMContext):
    context = message.text
    await state.update_data(context=context)
    data = await state.get_data()
    note = await Note.create(title=data['title'], content=data['context'])
    await message.answer(f'Note has been created!')
    await state.clear()



@router.message(F.text == 'Notes list')
async def get_notes(message: Message):
    notes: List[Note] = await Note.get_all()
    text = ''
    for i in notes:
        text += f'''
ID {i.id}
Title: {i.title}
Content: {i.content}
======================================='''
    await message.answer(text)


@router.message(Command('update'))
async def update_data(message: Message):
    note = await Note.update(1, title='First')  # отличие от creat: нужно отправить id и поля не обязательны
    print(note.title)
    await message.answer(f'Note has been changed {note.title}')


@router.message(F.text.startswith('delete'))
async def delete(message: Message):
    note_id = int(message.text.split(' ')[1])
    await Note.delete(Note.id == note_id)
    await message.answer('Note has been deleted')


@router.message(Command('filter'))
async def filtred_note(message: Message):
    notes = await Note.filter(Note.title == 'First')
    # notes = await Note.paginate(limit=10, page=1, filters=Note.content == 'asdfssa')
    await message.answer(f'number of notes: {len(notes)}')
