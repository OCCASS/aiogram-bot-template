import datetime
from typing import List
from typing import Union

from aiogram import Dispatcher
from aiogram import types

from src.data.config import ADMINS
from src.data.config import BotMode
from src.keyboards.inline import get_check_subscription_keyboard
from src.keyboards.inline import get_extend_subscription_keyboard
from src.keyboards.inline.callbacks import mange_subscription_callback_data
from src.loader import bot
from src.loader import db
from src.service.database.models import Subscription
from src.service.database.models import UserSubsctiption
from src.service.forms import author_main_form
from src.service.forms import author_profile_form
from src.service.forms import manage_subscription_form
from src.service.forms import select_mode_form
from src.service.forms import subscriber_main_form
from src.service.forms import subscriber_profile_form
from src.states import States
from src.utils import reset_data
from src.utils.text import get_created_subscription_text
from src.utils.text import get_days_text
from src.utils.text import get_purchased_subscription_text


async def get_chat_id() -> int:
    """This function used to get current chat id"""
    chat = types.Chat.get_current()
    if chat is None:
        chat = types.User.get_current()

    return chat.id if chat is not None else None


async def send_message(
    message_text: str,
    reply_markup: Union[types.ReplyKeyboardMarkup, types.InlineKeyboardMarkup, types.ReplyKeyboardRemove] = None,
    parse_mode: str = "HTML",
    user_id: int = None,
    photo: Union[str, types.InputFile] = None,
    reply_to_message_id: int = None,
) -> types.Message:
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
        return await bot.send_photo(
            user_id,
            photo=photo,
            caption=message_text,
            parse_mode=parse_mode,
            reply_markup=reply_markup,
            reply_to_message_id=reply_to_message_id,
        )

    return await bot.send_message(
        user_id, message_text, reply_markup=reply_markup, parse_mode=parse_mode, reply_to_message_id=reply_to_message_id
    )


async def send_author_general_menu():
    keyboard = await author_main_form.get_keyboard(row_width=2)
    await send_message("Вы поменял режим: теперь вы автор", reply_markup=keyboard)


async def send_subscriber_general_menu():
    keyboard = await subscriber_main_form.get_keyboard(row_width=3)
    await send_message("Вы поменял режим: теперь вы подписчик", reply_markup=keyboard)


async def send_general_menu(user_telegram_id):
    state = Dispatcher.get_current().current_state()
    mode = await db.get_user_mode(user_telegram_id)

    if mode == BotMode.AUTHOR:
        await send_author_general_menu()
    elif mode == BotMode.SUBSCRIBER:
        await send_subscriber_general_menu()

    await reset_data()
    await state.set_state(States.main_menu)


async def send_author_subscriptions(subscriptions: List[Subscription]):
    for s in subscriptions:
        keyboard = await manage_subscription_form.get_inline_keyboard(
            callback_data=mange_subscription_callback_data, callback_data_args={"sub_id": s.id}
        )
        await send_message(await get_created_subscription_text(s), reply_markup=keyboard)


async def send_purchased_subscriptions(subscriptions: List[UserSubsctiption]):
    for s in subscriptions:
        keyboard = get_extend_subscription_keyboard(s.id)
        await send_message(await get_purchased_subscription_text(s), reply_markup=keyboard)


async def send_plug():
    await send_message("⚙️ Данный метод в разработке")


async def send_subscription_request(subscription_id: int):
    keyboard = get_check_subscription_keyboard(subscription_id)
    for admin in ADMINS:
        await send_message("📨 Новая заявка на создание подписки", user_id=admin, reply_markup=keyboard)


async def send_select_mode(full_name: str):
    keyboard = await select_mode_form.get_inline_keyboard(row_width=2)
    await send_message(f"Привет 👋, <pre>{full_name}</pre>! Выбери режим:", reply_markup=keyboard)


async def send_author_profile(user_telegram_id: int, full_name: str):
    user = await db.get_user_by_telegram_id(user_telegram_id)
    all_subscriptions_count = len(await db.get_all_author_subscriptions(user.id))
    active_subscriptions_count = len(await db.get_all_active_author_subscriptions(user.id))

    reg_date_text = user.datetime.strftime("%d.%m.%Y")
    reg_days_text = get_days_text((datetime.datetime.now() - user.datetime).days)

    keyboard = await author_profile_form.get_keyboard(row_width=2)
    await send_message(
        f"👤 Аккаунт, <pre>{full_name}</pre>\n\n"
        f"👁‍🗨 <b>ID:</b> <pre>{user_telegram_id}</pre>\n"
        f"👁‍🗨 <b>Количество активных подписок:</b> <pre>{active_subscriptions_count}</pre>\n"
        f"👁‍🗨 <b>Всего создано подписок:</b> <pre>{all_subscriptions_count}</pre>\n"
        f"👁‍🗨 <b>Регистрация:</b> <pre>{reg_date_text} ({reg_days_text})</pre>",
        reply_markup=keyboard,
    )


async def send_subscriber_profile(telegram_id: int, full_name: str):
    user = await db.get_user_by_telegram_id(telegram_id)
    all_subscriptions_count = len(await db.get_all_active_user_subscriptions(user.id))
    active_subscriptions_count = len(await db.get_user_active_subscriptions(user.id))

    reg_date_text = user.datetime.strftime("%d.%m.%Y")
    reg_days_text = get_days_text((datetime.datetime.now() - user.datetime).days)

    keyboard = await subscriber_profile_form.get_keyboard(row_width=2)
    await send_message(
        f"👤 Аккаунт, <pre>{full_name}</pre>\n\n"
        f"👁‍🗨 <b>ID:</b> <pre>{telegram_id}</pre>\n"
        f"👁‍🗨 <b>Общее количество купленных подписок:</b> <pre>{all_subscriptions_count}</pre>\n"
        f"👁‍🗨 <b>Количество активных подписок:</b> <pre>{active_subscriptions_count}</pre>\n"
        f"👁‍🗨 <b>Регистрация:</b> <pre>{reg_date_text} ({reg_days_text})</pre>",
        reply_markup=keyboard,
    )
