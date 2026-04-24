import os

import bcrypt
import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv


load_dotenv()

class Database:
    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.database = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASS")
        self.port = os.getenv("DB_PORT")

        self.conn = None
        self.userId = None
        self.userName = None
        self.userRole = None
        self.last_error = ""

    def connection(self):
        if self.conn is not None:
            return self.conn

        try:
            self.conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            self.last_error = ""
            return self.conn
        except Exception:
            self.last_error = "Erreur de connexion a la base de donnees"
            self.conn = None
            return None

    def _cursor(self):
        conn = self.connection()
        if conn is None:
            return None
        return conn.cursor()


    def close(self):
        if self.conn is not None:
            self.conn.close()
    



    def listUsers(self):
        cursor = self._cursor()
        if cursor is None:
            return []

        cursor.execute("SELECT id, username, role FROM users ORDER BY id")
        records = cursor.fetchall()
        cursor.close()
        self.last_error = ""

        return records


    def addUser(self, username, password, role):
        cursor = self._cursor()
        if cursor is None:
            return False

        try:
            salt = bcrypt.gensalt()
            hashPassword = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

            cursor.execute(
                "INSERT INTO users (username, hashpassword, role) VALUES (%s, %s, %s)",
                (username, hashPassword, role)
            )
            self.connection().commit()
            return True
        except Error:
            self.last_error = "Operation SQL impossible"
            self.connection().rollback()
            return False
        finally:
            cursor.close()


    def updateRole(self, username, newRole):
        cursor = self._cursor()
        if cursor is None:
            return False

        try:
            cursor.execute("UPDATE users SET role = %s WHERE username = %s", (newRole, username))
            affected = cursor.rowcount
            self.connection().commit()
            return affected > 0
        except Error:
            self.last_error = "Operation SQL impossible"
            self.connection().rollback()
            return False
        finally:
            cursor.close()


    def setPassword(self, username, newPassword):
        cursor = self._cursor()
        if cursor is None:
            return False

        try:
            salt = bcrypt.gensalt()
            hashPassword = bcrypt.hashpw(newPassword.encode("utf-8"), salt).decode("utf-8")

            cursor.execute("UPDATE users SET hashpassword = %s WHERE username = %s", (hashPassword, username))
            affected = cursor.rowcount
            self.connection().commit()
            return affected > 0
        except Error:
            self.last_error = "Operation SQL impossible"
            self.connection().rollback()
            return False
        finally:
            cursor.close()


    def deleteUser(self, username):
        cursor = self._cursor()
        if cursor is None:
            return False

        try:
            cursor.execute("DELETE FROM users WHERE username = %s", (username,))
            affected = cursor.rowcount
            self.connection().commit()
            return affected > 0
        except Error:
            self.last_error = "Operation SQL impossible"
            self.connection().rollback()
            return False
        finally:
            cursor.close()
    


    def validateCredentials(self, username, password):
        cursor = self._cursor()
        if cursor is None:
            return False

        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        record = cursor.fetchone()
        cursor.close()

        if record:
            hash_stocke = record[2]

            if bcrypt.checkpw(password.encode('utf-8'), hash_stocke.encode('utf-8')):
                self.userId = record[0]
                self.userName = record[1]
                self.userRole = record[3]
                self.last_error = ""
                return True

            self.last_error = "Identifiants incorrects"
        return False
    

    def getUserInfo(self):
        if self.userId is None or self.userName is None or self.userRole is None:
            return None

        return {
            "id": self.userId,
            "username": self.userName,
            "role": self.userRole
        }