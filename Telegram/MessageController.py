from Telegram.Config import singleton
from Telegram.Config import bot


@singleton
class MsgMiddleware:
    storage = {}

    def add_message_id(self, user_id, message_id):
        self.storage[int(user_id)] = message_id

    def delete_message_id(self, user_id):
        user_id = int(user_id)
        if user_id in self.storage:
            if self.storage[user_id] is not None:
                bot.delete_message(user_id, self.storage[user_id])
                self.storage[user_id] = None

