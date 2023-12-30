from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class TextBuilder(object):

    _stickerset_ready = None
    _admin_panel = None
    _not_authenticated = None
    _state_cache_error = None
    _no_face_detected_error = None
    _await_image_generating_text = None
    _subscribe_text = None
    _сant_processed_text = None
    _start_message = None

    @classmethod
    def start_message(cls, first_name: str) -> str:
        cls._start_message = f'''
👋 Привет <b>{", "+ first_name if first_name is not None else ''}</b>!
Чтобы получить Ваш уникальный sticker-pack, загрузите, пожалуйста, свою фотографию.

<b>Следуйте советам:</b>
🤵 — На фото должно быть хорошо видно ваше лицо;
🙋🏻‍♂️ — На фото не должно быть других лиц, кроме вашего;
🎩 — Желательно без головного убора и очков;
🥸 — Если вы носите очки, то попробуйте использовать фото без них;
🙊 — Не отправляйте фото животных, бот распознаёт только лица людей;

⌛️ Обычно обработка фото занимает до 1-ой минуты, но при большой очереди придется подождать дольше 🥹
'''
        return cls._start_message

    @classmethod
    def сant_processed(cls) -> str:
        cls._сant_processed_text = '''
🙈 Ой!  
🤷‍♂️ Я еще не умею обрабатывать видео, стикеры, текст и другие файлы, кроме фото.
📸 Попробуйте загрузить фотографию.        
'''
        return cls._сant_processed_text

    @classmethod
    def subscribe_text(cls) -> str:
        cls._subscribe_text = '''
Отлично! Чтобы начать генерацию мемов с вами в главной роли, подпишитесь на <a href="https://t.me/+enenh6Q8DmNmZDIy">Telegram-канал</a> 😎

🥰 Подписка на наш канал — лучший подарок нам на Новый год         
'''
        return cls._subscribe_text

    @classmethod
    def await_image_generating(cls, position) -> str:
        cls._await_image_generating_text = f'''
Магия происходит, скоро все случится ✨
Ваша позиция {position} в очереди.
Как только все будет готово, мы пришлем уведомление. А пока можно заварить чай и отдохнуть 🙈
'''
        return cls._await_image_generating_text

    @classmethod
    def no_face_detected_error(cls):
        cls._no_face_detected_error = "🤔 На изображении не распознано лиц, попробуйте отправить другое фото"
        return cls._no_face_detected_error

    @classmethod
    def state_cache_error(cls):
        cls._state_cache_error = "🤔 Какая-то ошибка(( Отправьте фото еще раз или попробуйте позже"
        return cls._state_cache_error

    @classmethod
    def not_authenticated(cls):
        cls._not_authenticated = "not authenticated"
        return cls._not_authenticated

    @classmethod
    def admin_panel(cls):
        cls._admin_panel = "Привет, Босс\n<b>[admin panel]</b>"
        return cls._admin_panel

    @classmethod
    def stickerset_ready_text(cls):
        cls._stickerset_ready = '''
Готово! Чтобы добавить стикерпак, нажмите на стикер выше или по ссылке. А еще ботом нужно <a href="https://t.me/share/url?url=https://t.me/https://t.me/FaceSwap_Meme_Bot">поделиться</a> с друзьями 🙌
'''
        return cls._stickerset_ready
        

class MarkupBuilder(TextBuilder):

    _hide_menu: types.ReplyKeyboardRemove() = None

    @classmethod
    @property
    def hide_reply_markup(cls) -> types.ReplyKeyboardRemove():
        cls._hide_menu: object = types.ReplyKeyboardRemove()
        return cls._hide_menu

    @classmethod
    def subscribe_btn_markup(cls, channel_link: str, user_id, channel: str) -> types.InlineKeyboardMarkup:
        return types.InlineKeyboardMarkup(
            row_width=1,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="Подписаться!",
                        url=channel_link,
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="✅ Я уже подписан",
                        callback_data=f"subscribed:{user_id}:{channel}",
                    )
                ]
            ]
        )

    @classmethod
    def stickerset_ready_markup(cls, sticker_pack_url: str) -> types.InlineKeyboardMarkup:
        return types.InlineKeyboardMarkup(
            row_width=1,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="Стикер-пак",
                        url=sticker_pack_url,
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="Поделиться с друзьями!",
                        url="https://t.me/share/url?url=https://t.me/https://t.me/FaceSwap_Meme_Bot",
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="Попробовать еще раз?",
                        callback_data="again",
                    )
                ]
            ]
        )

    @classmethod
    def admin_menu(cls):
        menu: ReplyKeyboardMarkup = types.ReplyKeyboardMarkup(
            row_width=1,
            resize_keyboard=True,
            one_time_keyboard=True,
        ).add(
            types.KeyboardButton("Показать пул каналов рекламы"),
            types.KeyboardButton("Добавить канал в пул рекламы"),
            types.KeyboardButton("Удалить канал из пула реклам"),
            types.KeyboardButton("Список админов"),
            types.KeyboardButton("Добавить админа"),
            types.KeyboardButton("Удалить админа"),
            types.KeyboardButton("Логи"),
            types.KeyboardButton("/home"),
        )
        return menu

