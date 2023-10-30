from injector import inject

from symbiot_lib.objects.operation import Operation
from symbiot_lib.objects.record import Record
from symbiot_server.database.repositories.operation_repository import OperationRepository
# noinspection PyPackages
from .symbiot_service import SymbiotService


class OperationService(SymbiotService):
    division_name = "operation"

    @inject
    def __init__(
            self,
            operation_repository: OperationRepository):
        super().__init__()
        self._repository = operation_repository

    @property
    def operations(self) -> list[Operation]:
        return self._repository.get_all()

    def save_record(self, record: Record):
        self._repository.update_record(record)

    def get_record(self, id_: int):
        return self._repository.get_record_by_id(id_)

    def operation(self, by: str, content) -> Operation:
        match by:
            case "record_id":
                for operation in self.operations:
                    if content in [record.id for record in operation.records]:
                        return operation
                    raise ValueError(f"no record with id: {content}")
            case _: raise NotImplementedError(f"not implemented operation by {by}")

    def record(self, by: str, content) -> Record:
        match by:
            case "id": return self.get_record(content)
            case _: raise NotImplementedError(f"not implemented operation by {by}")

    def save_operation(self, operation):
        self._repository.save(operation)
