import pandas as pd
import csv
import os
from datetime import datetime

tasks_csv_path = os.path.join('data', 'tasks.csv')

def generate_new_task_id():
    if os.path.exists(tasks_csv_path) and os.path.getsize(tasks_csv_path) > 0:
        tasks_df = pd.read_csv(tasks_csv_path)

        if 'TaskID' in tasks_df.columns and not tasks_df['TaskID'].empty:
            return str(tasks_df['TaskID'].max() + 1)
        else:
            return "1"
    else:
        return "1"



def create_task(task_name, description, assigned_to, assigned_by, status, priority, date_assigned, date_start, time_to_do, date_end, deadline):
    task_id = generate_new_task_id()
    date_assigned = date_assigned.strftime('%Y-%m-%d %H:%M') if isinstance(date_assigned, datetime) else date_assigned
    date_start = date_start.strftime('%Y-%m-%d %H:%M') if isinstance(date_start, datetime) else date_start
    date_end = date_end.strftime('%Y-%m-%d %H:%M') if isinstance(date_end, datetime) and date_end else date_end  
    deadline = deadline.strftime('%Y-%m-%d %H:%M') if isinstance(deadline, datetime) else deadline
    with open(tasks_csv_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([task_id, task_name, description, assigned_to, assigned_by, status, priority, date_assigned, date_start, time_to_do, date_end, deadline])
    print(f"Task '{task_name}' created successfully.")


def read_tasks():
    tasks = pd.read_csv(tasks_csv_path)
    return tasks


def update_task(task_id, **kwargs):
    tasks = pd.read_csv(tasks_csv_path)
    task_index = tasks[tasks['TaskID'] == task_id].index

    for key, value in kwargs.items():
        if key in tasks.columns:
            tasks.loc[task_index, key] = value

    tasks.to_csv(tasks_csv_path, index=False)
    print(f"Task ID {task_id} updated.")


def delete_task(task_id):
    tasks = pd.read_csv(tasks_csv_path)
    tasks = tasks[tasks['TaskID'] != task_id]
    tasks.to_csv(tasks_csv_path, index=False)
    print(f"Task ID {task_id} deleted.")


#1
def task_completion_rate_by_team(menago_ID):
    tasks = read_tasks()
    total_tasks = tasks[tasks['AssignedBy'] == menago_ID].shape[0]
    completed_tasks = tasks[(tasks['AssignedBy'] == menago_ID) & (tasks['Status'] == 'Completed')].shape[0]
    inProgress_tasks = tasks[(tasks['AssignedBy'] == menago_ID) & (tasks['Status'] == 'InProgress')].shape[0]
    return (completed_tasks / total_tasks) * 100, (inProgress_tasks / total_tasks) * 100


#2
def task_completion_rate_by_employee(employee_ID):
    tasks = read_tasks()
    total_tasks = tasks[tasks['AssignedTo'] == employee_ID].shape[0]
    completed_tasks = tasks[(tasks['AssignedTo'] == employee_ID) & (tasks['Status'] == 'Completed')].shape[0]
    inProgress_tasks = tasks[(tasks['AssignedTo'] == employee_ID) & (tasks['Status'] == 'InProgress')].shape[0]
    return (completed_tasks / total_tasks) * 100, (inProgress_tasks / total_tasks) * 100


#3
def average_time_per_done_task_by_team(menago_ID):
    tasks = read_tasks()

    tasks['DateEnd'] = pd.to_datetime(tasks['DateEnd'], errors='coerce')
    tasks['DateStart'] = pd.to_datetime(tasks['DateStart'], errors='coerce')
    
    employee_tasks = tasks[(tasks['AssignedBy'] == menago_ID) & (tasks['Status'] == 'Completed')]
    
    employee_tasks['MeanTime'] = (employee_tasks['DateEnd'] - employee_tasks['DateStart']).dt.hours
    
    return employee_tasks['MeanTime'].mean() if not employee_tasks.empty else 0


#4
def average_time_per_done_task_by_employee(employee_ID):
    tasks = read_tasks()

    tasks['DateEnd'] = pd.to_datetime(tasks['DateEnd'], errors='coerce')
    tasks['DateStart'] = pd.to_datetime(tasks['DateStart'], errors='coerce')
    
    employee_tasks = tasks[(tasks['AssignedTo'] == employee_ID) & (tasks['Status'] == 'Completed')]
    
    employee_tasks['MeanTime'] = (employee_tasks['DateEnd'] - employee_tasks['DateStart']).dt.hours
    
    return employee_tasks['MeanTime'].mean() if not employee_tasks.empty else 0

#5
def average_time_they_wanted_per_task_by_team(menago_ID):
    tasks = read_tasks()

    tasks['TimeToDo'] = pd.to_datetime(tasks['TimeToDo'], errors='coerce')
    
    employee_tasks = tasks[(tasks['AssignedBy'] == menago_ID) & (tasks['Status'] == 'Completed')]
    
    employee_tasks['MeanTime'] = (employee_tasks['TimeToDo']).dt.hours
    
    return employee_tasks['MeanTime'].mean() if not employee_tasks.empty else 0


#6
def average_time_they_wanted_per_task_by_employee(employee_ID):
    tasks = read_tasks()

    tasks['TimeToDo'] = pd.to_datetime(tasks['TimeToDo'], errors='coerce')
    
    employee_tasks = tasks[(tasks['AssignedTo'] == employee_ID) & (tasks['Status'] == 'Completed')]
    
    employee_tasks['MeanTime'] = (employee_tasks['TimeToDo']).dt.hours
    
    return employee_tasks['MeanTime'].mean() if not employee_tasks.empty else 0

#7
def overdue_tasks_count_by_team(menago_ID):
    tasks = read_tasks()
    today = datetime.now()
    overdue_tasks = tasks[(tasks['AssignedBy'] == menago_ID) & (pd.to_datetime(tasks['Deadline']) < today) & (tasks['Status'] != 'Completed')]
    return overdue_tasks
#.shape[0]

#8
def overdue_tasks_count_by_employee(employee_ID):
    tasks = read_tasks()
    today = datetime.now()
    overdue_tasks = tasks[(tasks['AssignedTo'] == employee_ID) & (pd.to_datetime(tasks['Deadline']) < today) & (tasks['Status'] != 'Completed')]
    return overdue_tasks



# 1. Individual Task Completion Rate
def task_completion_rate(employee_ID):
    tasks = read_tasks()
    total_tasks = tasks[tasks['AssignedTo'] == employee_ID].shape[0]
    completed_tasks = tasks[(tasks['AssignedTo'] == employee_ID) & (tasks['Status'] == 'Completed')].shape[0]
    return (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

# 2. Average Time Spent on Tasks per Employee
def average_time_per_task(employee_ID):
    tasks = read_tasks()
    employee_tasks = tasks[tasks['AssignedTo'] == employee_ID]
    return employee_tasks['TimeSpent'].mean() if not employee_tasks.empty else 0

# 3. Employee Workload Overview
def workload_overview(employee_ID):
    tasks = read_tasks()
    return tasks[tasks['AssignedTo'] == employee_ID]['Status'].value_counts().to_dict()

# 4. Number of Overdue Tasks per Employee
def overdue_tasks_count(employee_ID):
    tasks = read_tasks()
    today = datetime.now()
    overdue_tasks = tasks[(tasks['AssignedTo'] == employee_ID) & (pd.to_datetime(tasks['Deadline']) < today) & (tasks['Status'] != 'Completed')]
    return overdue_tasks.shape[0]

# 5. Employee Efficiency Ratio
def efficiency_ratio(employee_ID):
    tasks = read_tasks()
    completed_tasks = tasks[(tasks['AssignedTo'] == employee_ID) & (tasks['Status'] == 'Completed')]
    total_time_spent = completed_tasks['TimeSpent'].sum()
    return (completed_tasks.shape[0] / total_time_spent) if total_time_spent > 0 else 0


#zamiast czasu dac procent wykonanych zadan ktore sa do zrobienia konkretnego dnia
#def average_time_for_completed_tasks_by_employee(task_name, employee_ID):
    
 #   tasks = read_tasks()

 #   # Filter tasks by TaskName, AssignedTo, and Status
 #   filtered_tasks = tasks[(tasks['TaskName'] == task_name) & 
  #                         (tasks['AssignedTo'] == employee_ID) & 
  #                     (tasks['Status'] == 'Completed')]

    # Check if there are any completed tasks with the given TaskName and Employee
  #  if not filtered_tasks.empty:
    # Calculate the average execution time
 #       average_time = filtered_tasks['TimeSpent'].mean()
 #       return average_time
#    else:
  #      return "No completed tasks found for the given task name and employee."
