import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from task_manager import *
from auth import *
from datetime import datetime
from gui import *
import gui


tasks_csv_path = os.path.join('data', 'tasks.csv')


def przypisanie_pracownikow():
# UserID,Username,PasswordHash,Role,IdMenago,IdDyr
# dyrektor
    register_user("Dyrektor", "123", 3, 0, 0)
# menadzerowie
    register_user("Menag1", "123", 2, 0, 1)
    register_user("Menag2", "123", 2, 0, 1)
    register_user("Menag3", "123", 2, 0, 1)
# pracownicy menadzera1
    register_user("Prac1", "123", 1, 2, 0)
    register_user("Prac2", "123", 1, 2, 0)
    register_user("Prac3", "123", 1, 2, 0)
    register_user("Prac4", "123", 1, 2, 0)
#pracownicy menadzera2
    register_user("Prac5", "123", 1, 3, 0)
    register_user("Prac6", "123", 1, 3, 0)
    register_user("Prac7", "123", 1, 3, 0)
    register_user("Prac8", "123", 1, 3, 0)
#pracownicy menadzera3
    register_user("Prac9", "123", 1, 4, 0)
    register_user("Prac10", "123", 1, 4, 0)
    register_user("Prac11", "123", 1, 4, 0)
    register_user("Prac12", "123", 1, 4, 0)
    return 0


def przypisanie_zadan():

#TaskID,taskName, Description, AssignedTo, AssignedBy, Status, Priority, DateAssigned, DateStart, TimeToDo, DateEnd, Deadline
    #zadania dla przykładowego pracownika
    date_assigned = datetime.now()
    date_start = datetime(2024, 1, 5, 9, 0)  
    deadline = datetime(2024, 1, 15, 17, 0)  
    date_assigned_str = date_assigned.strftime('%Y-%m-%dT%H:%M')
    date_start_str = date_start.strftime('%Y-%m-%dT%H:%M')
    deadline_str = deadline.strftime('%Y-%m-%dT%H:%M')
    create_task("pierwsze zadanie","opis zadania 1",17,2,1,1,date_assigned_str,date_start_str,"x","nie wskazano",deadline_str)





    return 0

#przypisanie_pracownikow()
#przypisanie_zadan()

#create_task(1,1,1,1,1,1,1,1,1,1,1)
#today= datetime.now()
#print(today)
#kwargs = {"TaskName":"Spotkanie", "Description":"Jezeli sie uda poinformowac dominike o mozliwosci spotkania", "AssignedTo":"Jakub","DateAssigned":"Today","Deadline":"Tomorrow","Status":"In Progress","Priority":"topPriority"}#, "Status":"Completed"}
#update_task(1,**kwargs)


# # Convert to string in ISO 8601 format without seconds
# formatted_datetime_without_seconds = now.strftime('%Y-%m-%dT%H:%M')
# print(formatted_datetime_without_seconds)  # Output: YYYY-MM-DDTHH:MM


#delete_task(5)

