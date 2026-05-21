from ninja import Router
from typing import List
from django.shortcuts import get_object_or_404
# from .models import Employee
# Assuming you create a Pydantic schema for data validation
# from .schemas import EmployeeOutSchema

router = Router(tags=["employee"])

# @router.post("/login")
# def login(request):
#   return Response

# @router.get("/", response=List[EmployeeOutSchema])
# def list_employees(request):
#   return Employee.objects.filter(is_active=True)

# @router.get("/{employee_id}/", response=EmployeeOutSchema)
# def get_employee(request, employee_id: int):
#   return get_object_or_404(Employee, id=employee_id)
