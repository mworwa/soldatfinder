from database import Database


database = Database()


class Soldier:
    def __init__(self, chat_id: str, name: str, birthdate: str):
        self.chat_id = chat_id
        self.name = name
        self.birthdate = birthdate


class SoldierRepository:
    def add(self, chat_id: str, name: str, birthdate: str):
        conn = database.get_db_connection()
        conn.execute(
            "INSERT INTO soldiers (chat_id, name, birthdate) VALUES (?, ?, ?)",
            (chat_id, name, birthdate),
        )
        conn.commit()
        conn.close()

    def get_all(self) -> list[Soldier]:
        conn = database.get_db_connection()
        soldiers = conn.execute("SELECT * FROM soldiers").fetchall()
        conn.close()
        soldiers_list = [
            Soldier(
                chat_id=soldier["chat_id"],
                name=soldier["name"],
                birthdate=soldier["birthdate"],
            )
            for soldier in soldiers
        ]

        return soldiers_list

    def get_by_chat_id(self, chat_id: str) -> list[Soldier]:
        conn = database.get_db_connection()
        soldiers = conn.execute(
            "SELECT * FROM soldiers WHERE chat_id = ?", (chat_id,)
        ).fetchall()
        conn.close()

        soldiers_list = [
            Soldier(
                chat_id=soldier["chat_id"],
                name=soldier["name"],
                birthdate=soldier["birthdate"],
            )
            for soldier in soldiers
        ]

        return soldiers_list
