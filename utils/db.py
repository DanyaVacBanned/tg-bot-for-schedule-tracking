import sqlite3

class Database:
    def __init__(self, db_file) -> None:
        try:
            self.connection = sqlite3.connect(db_file)
        except Exception as ex:
            print(f'Ошибка подключения к базе данных:\n{ex}')
        self.cursor = self.connection.cursor()
    

    def add_user(self, user_id, user_name, group_name):
        with self.connection:
            self.cursor.execute(
                """
                INSERT INTO users (user_id, user_name, group_name) VALUES (?,?,?)
                """, (user_id,user_name,group_name,))

    def get_user_by_id(self, user_id):
        with self.connection:
            user_data = self.cursor.execute(
                """
                SELECT user_name FROM users WHERE user_id = ?
                """, (user_id,)).fetchall()
        
        user = {
            'id':user_data[0][0],
            'name':user_data[0][1]
            }
        return user
            
    def get_user_group_by_id(self, user_id: int):
        with self.connection:
            group_name = self.cursor.execute(
                """
                SELECT group_name FROM users WHERE user_id = ?
                """, (user_id,)).fetchone()
        return group_name[0]
             


    def get_all_user_id(self):
        with self.connection:
            users_data = self.cursor.execute(
                """
                SELECT user_id FROM users
                """).fetchall()
            
        id_list = []
        for user in users_data:
            id_list.append(user[0])
        return id_list
    
    def delete_user_by_id(self, user_id):
        with self.connection:
            self.cursor.execute(
                """
                DELETE FROM users WHERE user_id = ?
                """, (user_id,))


