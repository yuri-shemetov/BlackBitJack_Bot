import sqlite3


class Settings:

    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения, если БД не существует - создаем ее"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS settings (id INTEGER AUTO_INCREMENT PRIMARY KEY, \
                        usd_byn DECIMAL DEFAULT (3.1), currency_rate DECIMAL DEFAULT (142800),  \
                        fees DECIMAL DEFAULT (6.0), percent DECIMAL DEFAULT (4.5))")


    # def get_all_settings(self, usd_byn, currency_rate, fees, percent):
    #     """Get all settings"""
    #     with self.connection:
    #         return self.cursor.execute("SELECT `usd_byn`, `currency_rate`, `fees`, `percent` FROM `settings`", (usd_byn, currency_rate, fees, percent)).fetchall()
    
    def get_usd_byn(self, usd_byn):
        with self.connection:
            return self.cursor.execute(
                "SELECT `usd_byn` FROM `settings`", (usd_byn)).fetchall()    

    def update_usd_byn(self, usd_byn):
        with self.connection:
            return self.cursor.execute(
                "UPDATE `settings` SET `usd_byn` = ?",
                (usd_byn)
            )

    def get_currency_rate(self, currency_rate):
        with self.connection:
            return self.cursor.execute(
                "SELECT `currency_rate` FROM `settings`", (currency_rate)).fetchall()

    def update_currency_rate(self, currency_rate):
        with self.connection:
            return self.cursor.execute(
                "UPDATE `settings` SET `currency_rate` = ?",
                (currency_rate)
            )

    def get_fees(self, fees):
        with self.connection:
            return self.cursor.execute(
                "SELECT `fees` FROM `settings`", (fees)).fetchall()

    def update_fees(self, fees):
        with self.connection:
            return self.cursor.execute(
                "UPDATE `settings` SET `fees` = ?",
                (fees)
            )

    def get_percent(self, percent):
        with self.connection:
            return self.cursor.execute(
                "SELECT `percent` FROM `settings`", (percent)).fetchall()

    def update_percent(self, percent):
        with self.connection:
            return self.cursor.execute(
                "UPDATE `settings` SET `percent` = ?",
                (percent)
            )


    def close(self):
        """Close DB"""
        self.connection.close()