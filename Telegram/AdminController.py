import sqlite3


class AdminController:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_admin_table()
        self.create_channel_table()

    def create_admin_table(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS admins (
                                user_id INTEGER PRIMARY KEY
                                )''')
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating admins table: {e}")

    def create_channel_table(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS channels (
                                channel_name TEXT PRIMARY KEY,
                                channel_link TEXT
                                )''')
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating channels table: {e}")

    def add_admin(self, user_id):
        try:
            self.cursor.execute("INSERT INTO admins (user_id) VALUES (?)", (user_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding admin: {e}")

    def remove_admin(self, user_id):
        try:
            self.cursor.execute("DELETE FROM admins WHERE user_id=?", (user_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error removing admin: {e}")

    def is_admin(self, user_id):
        try:
            self.cursor.execute("SELECT * FROM admins WHERE user_id=?", (user_id,))
            return bool(self.cursor.fetchone())
        except sqlite3.Error as e:
            print(f"Error checking admin status: {e}")
            return False

    def add_channel(self, channel_name, channel_link):
        try:
            self.cursor.execute("INSERT INTO channels (channel_name, channel_link) VALUES (?, ?)", (channel_name, channel_link))
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            print(f"Error adding channel: {e}")

    def remove_channel(self, channel_name):
        try:
            self.cursor.execute("DELETE FROM channels WHERE channel_name=?", (channel_name,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error removing channel: {e}")

    def get_channel_link(self, channel_name):
        try:
            self.cursor.execute("SELECT channel_link FROM channels WHERE channel_name=?", (channel_name,))
            result = self.cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        except sqlite3.Error as e:
            print(f"Error retrieving channel link for {channel_name}: {e}")
            return None

    def get_all_channels(self):
        try:
            self.cursor.execute("SELECT * FROM channels")
            channels = self.cursor.fetchall()
            return channels
        except sqlite3.Error as e:
            print(f"Error retrieving channels: {e}")
            return []

    def __del__(self):
        self.conn.close()
