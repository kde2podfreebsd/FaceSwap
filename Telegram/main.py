import queue
from telebot import types
from Telegram.Markups import MarkupBuilder
from FaceSwap.ImageController import ImageController
from FaceSwap.FaceSwapper import FaceSwapper
from FaceSwap.FaceSwapper import NoFaceDetectedError
from Telegram.Config import bot
from MessageController import MsgMiddleware
from AntifloodMiddleware import SimpleMiddleware
from Telegram.AdminControllerDB import AdminController
from Telegram.StickerMiddleware import StickerPackMiddleware
import random
from FaceSwap.ImagePreparing import ImageResizer
import os
from Telegram.Config import basedir

img_res: ImageResizer = ImageResizer()
msgController: MsgMiddleware = MsgMiddleware()
spm: StickerPackMiddleware = StickerPackMiddleware()
bot.setup_middleware(SimpleMiddleware(2))
queue_system: queue.Queue = queue.Queue()
processing: bool = False
db_path: str = 'cache.db'
admin_controller: AdminController = AdminController(db_path)
admin_controller.add_admin(user_id=406149871, username="@donqhomo")


@bot.message_handler(commands=["start", "home"])
def send_welcome(message: types.Message) -> None:
    bot.send_message(
        chat_id=message.chat.id,
        text=MarkupBuilder.start_message(first_name=(
            message.chat.first_name if message.chat.first_name is not None else message.chat.username
        )),
        reply_markup=MarkupBuilder.hide_reply_markup,
        parse_mode="html",
    )


@bot.message_handler(commands=["admin"])
def admin(message: types.Message) -> None:
    if admin_controller.is_admin(message.chat.id):
        bot.send_message(
            chat_id=message.chat.id,
            text=MarkupBuilder.admin_panel(),
            reply_markup=MarkupBuilder.admin_menu(),
            parse_mode="html",
        )
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text=MarkupBuilder.not_authenticated(),
            reply_markup=None,
            parse_mode="html",
        )


@bot.message_handler(content_types=['text'])
def text_handler(message: types.Message) -> None:

    if message.text == 'Показать пул каналов рекламы':
        channels = admin_controller.get_all_channels()
        if len(channels) == 0:
            bot.send_message(
                chat_id=message.chat.id,
                text="Нет каналов для рекламы",
                reply_markup=MarkupBuilder.admin_menu(),
                parse_mode="html",
            )
            return

        text = ''
        for idx, channel in enumerate(channels):
            text += f"{idx+1}. Channel: {channel[0]}\nChannel link: {channel[1]}\n\n"

        bot.send_message(
            chat_id=message.chat.id,
            text=text,
            reply_markup=MarkupBuilder.admin_menu(),
            parse_mode="html",
        )

    elif message.text == 'Добавить канал в пул рекламы':
        msg = bot.send_message(
            chat_id=message.chat.id,
            text="Отправьте @username канала",
            reply_markup=MarkupBuilder.hide_reply_markup,
            parse_mode="html",
        )
        bot.register_next_step_handler(msg, _add_channel_step2)

    elif message.text == 'Удалить канал из пула реклам':
        msg = bot.send_message(
            chat_id=message.chat.id,
            text="Отправьте @username канала",
            reply_markup=MarkupBuilder.hide_reply_markup,
            parse_mode="html",
        )
        bot.register_next_step_handler(msg, _delete_channel_step2)

    elif message.text == 'Список админов':
        admins = admin_controller.get_all_admins()
        if len(admins) == 0:
            bot.send_message(
                chat_id=message.chat.id,
                text="Нет админов",
                reply_markup=MarkupBuilder.admin_menu(),
                parse_mode="html",
            )
            return

        text = ''
        for idx, admin in enumerate(admins):
            text += f"{idx+1}. Admin id: {admin[0]}\nAdmin username: {admin[1]}\n\n"

        bot.send_message(
            chat_id=message.chat.id,
            text=text,
            reply_markup=MarkupBuilder.admin_menu(),
            parse_mode="html",
        )

    elif message.text == 'Добавить админа':
        msg = bot.send_message(
            chat_id=message.chat.id,
            text="Отправьте @username админа",
            reply_markup=MarkupBuilder.hide_reply_markup,
            parse_mode="html",
        )
        bot.register_next_step_handler(msg, _add_admin_step2)

    elif message.text == 'Удалить админа':
        msg = bot.send_message(
            chat_id=message.chat.id,
            text="Отправьте chat_id админа",
            reply_markup=MarkupBuilder.hide_reply_markup,
            parse_mode="html",
        )
        bot.register_next_step_handler(msg, _delete_admin_step2)


