from ninja import NinjaAPI
from employeemanagement.api import router as employees_router
from punchmanagement.api import router as punch_router
from leavemanagement.api import router as leave_router

api = NinjaAPI(
  title="HRMS API",
  version="0.1.1",
  description="Rest API for Human Resource Management System"
)

api.add_router("/employees/", employees_router)
api.add_router("/punch/", punch_router)
api.add_router("/leave/", leave_router)
