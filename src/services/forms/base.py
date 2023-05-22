import logging
from collections import namedtuple
from typing import TypeAlias
from typing import Union

from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

_logger = logging.getLogger(__name__)
KeyboardExceptions: TypeAlias = list[int | str] | tuple[int | str]
Keyboard: TypeAlias = ReplyKeyboardMarkup | InlineKeyboardMarkup
_KeyboardButton: TypeAlias = InlineKeyboardButton | KeyboardButton | str


class BaseForm:
    @classmethod
    async def validate_message(cls, message: str) -> bool:
        for button in cls.fields():
            if message == button.text:
                return True

        return False

    @classmethod
    def callback_data(cls) -> CallbackData:
        return CallbackData(cls.__name__, "id")

    @classmethod
    def fields(cls):
        _fields = {}
        _count = 1
        for var, value in cls.__dict__.items():
            if not var.startswith("__"):
                if value.id == -1:
                    value.id = _count
                _fields[var] = value
                _count += 1

        _buttons = namedtuple("fields", list(_fields.keys()))
        return _buttons(**_fields)

    @classmethod
    def get_keyboard(
        cls,
        exceptions: KeyboardExceptions = None,
        row_width: int | None = None,
        rows_template: tuple | list[int] | None = None,
    ) -> ReplyKeyboardMarkup:
        """
        :param exceptions: fields ids list to expect it in keyboard
        :param row_width: keyboard buttons count in one row
        :param rows_template: the template of buttons is tuple or list of count buttons in one row for ex. (1, 2, 1)
        """

        # if used to types of render
        if row_width and rows_template:
            raise ValueError("Use only one variable of row_width and rows_template")

        # if buttons in template more than total buttons count
        if rows_template and sum(rows_template) != len(cls.fields()):
            raise ValueError("Template is not correct, count of buttons is bigger or lower than form fields count")

        # if no one from types is used to render use row_width by default
        if row_width is None and rows_template is None:
            row_width = 1

        if exceptions is None:
            exceptions = []

        keyboard = ReplyKeyboardMarkup(row_width=row_width, resize_keyboard=True)
        fields = [field.text for field in cls.fields() if field.id not in exceptions]
        if rows_template:
            cls._add_buttons_by_rows_template(keyboard, fields, rows_template)
        else:
            cls._add_buttons_by_row_width(keyboard, fields, row_width)

        return keyboard

    @classmethod
    def get_inline_keyboard(
        cls,
        callback_data: CallbackData = None,
        callback_data_args: dict | None = None,
        exceptions: KeyboardExceptions = None,
        rows_template: tuple | list[int] = None,
        row_width: int = None,
    ) -> InlineKeyboardMarkup:
        """
        :param callback_data: callback_data of inline keyboard
        :param callback_data_args: args to pass it to own callback data
        :param exceptions: fields ids list to expect it in keyboard
        :param row_width: keyboard buttons count in one row
        :param rows_template: the template of buttons is tuple or list of count buttons in one row for ex. (1, 2, 1)
        """

        # if used to types of render
        if row_width and rows_template:
            raise ValueError("Use only one variable of row_width and rows_template")

        # if buttons in template more than total buttons count
        if rows_template and sum(rows_template) != len(cls.fields()):
            raise ValueError("Template is not correct, count of buttons is bigger or lower than form fields count")

        # if no one from types is used to render use row_width by default
        if row_width is None and rows_template is None:
            row_width = 1

        if callback_data is None:
            callback_data = cls.callback_data()

        if exceptions is None:
            exceptions = []

        keyboard = InlineKeyboardMarkup(row_width=row_width)

        buttons = []
        for field in cls.fields():
            if field.id in exceptions:
                continue

            if callback_data_args is None:
                callback_data_args = {"id": field.id}
            else:
                callback_data_args["id"] = field.id

            try:
                _callback_data = callback_data.new(**callback_data_args)
            except TypeError:
                raise ValueError("callback_data should contain id argument!")

            button = InlineKeyboardButton(text=field.text, callback_data=_callback_data)
            buttons.append(button)

        if rows_template:
            cls._add_buttons_by_rows_template(keyboard, buttons, rows_template)
        else:
            cls._add_buttons_by_row_width(keyboard, buttons, row_width)

        return keyboard

    @classmethod
    def _add_buttons_by_rows_template(
        cls, keyboard: Keyboard, buttons: list[_KeyboardButton], rows_template: list | tuple
    ) -> None:
        for index, count_in_row in enumerate(rows_template):
            offset = sum(rows_template[:index])
            keyboard.row(*buttons[offset : offset + count_in_row])

    @classmethod
    def _add_buttons_by_row_width(cls, keyboard: Keyboard, buttons: list[_KeyboardButton], row_width: int) -> None:
        for i in range(0, len(buttons), row_width):
            keyboard.row(*buttons[i : i + row_width])

    @classmethod
    def get_id_by_text(cls, text: str) -> Union[int, None]:
        for field in cls.fields():
            if text == field.text:
                return field.id

        return

    @classmethod
    def get_by_id(cls, id: int | str):
        for field in cls.fields():
            if field.id == id:
                return field

        return

    def __getattr__(self, item):
        pass


class FormField:
    def __init__(self, text: str, id_: int | str = None):
        self.text = text
        if id_ is None:
            self.id = -1
        else:
            self.id = id_

    def __eq__(self, other: str | int) -> bool:
        if isinstance(other, (int, str)):
            try:
                return str(other) == str(self.id)
            except ValueError as e:
                _logger.error(e)
                return False
        else:
            return False

    def __repr__(self):
        return f"<FormField id={self.id}, text={self.text}>"
