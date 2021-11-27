
class Tasks():
    def __init__(self, tasks={}):
        self.tasks = {}

    def create_task(self):
        task_name = input('what is the name of the task?')
        task_priority = input('what is the priority of the task?')
        task_deadline = input('what is the deadline of the task?')
        task_status = input('what is the status of the task?')
        if task_name in self.tasks.keys():
            return "the task has created already"
        self.tasks[task_name] = [task_priority, task_deadline, task_status]

    def delete_task(self):
        task_name = input('please type the name of task that you want to delete')
        if task_name not in self.tasks.keys():
            return "this task is not found in the tasks"
        self.tasks.pop(task_name, None)

    def edit_task(self):
        task_name = input('please type the name of task that you want to edit')
        if task_name not in self.tasks.keys():
            return "this task is not found in the tasks", action()
        edit_value = input("""do you want to change the priority, due date or the status of the task?
    1) task name
    2) priority 
    2) deadline
    3) status""")
        if edit_value not in ('task name','priority', 'deadline','status'):
            return ("action is not found")
        new_value = input("type the new value please")
        if edit_value == 'task name' and new_value in self.tasks.keys():
            return ("the name of the task is already taken")
        if edit_value == 'task name' and new_value not in self.tasks.keys() :
            self.tasks[new_value] = self.tasks[edit_value]
            del self.tasks[edit_value]
            pass
        else:
            self.tasks[edit_value] = new_value
    def __repr__(self):
        return f"Tasks Lists: {print(self.tasks.items())}"

# task1 = Tasks()
# print(task1)
# task1.create_task()
# print(task1)

change_tasks = True
while change_tasks:
    users = []
    name = input("type your name please")
    if name not in users:
        users.append(name)
        name = Tasks()
    def action():
        action = input("""what do you want to do?
1) Create a task
2) Delete a task
3) Edit a task
 4) nothing""")
        if action == "Create a task":
            create_task()
        elif action == "Delete a task":
            delete_task()
        elif action == "Edit a task":
            edit_task()
        elif action == "Nothing":
            change_tasks = False
    action()

## Task                     Priority            Due Date
## Do homework           High                28/11/2021
## Clean the house       Mid                 30/11/2021
## Buy a Car             Low                 15/12/2021

#{"Do homework" : ["High", "Due_Date"]