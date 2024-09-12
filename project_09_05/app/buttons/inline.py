from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

page = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='⬅️', callback_data='previous'), InlineKeyboardButton(text='➡️', callback_data='next')]
])
update_btn = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Update', callback_data='updt')]
])