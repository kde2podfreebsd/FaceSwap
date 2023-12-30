import os
from Telegram.StickerRequest import StickerPackRequest
from Telegram.Config import basedir


class StickerPackMiddleware(StickerPackRequest):

    def __init__(self):
        super().__init__()

    def create_sticker_pack(self, user_id, name, title):
        folder_path = os.path.join(basedir, 'FaceSwap', 'outputs', str(user_id), 'prepared_images')
        sticker_files = os.listdir(folder_path)

        uploaded_stickers = []

        for file in sticker_files:
            file_path = os.path.join(folder_path, file)
            response = self.uploadStickerFile(user_id, file_path)

            if response.get('ok', False):
                file_id = response['result']['file_id']
                uploaded_stickers.append({
                    "sticker": file_id,
                    "emoji_list": ["😂"],
                    "keywords": ["мем"]
                })
        if uploaded_stickers:
            response = self.createNewStickerSet(user_id, name, title, uploaded_stickers)
            return response
        else:
            return {"ok": False, "message": "No stickers were uploaded."}


if __name__ == "__main__":
    spm = StickerPackMiddleware()
    spm.create_sticker_pack(user_id=406149871, name="face_swap_meme_by_FaceSwap_Meme_Bot", title="Face Swap Meme by @donqhomo")