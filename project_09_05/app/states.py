from aiogram.fsm.state import StatesGroup, State


class NotesState(StatesGroup):
    note_id = State()
    title = State()
    description = State()
    photo = State()
    page=State()
class NoteUpdateState(StatesGroup):
    title = State()
    description = State()
    status = State()
    photo = State()