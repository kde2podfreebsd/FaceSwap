import queue
from telebot import types
from Telegram.Markups import MarkupBuilder
from FaceSwap.ImageController import ImageController
from FaceSwap.FaceSwapper import FaceSwapper
from FaceSwap.FaceSwapper import NoFaceDetectedError
from Telegram.Config import bot
from MessageController import MsgMiddleware
from AntifloodMiddleware import SimpleMiddleware
from Telegram.AdminController import AdminController


msgController = MsgMiddleware()
bot.setup_middleware(SimpleMiddleware(2))
queue_system = queue.Queue()
processing = False
db_path = 'cache.db'
admin_controller = AdminController(db_path)
# admin_controller.add_channel(channel_name='@abobaabobaabobaaboba1488', channel_link='https://t.me/+enenh6Q8DmNmZDIy')
# @abobaabobaabobaaboba1488
# @geeksflow


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
        'voice'
    ])
def cant_processed(message: types.Message) -> None:
    bot.send_message(
        chat_id=message.chat.id,
        text=MarkupBuilder.сant_processed(),
        reply_markup=None,
        parse_mode="html",
    )


def _subbed(chat_id: int | str) -> None:
    position = queue_system.qsize() + 1
    msg = bot.send_message(
        chat_id=chat_id,
        text=MarkupBuilder.await_image_generating(position=position),
        reply_markup=None,
        parse_mode="html",
    )

    msgController.add_message_id(user_id=chat_id, message_id=msg.message_id)
    queue_system.put(chat_id)
    process_queue()


def process_queue():
    global processing
    if not processing and not queue_system.empty():
        next_user = queue_system.get()
        processing = True
        f = FaceSwapper()
        imgCtr = ImageController()
        target_path = imgCtr.get_target_path(next_user)
        if target_path is None:
            msgController.delete_message_id(user_id=next_user)
            bot.send_message(
                chat_id=next_user,
                text=MarkupBuilder.state_cache_error(),
                parse_mode="HTML",
                disable_web_page_preview=False
            )
            return
        try:
            f.create_mempack(user_id=next_user, target_face_image_path=target_path)
        except NoFaceDetectedError:
            msgController.delete_message_id(user_id=next_user)
            bot.send_message(
                chat_id=next_user,
                text=MarkupBuilder.no_face_detected_error(),
                parse_mode="HTML",
                disable_web_page_preview=False
            )
            return

        file_paths = imgCtr.get_output_paths(next_user)[:10]  # Получаем пути к первым 10 файлам
        media = []

        for file_path in file_paths:
            with open(file_path, 'rb') as file:
                file_data = file.read()
                media.append(types.InputMediaPhoto(media=file_data))

        msgController.delete_message_id(user_id=next_user)
        bot.send_media_group(next_user, media)
    else:
        processing = False


def _not_subbed(chat_id: int | str, channel: str, channel_link: str) -> None:

    msg = bot.send_message(
        chat_id=chat_id,
        text=MarkupBuilder.subscribe_text(),
        reply_markup=MarkupBuilder.subscribe_btn_markup(
            channel_link=channel_link,
            user_id=chat_id,
            channel=channel,
        ),
        parse_mode="HTML",
        disable_web_page_preview=False
    )

    msgController.add_message_id(user_id=chat_id, message_id=msg.message_id)


def _go_subscribe(chat_id: int | str, channel_username: str = None, channel_href: str = None) -> None:

    target_channel = None
    if channel_username or channel_href is None:
        all_channels = admin_controller.get_all_channels()
        for channel in all_channels:
            is_member = bot.get_chat_member(channel[0], chat_id)
            if is_member.status == 'left':
                target_channel = channel[0]
                target_channel_link = channel[1]
                break
    else:
        is_member = bot.get_chat_member(channel_username, chat_id)

    msgController.delete_message_id(user_id=chat_id)

    if is_member.status != 'left':
        _subbed(chat_id=chat_id)
    else:
        _not_subbed(chat_id=chat_id, channel=target_channel, channel_link=target_channel_link)


@bot.message_handler(content_types=['photo'])
def image_handler(message: types.Message) -> None:
    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    imgCtr = ImageController()
    imgCtr.saveImage(message.chat.id, downloaded_file)
    _go_subscribe(message.chat.id)
    process_queue()


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):

    if "subscribed" in call.data:
        response = call.data.split(':')
        user_id = response[1]
        channel = response[2]
        channel_link = admin_controller.get_channel_link(channel)

        _go_subscribe(user_id, channel_username=channel, channel_href=channel_link)
        process_queue()


if __name__ == "__main__":
    bot.infinity_polling()
