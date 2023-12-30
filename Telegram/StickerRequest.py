import requests
import json
import os
from Telegram.Config import basedir


class StickerPackRequest:

    def __init__(self):
        self.__bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.sticker_format = 'static'
        self.sticker_type = 'regular'

    def uploadStickerFile(self, user_id: int, filepath: str) -> json:

        url = f'https://api.telegram.org/bot{self.__bot_token}/uploadStickerFile'

        files = {
            'sticker': open(filepath, 'rb')
        }

        params = {
            'user_id': user_id,
            'sticker_format': self.sticker_format
        }

        response = requests.post(url, files=files, params=params)

        return response.json()

    def createNewStickerSet(self, user_id: int, name: str, title: str, stickers: list) -> json:
        url = f'https://api.telegram.org/bot{self.__bot_token}/createNewStickerSet'

        data = {
            "user_id": user_id,
            "name": name,
            "title": title,
            "sticker_format": self.sticker_format,
            "sticker_type": self.sticker_type,
            "stickers": stickers
        }

        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.post(url, json=data, headers=headers)

        return response.json()

    def getStickerSet(self, sticker_pack_name: str):
        url = f'https://api.telegram.org/bot{self.__bot_token}/getStickerSet'

        data = {
            "name": sticker_pack_name
        }

        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.post(url, json=data, headers=headers)

        return response.json()


if __name__ == "__main__":
    sr = StickerPackRequest()
    # print(sr.uploadStickerFile(
    #     user_id="406149871",
    #     filepath=os.path.join(basedir, 'FaceSwap', 'outputs', '406149871', 'prepared_images', 'mem1_406149871.png')
    # ))

    # print(sr.getStickerSet(sticker_pack_name="face_swap_meme_by_FaceSwap_Meme_Bot"))




