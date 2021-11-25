from apps.ref.models.employee import Employee
from apps.ref.schemas.employee import EmployeeCreate, EmployeeUpdate
from core.crud import CRUDBase


class CRUDEmployee(CRUDBase[Employee, EmployeeCreate, EmployeeUpdate]):
    pass


employee = CRUDEmployee(Employee)
