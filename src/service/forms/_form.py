from collections import namedtuple
from typing import Union

from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


class BaseForm:
    fields = None

    def __new__(cls, *args, **kwargs):
        __fields = {}
        __count = 1
        for var, value in cls.__dict__.items():
            if not var.startswith("__"):
                if value.id == -1:
                    value.id = __count
                __fields[var] = value
                __count += 1

        _buttons = namedtuple("fields", list(__fields.keys()))
        cls.fields = _buttons(**__fields)
        return cls

    @classmethod
    async def validate_message(cls, message: str) -> bool:
        for button in cls.fields:
            if message == button.text:
                return True

        return False

    @classmethod
    async def get_keyboard(cls, row_width=1, exceptions=None) -> ReplyKeyboardMarkup:
        """
        :param row_width:
        :param exceptions: список идентификаторов полей которые надо исключить при создании клавиатуры
        """

        if exceptions is None:
            exceptions = []

        keyboard = ReplyKeyboardMarkup(row_width=row_width, resize_keyboard=True)
        fields = [field.text for field in cls.fields if field.id not in exceptions]
        for i in range(0, len(fields), row_width):
            keyboard.row(*fields[i : i + row_width])

        return keyboard

    @classmethod
    def get_callback_data(cls):
        return CallbackData(cls.__name__, "id")

    @classmethod
    async def get_inline_keyboard(
        cls, callback_data=None, callback_data_args: Union[dict, None] = None, row_width=1, exceptions=None
    ):
        if callback_data is None:
            callback_data = cls.get_callback_data()

        if exceptions is None:
            exceptions = []

        keyboard = InlineKeyboardMarkup(row_width=row_width)

        buttons = []
        for field in cls.fields:
            if field.id in exceptions:
                continue

            if callback_data_args is None:
                callback_data_args = {"id": field.id}
            else:
                callback_data_args["id"] = field.id

            button = InlineKeyboardButton(text=field.text, callback_data=callback_data.new(**callback_data_args))
            buttons.append(button)

        for i in range(0, len(buttons), row_width):
            keyboard.row(*buttons[i : i + row_width])

        return keyboard

    @classmethod
    async def get_id_by_text(cls, text) -> Union[int, None]:
        for field in cls.fields:
            if text == field.text:
                return field.id

        return

    @classmethod
    async def get_by_id(cls, id: int):
        for field in cls.fields:
            if field.id == id:
                return field

        return


class FormField:
    def __init__(self, text, id_: int = None):
        self.text = text
        if id_ is None:
            self.id = -1
        else:
            self.id = id_

    def __eq__(self, other) -> bool:
        if isinstance(other, int):
            return other == self.id
        elif isinstance(other, str):
            return other == str(self.id)
        else:
            return False

    def __repr__(self):
        return f"<FormField id={self.id}, text={self.text}>"
