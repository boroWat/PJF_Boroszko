import sqlite3
from datetime import datetime, time, timedelta

from PySide6.QtCore import Qt


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
        self.createTableDay()

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

    def createTableDay(self):
        cursor = self.connection.cursor()
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS day (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        taskID INTEGER,
                        dzien DATE,
                        zaczecie DATETIME,
                        zakonczenie DATETIME,
                        FOREIGN KEY (taskID) REFERENCES task(id)
                    )
                ''')
        self.connection.commit()  # Zatwierdza wprowadzone zmiany do bazy danych

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
                dataDodania DATETIME,
                deadLine DATETIME,
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
            INSERT INTO task (osobaID,przelozonyID, status, piorytet, tytul, opis, uwagi, dataDodania, deadLine)
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
        print(date)
        cursor = self.connection.cursor()
        query = """
        SELECT * FROM task
        WHERE osobaID  = ? AND deadLine >= ?
        """

        cursor.execute(query, (employee_id, date))
        tasks = cursor.fetchall()
        task_list = []
        for task in tasks:
            print(task)
            #print(type(task[8]))
            #print(type(date))
            startDateTime = datetime.strptime(task[8], '%Y-%m-%d %H:%M:%S')
            startDate = startDateTime.date()
            #print(type(startDate))
            if(startDate<=date):
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

    def get_task_by_id(self, task_id):
        # Zapytanie SQL do pobrania zadania na podstawie jego ID
        query = "SELECT * FROM task WHERE id = ?"
        cursor = self.connection.cursor()
        cursor.execute(query, (task_id,))
        task = cursor.fetchone()
        if task:

            # Konwersja wyniku zapytania na słownik dla łatwiejszego dostępu
            task_dict = {
                'id': task[0],
                'tytul': task[5],
                'opis': task[6],
                'status': task[3],
                'uwagi': task[7]
            }
            return task_dict
        return None

    def update_task(self, task_id, start_time, end_time, status, comments, work_day):
        start_datetime = datetime.combine(datetime.today(),
                                          time(start_time.hour(), start_time.minute(), start_time.second()))
        end_datetime = datetime.combine(datetime.today(), time(end_time.hour(), end_time.minute(), end_time.second()))

        # Obliczenie czasu pracy jako różnicy między czasami
        czas = end_datetime - start_datetime
        total_minutes = czas.total_seconds() / 60


        # Sprawdzenie, czy istnieje już wpis dla tego zadania w danym dniu
        query_check_day = "SELECT * FROM day WHERE taskID = ? AND dzien = ?"
        values_check_day = (task_id, work_day)
        cursor = self.connection.cursor()
        cursor.execute(query_check_day, values_check_day)
        existing_day = cursor.fetchone()

        # Jeśli istnieje, aktualizuj wpis
        if existing_day:
            query_update_day = "UPDATE day SET zaczecie = ?, zakonczenie = ? WHERE taskID = ? AND dzien = ?"
            values_update_day = (start_time.toString(Qt.ISODate), end_time.toString(Qt.ISODate), task_id, work_day)
            cursor.execute(query_update_day, values_update_day)
        # Jeśli nie istnieje, dodaj nowy wpis
        else:
            query_insert_day = "INSERT INTO day (dzien, zaczecie, zakonczenie, taskID) VALUES (?, ?, ?, ?)"
            values_insert_day = (work_day, start_time.toString(Qt.ISODate), end_time.toString(Qt.ISODate), task_id)
            cursor.execute(query_insert_day, values_insert_day)
        pracaCzas = self.calkowityCzasPrzeprowaowanyZadania(task_id)
        # Aktualizacja statusu i uwag dla zadania
        query_update_task = "UPDATE task SET status = ?, uwagi = ?, przepracowanyCzas = ?  WHERE id = ?"
        values_update_task = (status, comments, pracaCzas, task_id)
        cursor.execute(query_update_task, values_update_task)

        self.connection.commit()

    def calkowityCzasPrzeprowaowanyZadania(self, task_id):
        cursor = self.connection.cursor()
        query = "SELECT DISTINCT dzien FROM day WHERE taskID = ?"
        cursor.execute(query, (task_id,))
        days = cursor.fetchall()  # Pobieramy wszystkie unikalne dni, w których występuje zadanie

        total_time = 0  # Inicjalizacja łącznego czasu pracy na 0
        for day in days:
            day_date = day[0]
            total_time += self.czasPracyNaDzien(day_date)
        print(f"Na zadanie {task_id}")
        print(total_time)
        return total_time

    def czasPracyNaDzien(self, day_date): # wszystkie taski na dzien  --------------- to jest git
        cursor = self.connection.cursor()
        query = "SELECT zaczecie, zakonczenie FROM day WHERE dzien = ?"
        cursor.execute(query, (day_date,))
        result = cursor.fetchall()  # Pobieramy wszystkie pasujące wiersze
        print ("KURWA")
        print(result)
        if result:
            total_time = 0  # Inicjalizacja łącznego czasu pracy na 0
            for row in result:
                start_timeS, end_timeS = row
                start_time = datetime.strptime(start_timeS, "%H:%M:%S")
                end_time = datetime.strptime(end_timeS, "%H:%M:%S")
                czas_pracy = (end_time - start_time).total_seconds() / 60  # Różnica czasu w minutach
                total_time += czas_pracy
            print(total_time)
            return total_time

        else:
            return 0

    def dayInfo(self, id,dzien):
        query = "SELECT * FROM day WHERE taskID = ? AND dzien = ?"
        cursor = self.connection.cursor()
        cursor.execute(query, (id,dzien))
        day = cursor.fetchone()
        if day:
            # Konwersja wyniku zapytania na słownik dla łatwiejszego dostępu
            task_dict = {
                'id': day[0],
                'zaczecie': day[3],
                'zakonczenie': day[4]
            }
            return task_dict

        return {
                'id': None,
                'zaczecie': '00:00:00',
                'zakonczenie': '00:00:00'
        }

    def sumaCzasuPracyWTygodniu(self, start_date):
        total_time_week = 0  # Inicjalizacja łącznego czasu pracy w tygodniu na 0
        for i in range(7):  # 7 dni w tygodniu
            day_date = start_date + timedelta(days=i)
            total_time_week += self.czasPracyNaDzien(day_date)

        return total_time_week

    def czasPracyNaDzienNaTask(self, day_date, taskID):
        cursor = self.connection.cursor()
        query = "SELECT zaczecie, zakonczenie FROM day WHERE dzien = ? AND taskID = ?"
        cursor.execute(query, (day_date, taskID))
        result = cursor.fetchall()  # Pobieramy wszystkie pasujące wiersze
        if result:
            total_time = 0  # Inicjalizacja łącznego czasu pracy na 0
            for row in result:
                start_timeS, end_timeS = row
                start_time = datetime.strptime(start_timeS, "%H:%M:%S")
                end_time = datetime.strptime(end_timeS, "%H:%M:%S")
                czas_pracy = (end_time - start_time).total_seconds() / 60  # Różnica czasu w minutach
                total_time += czas_pracy

            return total_time
        else:
            return 0
