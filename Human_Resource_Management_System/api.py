from ninja import NinjaAPI
from employeemanagement.api import router as employees_router

api = NinjaAPI(
  title="HRMS API",
  version="0.1.1",
  description="Rest API for Human Resource Management System"
)

api.add_router("/employees/", employees_router)
