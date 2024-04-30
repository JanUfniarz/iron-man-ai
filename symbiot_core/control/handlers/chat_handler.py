from abc import abstractmethod, ABC

from symbiot_core.connection.connectors.object_connector import ObjectConnector
from symbiot_core.control.handler_interface import HandlerInterface
from symbiot_lib.objects.step_record import StepRecord


class ChatHandler(HandlerInterface):

    def __init__(self, object_connector: ObjectConnector):
        self.server = object_connector
        self.active_step: StepRecord | None = None

    @abstractmethod
    def create(self, *args, **kwargs):
        # ! method should send data to server
        pass

    def open_chat(self, step_id):
        self.active_step = self.server.get_record_by_id(step_id)

    def close_chat(self):
        self.server.post_pickle(self.active_step,
                                path="operation/record")
        self.active_step = None

    def set_body(self, new_body: str) -> None:
        self.active_step.body = new_body
        self.server.post_pickle(self.active_step,
                                path="operation/record")

    def continue_chat(self, prompt: str) -> str:
        step = self.active_step

        if not step:
            # TODO: implement
            raise NotImplementedError("no active step")

        step.add_entry("user", prompt)
        response: dict = step.client.chat(prompt)
        step.add_entry(response["role"], response["content"])
        return step.body
