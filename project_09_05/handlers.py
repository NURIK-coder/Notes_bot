import requests
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton, CallbackQuery
from aiogram import html

from buttons.inline import page, update_btn
from buttons.reply import note_list_create_btn
from states import NotesState, NoteUpdateState

router = Router()



@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(f'Hello, {message.from_user.full_name}', reply_markup=note_list_create_btn)


@router.message(F.text.endswith('list'))
async def notes_handler(message: Message, state: FSMContext):
    notes = requests.get('http://127.0.0.1:8000/notes/list/?page=1').json()
    text = ''
    for i in notes['results']:
        text += f'''
ID: {i['id']}
Title: {i['title']}
Description: {i['description']}
-------------------------------------------'''
    await state.update_data(notes=notes['results'])
    await message.answer(text, reply_markup=page)

    await state.set_state(NotesState.note_id)


@router.callback_query(F.data == 'next')
async def next_page(call: CallbackQuery):
    data = requests.get('http://127.0.0.1:8000/notes/list/?page=2').json()
    # print(data)
    text = ''
    for i in data['results']:
        text += f"""
ID: {i['id']}
Title: {i['title']}
Description: {i['description']}
-------------------------------------------
"""
    # print(text)
    await call.message.answer(text, reply_markup=page)


@router.callback_query(F.data == 'previous')
async def previous_page(call: CallbackQuery):
    data = requests.get('http://127.0.0.1:8000/notes/list/?page=1').json()
    print(data)
    if data['previous'] == None:
        await call.message.answer('This is the first page!')
    text = ''
    for i in data['results']:
        text += f"""
ID: {i['id']}
Title: {i['title']}
Description: {i['description']}
-------------------------------------------
    """
    await call.message.answer(text, reply_markup=page)





@router.message(NotesState.title)
async def title(message: Message, state: FSMContext):
    title = message.text
    await state.update_data(title=title)

    await message.answer('Note description: ')
    await state.set_state(NotesState.description)


@router.message(NotesState.description)
async def description(message: Message, state: FSMContext):
    description = message.text
    await state.update_data(description=description)

    dt = await state.get_data()
    body = {
        'title': dt['title'],
        'description': dt['description']
    }

    requests.post('http://127.0.0.1:8000/notes/create/', json=body)
    await message.answer('Success!')


@router.message(NotesState.note_id)
async def note_detail(message: Message, state: FSMContext):
    note_id = message.text
    if not note_id.isdigit():
        await message.answer('Enter a number!')
    note_id = int(note_id)
    data = requests.get(f'http://127.0.0.1:8000/notes/{note_id}').json()
    text = ''
    text += f'''
ID: {data['id']}
Title: {data['title']}
Description: {data['description']}
'''
    await message.answer(text, reply_markup=update_btn)
    await state.update_data(note_id=note_id)
    await state.set_state(NotesState.note_id)


@router.message(F.text.endswith('create'))
async def note_create_handler(message: Message, state: FSMContext):
    await message.answer('The title of the Note:', reply_markup=ReplyKeyboardRemove())
    await state.set_state(NotesState.title)

@router.callback_query(F.data == 'updt')
async def update_note(call: CallbackQuery, state: FSMContext):
    note_data = await state.get_data()
    note_id = note_data['note_id']
    requests.patch(f'http://127.0.0.1:8000/notes/update/{note_id}', json=)
    await call.message.answer('Note title: ')
    await state.set_state(NoteUpdateState.title)

@router.message(NoteUpdateState.title)
async def updated_title(message: Message, state: FSMContext):
    title = message.text
    await state.update_data(title=title)
    await message.answer('Note description: ')
    await state.set_state(NoteUpdateState.description)

@router.message(NoteUpdateState.description)
async def updated_desciption(message:Message, state: FSMContext):
    description = message.text
    await state.update_data(description=description)
    await message.answer("Note status: (If you want to change it enter 'Done')")
    await state.set_state(NoteUpdateState.status)

@router.message(NoteUpdateState.status)
async def update_status(message:Message, state:FSMContext):
    if message.text == 'Done':
        status = True
        await state.update_data(status=status)
        await message.answer("Note Photo(if you want to change it enter 'Yes')")
        await state.set_state(NoteUpdateState.photo)
    else:
        await message.answer("Note Photo(if you want to change it enter 'Yes'):")
        await state.set_state(NoteUpdateState.photo)


@router.message(NoteUpdateState.photo)
async def photo(message: Message, state: FSMContext):
    photo = message.photo[-1]
    photo_tg_file = await message.bot.get_file(file_id=photo.file_id)
    buffered_file = io.BytesIO()
    await message.bot.download_file(file_path=photo_tg_file.file_path, destination=buffered_file)
    filename = photo_tg_file.file_path.split('/')[1]
    files = {
        'photo': buffered_file.read()
    }
    buffered_file.seek(0)
    dt = await state.get_data()

    requests.post('http://127.0.0.1:8000/notes/create/', files=files, data=dt)

    # send_buffered_file = BufferedInputFile(buffered_file.read(), filename=filename)

    await message.answer('Success!')