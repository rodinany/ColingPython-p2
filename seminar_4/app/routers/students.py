from fastapi import APIRouter, status
from app.schemas.people import Student

router = APIRouter()

DB = [
    {
        "id": 1,
        "name": "Ivanov Ivan",
        "faculty": "philological"
    },
    {
        "id": 2,
        "name": "Petrov Ivan",
        "faculty": "sports"
    },
    {
        "id": 10,
        "name": "Kate Sivridova",
        "faculty": "mathematical"
    }
]

@router.get("/student/{student_id}")
def fetch_student(student_id: int) -> dict:
    
    result = [student for student in DB if student["id"] == student_id]
    if result:
        return result[0]

@router.get("/student/search/")
def search_students(keyword: str):
    result = [student for student in DB if keyword.lower() in student["name"].lower()]
    if result:
        return result

@router.post("/student/", status_code=status.HTTP_201_CREATED)
def create_student(student: Student):
    DB.append(student)
    return {"name": student.name}