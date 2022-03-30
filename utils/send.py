from typing import Union

from aiogram import types

from loader import bot


async def get_chat_id() -> int:
    """This function used to get current chat id"""
    return types.Chat.get_current().id


async def send_message(message_text: str,
                       reply_markup: Union[
                           types.ReplyKeyboardMarkup,
                           types.InlineKeyboardMarkup,
                           types.ReplyKeyboardRemove] = None,
                       parse_mode: str = 'HTML',
                       user_id: int = None,
                       photo: Union[
                           str,
                           types.InputFile
                       ] = None,
                       reply_to_message_id: int = None) -> types.Message:
    """
    This function used to send message to user, with default keyboard if keyboard not given in arg
    if user is admin method send message using admin keyboard

    :param message_text: message text, required parameter
    :param reply_markup: keyboard sent with message
    :param parse_mode: message parse mode
    :param user_id: to message user id
    :param photo: photo sent with message
    :param reply_to_message_id: reply to message id
    :return: sent message
    """

    if not user_id:
        user_id = await get_chat_id()

    if photo:
        return await bot.send_photo(user_id, photo=photo, caption=message_text, parse_mode=parse_mode,
                                    reply_markup=reply_markup, reply_to_message_id=reply_to_message_id)

    return await bot.send_message(user_id, message_text, reply_markup=reply_markup, parse_mode=parse_mode,
                                  reply_to_message_id=reply_to_message_id)
