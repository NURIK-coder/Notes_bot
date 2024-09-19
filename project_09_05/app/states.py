from aiogram.fsm.state import StatesGroup, State


class NotesState(StatesGroup):
    note_id = State()
    title = State()
    description = State()
    photo = State()
    page=State()

class NoteUpdateState(StatesGroup):
    title = State()
    context = State()
    status = State()
    photo = State()
class NoteState(StatesGroup):
    note_id = State()
    title = State()
    context = State()
    photo = State()
    status = State()

class UserState(StatesGroup):
    tg_id = State()
    name = State()
    phone = State()
    role = State()
    contact = State()