def _delete_admin_step2(message):
    chat_id = message.text
    admin_controller.remove_admin(user_id=chat_id)

    bot.send_message(
        chat_id=message.chat.id,
        text=f"{chat_id} успешно удален из админов",
        reply_markup=MarkupBuilder.admin_menu(),
        parse_mode="html",
    )


def _add_admin_step2(message):
    user_id = message.text
    if admin_controller.is_admin(user_id):
        bot.send_message(
            chat_id=message.chat.id,
            text=f"Админ с user_id {user_id} уже существует.",
            reply_markup=MarkupBuilder.admin_menu(),
            parse_mode="html",
        )
    else:
        admin_controller.admin_storage[message.chat.id] = user_id
        msg = bot.send_message(
            chat_id=message.chat.id,
            text="Отправьте @username админа",
            reply_markup=MarkupBuilder.hide_reply_markup,
            parse_mode="html",
        )
        bot.register_next_step_handler(msg, _add_admin_step3)


def _add_admin_step3(message):
    username = admin_controller.admin_storage[message.chat.id]
    chat_id = message.text

    admin_controller.add_admin(user_id=chat_id, username=username)

    bot.send_message(
        chat_id=message.chat.id,
        text=f"Админ {username} успешно добавлен",
        reply_markup=MarkupBuilder.admin_menu(),
        parse_mode="html",
    )


def _add_channel_step2(message):
    admin_controller.channel_storage[message.chat.id] = message.text

    msg = bot.send_message(
        chat_id=message.chat.id,
        text="Отправьте ссылку на канал",
        reply_markup=MarkupBuilder.hide_reply_markup,
        parse_mode="html",
    )
    bot.register_next_step_handler(msg, _add_channel_step3)


def _add_channel_step3(message):
    channel = admin_controller.channel_storage.get(message.chat.id)
    channel_link = message.text

    admin_controller.add_channel(channel_name=channel, channel_link=channel_link)

    bot.send_message(
        chat_id=message.chat.id,
        text=f"Канал {channel} успешно добавлен",
        reply_markup=MarkupBuilder.admin_menu(),
        parse_mode="html",
    )


def _delete_channel_step2(message):
    channel_to_delete = message.text

    admin_controller.remove_channel(channel_name=channel_to_delete)

    bot.send_message(
        chat_id=message.chat.id,
        text="Канал успешно удален из рекламного пула",
        reply_markup=MarkupBuilder.admin_menu(),
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
            name = f"meme_{next_user}_{str(random.randint(100000, 999999))}_by_FaceSwap_Meme_Bot"
            print(target_path)
            f.create_mempack(user_id=next_user, target_face_image_path=target_path)
            img_res.prepare_images(
                folder_path=os.path.join(
                    basedir,
                    'FaceSwap',
                    'outputs',
                    str(next_user)
                )
            )

            spm.create_sticker_pack(
                user_id=next_user,
                name=name,
                title="Face Meme Swap @donqhomo"
            )
            sticker_pack = spm.getStickerSet(sticker_pack_name=name)
            sticker_pack_name = f"t.me/addstickers/{name}"
            first_sticker_file_id = sticker_pack['result']['stickers'][0]['file_id']
            bot.send_sticker(next_user, first_sticker_file_id)

        except NoFaceDetectedError:
            msgController.delete_message_id(user_id=next_user)

            bot.send_message(
                chat_id=next_user,
                text=MarkupBuilder.no_face_detected_error(),
                parse_mode="HTML",
                disable_web_page_preview=False
            )
            return

        msgController.delete_message_id(user_id=next_user)

        bot.send_message(
            chat_id=next_user,
            text=MarkupBuilder.stickerset_ready_text(),
            reply_markup=MarkupBuilder.stickerset_ready_markup(sticker_pack_url=sticker_pack_name),
            parse_mode="HTML",
            disable_web_page_preview=False
        )
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
        if len(all_channels) == 0:
            _subbed(chat_id=chat_id)
            return
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

    elif call.data == 'again':
        bot.send_message(
            chat_id=call.message.chat.id,
            text=MarkupBuilder.start_message(first_name=(
                call.message.chat.first_name if call.message.chat.first_name is not None else call.message.chat.username
            )),
            reply_markup=None,
            parse_mode="html",
        )


if __name__ == "__main__":
    bot.infinity_polling()
