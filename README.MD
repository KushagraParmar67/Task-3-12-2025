# Task API Assignment

This project implements a simple Task Management API using **FastAPI** with in-memory storage.  
The API provides task creation, advanced filtering, sorting, pagination, and analytics using **pandas**.

---

## Features

- Create tasks with validation
- List tasks with:
  - Status filter
  -  search (title and description)
  - Date range filtering for created and updated time
  - Sorting by any field
  - Pagination with metadata
- Analytics summary:
  - Status distribution
  - Weekly task completion rate
  - Average tasks created per day
- Proper HTTP status codes and error validation
- In-memory data storage (no database required)

---

## Technology Stack

- Python 3.10+
- FastAPI
- Uvicorn
- Pydantic
- Pandas

---

## Setup Instructions

### 1. Create virtual environment (recommended)
```
python3 -m venv venv
```
```
Linux / macOS
source venv/bin/activate
```
```
Windows (Command Prompt)
venv\Scripts\activate.bat
```


### 2. Install dependencies
```
pip install -r requirements.txt
```


### 3. Run the API server
```
cd root/Task-3-12-2025/app
### Then run 
uvicorn main:app --reload
```


API documentation will be available at:

Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## API Endpoints

| Method | Endpoint              | Description                                      |
|--------|-----------------------|--------------------------------------------------|
| POST   | `/tasks`              | Create a new task                               |
| GET    | `/tasks`              | List tasks with filters, sorting, pagination    |
| GET    | `/analytics/summary`  | Analytics summary using pandas                  |

---

## Example `curl` Commands

### Create a task
```
curl -X POST "http://127.0.0.1:8000/tasks"
-H "Content-Type: application/json"
-d '{"title": "Task One", "description": "Test", "status": "pending"}'
```


### List all tasks
```
curl "http://127.0.0.1:8000/tasks"
```


### Filter by status
```
curl "http://127.0.0.1:8000/tasks?status=completed"

```

### Search tasks
```
curl "http://127.0.0.1:8000/tasks?search=Task"
```


### Sorting
```
curl "http://127.0.0.1:8000/tasks?sort_by=title&order=asc"
```


### Pagination
```
curl "http://127.0.0.1:8000/tasks?page=2&page_size=5"
```


### Analytics
```
curl "http://127.0.0.1:8000/analytics/summary"
```


---

## Design Choices

- **FastAPI** was selected for ease of creating structured RESTful APIs and automatic documentation via Swagger UI.
- **Pydantic** models ensure strict validation for input and output formatting.
- **In-memory storage** keeps the implementation simple since persistent storage was not required by the task.
- **Query parameters** allow flexible filtering and sorting without modifying API routes.
- **Pandas** is used for analytics to simplify data aggregation and statistical calculations.
- **Error handling** ensures clear responses for client-side and validation issues
