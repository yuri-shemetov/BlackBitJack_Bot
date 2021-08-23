import sqlite3

class SQLighter:

    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения, если БД не существует - создаем ее"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS subscriptions (id INTEGER AUTO_INCREMENT PRIMARY KEY, \
                        user_id VARCHAR (255) NOT NULL, premium BOOLEAN DEFAULT (False), price DECIMAL, \
                        rate CHAR (3), translation DECIMAL, address CHAR, photo BLOB, created CHAR)")

    def subscriber_exists(self, user_id):
        """Check user"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `subscriptions` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_subscriber(self, user_id, rate, price, translation, created, premium=False):
        """Add a new user"""
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO `subscriptions` (`user_id`, 'premium', 'rate', 'price', 'translation', 'created') "
                "VALUES(?, ?, ?, ?, ?, ?)",
                (user_id, premium, rate, price, translation, created)
            )

    def update_subscription(self, user_id, rate, price, translation, created):
        """Update user"""
        with self.connection:
            return self.cursor.execute(
                "UPDATE `subscriptions` SET `rate` = ?, `price` = ?, 'translation' = ?, 'created' = ? "
                "WHERE `user_id` = ?",
                (rate, price, translation, created, user_id)
            )

    def update_subscription_address(self, user_id, address):
        """Update address"""
        with self.connection:
            return self.cursor.execute(
                "UPDATE `subscriptions` SET `address` = ? WHERE `user_id` = ?",
                (address, user_id)
            )

    def update_subscription_photo(self, user_id, photo):
        """Update photo"""
        with self.connection:
            return self.cursor.execute(
                "UPDATE `subscriptions` SET `photo` = ? WHERE `user_id` = ?",
                (photo, user_id)
            )

    def get_subscriptions_all_price(self, user_id):
        """Get all price"""
        with self.connection:
            return self.cursor.execute("SELECT `price` FROM `subscriptions` WHERE `user_id` = ?", (user_id,)).fetchall()

    def get_subscriptions_translation(self, user_id):
        """Get bitcoins"""
        with self.connection:
            return self.cursor.execute("SELECT `translation` FROM `subscriptions` WHERE `user_id` = ?", (user_id,)).fetchall()

    def close(self):
        """Close DB"""
        self.connection.close()