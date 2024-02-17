import sqlite3
from datetime import datetime



class DataBaseHandler:  # odpowiada za obsługę bazy danych SQLite w kontekście transakcji
    def __init__(self, dbName="TaskApplication.db"):
        self.connection = sqlite3.connect(dbName)  # Otwiera połączenie z bazą danych
        self.createTables()
        if not self.is_default_accounts_added():
            self.add_default_accounts()
            self.mark_default_accounts_added()
    def createTables(self):
        self.createTableAccounts()
        self.createTableTask()
        self.createSettingsTable()

    def createSettingsTable(self):
        cursor = self.connection.cursor()
        cursor.execute('''
               CREATE TABLE IF NOT EXISTS settings (
                   id INTEGER PRIMARY KEY,
                   default_accounts_added INTEGER DEFAULT 0
               )
           ''')
        self.connection.commit()

    def is_default_accounts_added(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT default_accounts_added FROM settings WHERE id=1
        ''')
        row = cursor.fetchone()
        if row:
            return row[0] == 1
        return False

    def mark_default_accounts_added(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO settings (id, default_accounts_added) VALUES (1, 1)
        ''')
        self.connection.commit()
    def createTableTask(self):  # Tworzy tabelę "transactions" w bazie danych, jeżeli nie istnieje.
        cursor = self.connection.cursor()  # Tworzy obiekt kursora, który jest używany do wykonania operacji na bazie danych
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS task (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                osobaID INTEGER,
                przelozonyID INTEGER,
                status TEXT,
                piorytet INTEGER, 
                tytul TEXT, 
                opis TEXT, 
                uwagi TEXT,
                startTime DATETIME,
                endTime DATETIME,
                przepracowanyCzas INTEGER DEFAULT 0, --minuty
                FOREIGN KEY (osobaID) REFERENCES accounts(id),
                FOREIGN KEY (przelozonyID) REFERENCES accounts(id)
            )
        ''')
        self.connection.commit()  # Zatwierdza wprowadzone zmiany do bazy danych

    def createTableAccounts(self):  # Tworzy tabelę "transactions" w bazie danych, jeżeli nie istnieje.
        cursor = self.connection.cursor()  # Tworzy obiekt kursora, który jest używany do wykonania operacji na bazie danych
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                imie TEXT,
                nazwisko TEXT,
                login TEXT,
                haslo TEXT,
                stanowisko TEXT,
                jednostka TEXT,
                zespol TEXT NULL     -- opcjonalne 
            )
        ''')
        self.connection.commit()  # Zatwierdza wprowadzone zmiany do bazy danych
    def add_default_accounts(self):
        default_accounts = [
            ("Jan", "Kowalski","jan","abc", "Pracownik", "Główny", "Zespół A"),
            ("Jakub", "Boroszko","jakub","abc", "Pracownik", "Główny", "Zespół A"),
            ("Anna", "Nowak","anna","bc", "Manager", "Główna", "Zespół A"),
            ("Piotr", "Wiśniewski","piotr","Abc", "Dyrektor", "Główna", None)
        ]

        cursor = self.connection.cursor()
        cursor.executemany('''
            INSERT INTO accounts (imie, nazwisko,login,haslo, stanowisko, jednostka, zespol)
            VALUES (?, ?,?,?, ?, ?, ?)
        ''', default_accounts)
        self.connection.commit()


    def add_account(self, imie, nazwisko,login,haslo, stanowisko, jednostka, zespol):
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO accounts (imie, nazwisko,login,haslo, stanowisko, jednostka, zespol)
            VALUES (?, ?, ?,?,?, ?, ?)
        ''', (imie, nazwisko,login,haslo, stanowisko, jednostka, zespol))
        self.connection.commit()

    def authenticate_user(self, username, password):
        cursor = self.connection.cursor()
        cursor.execute('''
               SELECT * FROM accounts WHERE login=? AND haslo=?
           ''', (username, password))
        account = cursor.fetchone()
        if account:
            return {
                'id': account[0],
                'imie': account[1],
                'nazwisko': account[2],
                'login': account[3],
                'haslo': account[4],
                'stanowisko': account[5],
                'jednostka': account[6],
                'zespol': account[7]
            }
        else:
            return None

    def get_tasks_for_employee(self, pracownikID):
        cursor = self.connection.cursor()
        cursor.execute('''
               SELECT tytul FROM task WHERE osobaID=?
           ''', (pracownikID,))
        tasks = cursor.fetchall()
        return [{'tytul': task[0]} for task in tasks]

    def add_task(self, osobaID,przelozonyID, status, piorytet, tytul, opis, uwagi, startTime, endTime):
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO task (osobaID,przelozonyID, status, piorytet, tytul, opis, uwagi, startTime, endTime)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (osobaID,przelozonyID, status, piorytet, tytul, opis, uwagi, startTime, endTime))
        self.connection.commit()

    def get_employees(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT id, imie, nazwisko FROM accounts WHERE stanowisko="Pracownik"
        ''')
        employees = cursor.fetchall()
        return [{'id': emp[0], 'imie': emp[1], 'nazwisko': emp[2]} for emp in employees]

    def get_active_tasks_for_day(self, date, employee_id):
        cursor = self.connection.cursor()
        query = """
        SELECT * FROM task
        WHERE osobaID  = ? AND endTime >= ? 
        """
        date_str = date.strftime('%Y-%m-%d 00:00:00')
        cursor.execute(query, (employee_id, date_str))
        tasks = cursor.fetchall()

        task_list = []
        for task in tasks:
            task_start_time = datetime.strptime(task[8], '%Y-%m-%d %H:%M:%S')  # Convert string to datetime
            if task_start_time.date() >= date:
                task_list.append({
                    'id': task[0],
                    'osobaID': task[1],
                    'przelozonyID': task[2],
                    'status': task[3],
                    'piorytet': task[4],
                    'tytul': task[5],
                    'opis': task[6],
                    'uwagi': task[7],
                    'startTime': task[8],
                    'endTime': task[9],
                    'czas': task[10],
                })

        return task_list
