from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

page = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='⬅️', callback_data='previous'), InlineKeyboardButton(text='➡️', callback_data='next')]
])
update_btn = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Update', callback_data='update')],
    [InlineKeyboardButton(text='Delete', callback_data='delete')]
])
admin_btn = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Block', callback_data='block')
    ],
    [
        InlineKeyboardButton(text='Change role to admin', callback_data='change')
    ]
])