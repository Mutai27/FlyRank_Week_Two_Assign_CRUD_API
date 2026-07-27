#import dependant libraries and modules
from fastapi import FastAPI,HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

#initalize a fastapi app
app = FastAPI()

#Stage 1
#check for root and health status of the api
@app.get("/")
def get_root():
    '''Return the info about the api'''
    return {
        "name": "FastAPI",
        "version": "1.0",
        "endpoints": "/tasks"

    }

@app.get("/health")
def get_health():
    '''check for the app status'''
    return "status ok"

#create a dictionary of tasks to perfom
tasks_db= [
    {"id": 1, "title": "Buy groceries", "doen": False},
    {"id": 2, "title": "Read a book", "done": False },
    {"id": 3, "title": "Buld API", "done": False}
]

#initiate task_id counter
next_id = 4

#Create a class to define the schema of the to-do items
class TaskCreate(BaseModel):
    id: Optional[int] = None
    title: str

#create a class for optional field of the todo instances
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

#stage 2 : read the list and return 1 task
@app.get("/tasks")
def list_tasks():
    '''return the entire tasks list'''
    return tasks_db

#get a specific task from the db
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    '''Get a single task in the db by using ID'''
    for task in tasks_db:
        if task["id"]==task_id:
            return task
    raise HTTPException(
        status_code= status.HTTP_404_NOT_FOUND,
        detail = f"Task {task_id} not found"

    )

#stage 3: Create post a new task
@app.post("/tasks", status_code= status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate):
    '''Create a new task into the task_db with validation'''
    global next_id

    if not task_data.title.strip():
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            
        )
    #add new task
    new_task = {
        "id": next_id,
        "title": task_data.strip(),
        "done": False
    }
    tasks_db.append(new_task)
    next_id +=1
    return new_task

# Stage 4: Put and Delete tasks
#update task on title and/or completeness
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_data: TaskUpdate):
    '''Update task by title or done'''
    for task in tasks_db:
        if task["id"]==task_id:
            if task_data.title is not None:
                if not task_data.title.strip():
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail = "title cannot be empty"
                    )
                task["title"]= task_data.title
            if task_data.done is not None:
                task["doen"]=task_data.done
            return task
    raise HTTPException(
        status_code= status.HTTP_404_NOT_FOUND,
        detail= f"Task {task_id} could not be found"

    )    

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    '''delete task by id'''
    for index, task in enumerate(tasks_db):
        if task["id"] == task_id:
            tasks_db.pop(index)
            return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task {task_id} not found"
    
    )
