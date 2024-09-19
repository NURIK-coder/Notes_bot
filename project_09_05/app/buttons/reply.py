from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

note_list_create_btn = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Notes list'), KeyboardButton(text='Note create')]
    ])
auth = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Register', request_contact=True)
        ]
    ]
)