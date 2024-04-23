from injector import inject

from symbiot_core.connection.connectors.object_connector import ObjectConnector
from symbiot_core.control.handlers.chat_handler import ChatHandler
from symbiot_lib.objects.operation import Operation
from symbiot_lib.objects.step_record import StepRecord


class CalibrationHandler(ChatHandler):

    @inject
    def __init__(self, object_connector: ObjectConnector):
        super().__init__(object_connector)

    def create(self, wish):
        # noinspection PyTypeChecker
        operation = Operation(
            None, wish, wish,
            "", "NEW",
            "unnamed", "", [])

        step = StepRecord([], client=self.server.get_client_by_name("calibrator"))
        step.add_to_status("calibration")
        step.client.tool_kit.func = self.assign_nord_star
        operation.add_or_update_record(step)

        step.client.tool_kit.func = None
        self.server.post_pickle(operation,
                                path="operation")
        step.client.tool_kit.func = self.assign_nord_star

        self.active_step = step
        self.continue_chat(wish)
        self.close_chat()

    def open_chat(self, step_id):  # * overwrite
        super().open_chat(step_id)
        self.active_step.client.tool_kit.func = self.assign_nord_star

    def close_chat(self):  # * overwrite
        self.active_step.client.tool_kit.func = None
        super().close_chat()

    def set_body(self, new_body: str) -> None:  # * overwrite
        self.active_step.client.tool_kit.func = None
        super().set_body(new_body)
        self.active_step.client.tool_kit.func = self.assign_nord_star

    def assign_nord_star(self, nord_star, name):  # * callback method
        step = self.active_step
        step.inputs.append(name)
        step.outputs.append(nord_star)
        step.add_to_status("ns_generated")
