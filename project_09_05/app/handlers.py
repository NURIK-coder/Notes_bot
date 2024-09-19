from typing import List

import requests
from aiogram import Router, F, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton, CallbackQuery
from aiogram import html

from app.notes.models import Note
from app.buttons.inline import page, update_btn, admin_btn
from app.buttons.reply import note_list_create_btn, auth
from app.states import NotesState, NoteUpdateState, NoteState, UserState
import io

from app.users.models import User

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    user = await User.detail(record_id=message.from_user.id)
    if user is None:
        await message.answer('You are not authenticated. Please sign up', reply_markup=auth)
        await state.set_state(UserState.contact)
    else:
        await message.answer(f'Hello, {message.from_user.full_name}', reply_markup=note_list_create_btn)

@router.message(UserState.contact)
async def contact(messsage: Message):
    print(messsage.contact)



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

#==================================================================================
################ CREATE ######################


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

#=====================================================================================
######################### LIST ###########################################

@router.message(F.text == 'Notes list')
async def get_notes(message: Message, state: FSMContext):
    notes: List[Note] = await Note.get_all()
    count = 0
    text = ''
    for i in notes:
        text += f'''
ID {i.id}
Title: {i.title}
Content: {i.content}
Created at: {i.created_at}
Status: {i.status}
======================================='''
        count+=1
    await state.update_data(count=count)
    await message.answer(text)
    await state.set_state(NoteState.note_id)

#===========================================================================
####################### NOTE DETAIL #######################################

@router.message(NoteState.note_id)
async def note_detail(message: Message, state:FSMContext):
    noteId = message.text
    if not noteId.isdigit():
        await message.answer('Enter a number please!')
    note = await Note.detail(record_id=int(noteId))
    text = ''

    text+=f'''
ID {note.id}
Title: {note.title}
Content: {note.content}
Created at: {note.created_at}
Status: {note.status}
======================================='''

    await message.answer(text, reply_markup=update_btn)
    await state.clear()
    await state.update_data(note_id=noteId)

# =========================================================================================================
######################################## UPDATE ########################################

@router.callback_query(F.data == 'update')
async def update_data(call: CallbackQuery, state: FSMContext):
    await call.message.answer("If you want to change title enter title name or enter('Skip'):")
    await state.set_state(NoteUpdateState.title)
    # note = await Note.update(1, title='First')  # отличие от creat: нужно отправить id и поля не обязательны

@router.message(NoteUpdateState.title)
async def updt_title(message: Message, state: FSMContext):
    title = message.text
    if title == 'Skip':
        await message.answer("If you want to change context enter context name or enter('Skip'):")
        await state.set_state(NoteUpdateState.context)

    await state.update_data(title=title)
    await message.answer("If you want to change context enter context name or enter('Skip'):")
    await state.set_state(NoteUpdateState.context)

@router.message(NoteUpdateState.context)
async def updt_context(message: Message, state: FSMContext):
    context = message.text
    if context == 'Skip':
        await message.answer("If you want to change status enter('Done')")
        await state.set_state(NoteUpdateState.status)
    await state.update_data(context=context)
    await message.answer("If you want to change status enter('Done')")
    await state.set_state(NoteUpdateState.status)
@router.message(NoteUpdateState.status)
async def updt_status(message: Message, state: FSMContext):
    status = message.text
    if status == 'Done':
        await state.update_data(status=True)
        await message.answer('Success!')
    data = await state.get_data()
    updated_note = await Note.update(data['note_id'], title=data['title'], content=data['context'], status=data['status'])
    await message.answer('Success!')

#=====================================================================================================================================
################### DELETE #########################

@router.callback_query(F.data == 'delete')
async def delete(call: CallbackQuery, state:FSMContext):
    dt = await state.get_data()
    note_id = dt['note_id']
    await Note.delete(Note.id == note_id)
    await call.message.answer('Note has been deleted')

#=================================================================
############## FILTER ##################

@router.message(Command('filter'))
async def filtred_note(message: Message):
    notes = await Note.filter(Note.title == 'First')
    # notes = await Note.paginate(limit=10, page=1, filters=Note.content == 'asdfssa')
    await message.answer(f'number of notes: {len(notes)}')

#==============================================================================
########################### FOR ADMIN ##########################

@router.message(Command('users'))
async def get_all_users(message: Message, state: FSMContext):
    users = await User.get_all()
    text = ''
    for i in users:
        text += f'''
ID: {i.tg_id}
Name: {i.name}
Phone: {i.phone}
Role: {i.role}'''

    await message.answer(text)
    await state.set_state(UserState.tg_id)

@router.message(UserState.tg_id)
async def user_detail(message:Message, state: FSMContext):
    user_id = message.text
    user = await User.detail(record_id=int(user_id))
    text = ''
    text += f'''
ID: {user.tg_id}
Name: {user.name}
Phone: {user.phone}
Role: {user.role}

'''
    await message.answer(text, reply_markup=admin_btn)



