import telebot
from telebot import types
from Telegram.Markups import MarkupBuilder
from Telegram.Markups import TextBuilder
from Telegram.Config import bot


@bot.message_handler(commands=["start"])
def send_welcome(message: types.Message) -> None:
    bot.send_message(
        chat_id=message.chat.id,
        text=MarkupBuilder.start_message(first_name=(
            message.chat.first_name if message.chat.first_name is not None else message.chat.username
        )),
        reply_markup=None,
        parse_mode="html",
    )


@bot.message_handler(
    content_types=[
        'animation',
        'audio',
        'contact',
        'dice',
        'document',
        'location',
        'poll',
        'sticker',
        'text',
        'venue',
        'video',
        'video_note',
        'voice'])
def cant_processed(message: types.Message) -> None:
    bot.send_message(
        chat_id=message.chat.id,
        text=MarkupBuilder.сant_processed(),
        reply_markup=None,
        parse_mode="html",
    )


def _go_subscribe(chat_id: int | str)->None:
    # @abobaabobaabobaaboba1488
    # @geeksflow

    channel = '@abobaabobaabobaaboba1488'
    channel_link = 'https://t.me/+enenh6Q8DmNmZDIy'
    is_member = bot.get_chat_member(channel, chat_id)

    if is_member.status != 'left':
        bot.send_message(
            chat_id=chat_id,
            text=MarkupBuilder.await_image_generating(),
            reply_markup=None,
            parse_mode="html",
        )

    else:
        bot.send_message(
            chat_id=chat_id,
            text=MarkupBuilder.subscribe_text(),
            reply_markup=MarkupBuilder.subscribe_btn_markup(
                channel_link=channel_link,
                user_id=chat_id,
                channel=channel
            ),
            parse_mode="html",
        )


@bot.message_handler(content_types=['photo'])
def image_handler(message: types.Message) -> None:
    _go_subscribe(message.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):

    if "subscribed" in call.data:
        response = call.data.split(':')
        user_id = response[1]
        channel = response[2]

        is_member = bot.get_chat_member(channel, user_id)

        if is_member.status != 'left':
            pass
        else:
            _go_subscribe(user_id)





bot.infinity_polling()