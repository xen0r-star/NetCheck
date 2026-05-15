import os
import re
from datetime import datetime, timedelta

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
        self.password_reset_required = False

        self.max_failed_attempts = 5
        self.lockout_minutes = 15

        self.password_min_length = 13

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

        cursor.execute(
            """
            SELECT id, username, role, is_temporary, failed_attempts, locked_until, last_login
            FROM users
            ORDER BY id
            """
        )
        records = cursor.fetchall()
        cursor.close()
        self.last_error = ""

        return records


    def addUser(self, username, password, role, is_temporary=True):
        cursor = self._cursor()
        if cursor is None:
            return False

        try:
            if not is_temporary and not self._is_password_strong(password):
                self.last_error = "PASSWORD_WEAK"
                return False

            salt = bcrypt.gensalt()
            hashPassword = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

            cursor.execute(
                """
                INSERT INTO users (username, hashpassword, role, is_temporary, failed_attempts, locked_until, last_login)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (username, hashPassword, role, is_temporary, 0, None, None)
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
            if not self._is_password_strong(newPassword):
                self.last_error = "PASSWORD_WEAK"
                return False

            salt = bcrypt.gensalt()
            hashPassword = bcrypt.hashpw(newPassword.encode("utf-8"), salt).decode("utf-8")

            cursor.execute(
                """
                UPDATE users
                SET hashpassword = %s,
                    is_temporary = %s,
                    failed_attempts = %s,
                    locked_until = %s
                WHERE username = %s
                """,
                (hashPassword, False, 0, None, username)
            )
            affected = cursor.rowcount
            self.connection().commit()
            return affected > 0
        except Error:
            self.last_error = "Operation SQL impossible"
            self.connection().rollback()
            return False
        finally:
            cursor.close()


    def setPasswordAndActivate(self, username, newPassword):
        return self.setPassword(username, newPassword)


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

        self.password_reset_required = False

        cursor.execute(
            """
            SELECT id, username, hashpassword, role, is_temporary, failed_attempts, locked_until, last_login
            FROM users
            WHERE username = %s
            """,
            (username,)
        )
        record = cursor.fetchone()
        cursor.close()

        if record:
            hash_stocke = record[2]
            is_temporary = bool(record[4])
            failed_attempts = record[5] if record[5] is not None else 0
            locked_until = record[6]

            now = datetime.utcnow()
            if locked_until and locked_until > now:
                self.last_error = "ACCOUNT_LOCKED"
                return False

            if bcrypt.checkpw(password.encode('utf-8'), hash_stocke.encode('utf-8')):
                if is_temporary:
                    self.last_error = "PASSWORD_RESET_REQUIRED"
                    self.password_reset_required = True
                    return False

                self._reset_failed_attempts(username)
                self._set_last_login(username)
                self.userId = record[0]
                self.userName = record[1]
                self.userRole = record[3]
                self.last_error = ""
                return True

            self._register_failed_attempt(username, failed_attempts)
            self.last_error = "Identifiants incorrects"
        return False


    def _is_password_strong(self, password):
        if not password or len(password) < self.password_min_length:
            return False

        if not re.search(r"[A-Z]", password):
            return False

        if not re.search(r"[a-z]", password):
            return False

        if not re.search(r"\d", password):
            return False

        if not re.search(r"[^A-Za-z0-9]", password):
            return False

        return True


    def _register_failed_attempt(self, username, failed_attempts):
        cursor = self._cursor()
        if cursor is None:
            return

        try:
            next_attempts = failed_attempts + 1
            locked_until = None

            if next_attempts >= self.max_failed_attempts:
                locked_until = datetime.utcnow() + timedelta(minutes=self.lockout_minutes)

            cursor.execute(
                """
                UPDATE users
                SET failed_attempts = %s,
                    locked_until = %s
                WHERE username = %s
                """,
                (next_attempts, locked_until, username)
            )
            self.connection().commit()
        except Error:
            self.connection().rollback()
        finally:
            cursor.close()


    def _reset_failed_attempts(self, username):
        cursor = self._cursor()
        if cursor is None:
            return

        try:
            cursor.execute(
                "UPDATE users SET failed_attempts = %s, locked_until = %s WHERE username = %s",
                (0, None, username)
            )
            self.connection().commit()
        except Error:
            self.connection().rollback()
        finally:
            cursor.close()


    def _set_last_login(self, username):
        cursor = self._cursor()
        if cursor is None:
            return

        try:
            cursor.execute(
                "UPDATE users SET last_login = %s WHERE username = %s",
                (datetime.utcnow(), username)
            )
            self.connection().commit()
        except Error:
            self.connection().rollback()
        finally:
            cursor.close()


    def getLastLogin(self, username):
        cursor = self._cursor()
        if cursor is None:
            return None

        cursor.execute("SELECT last_login FROM users WHERE username = %s", (username,))
        record = cursor.fetchone()
        cursor.close()

        return record[0] if record else None
    

    def getUserInfo(self):
        if self.userId is None or self.userName is None or self.userRole is None:
            return None

        return {
            "id": self.userId,
            "username": self.userName,
            "role": self.userRole
        }