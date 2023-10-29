from injector import inject

from symbiot_lib.objects.gpt_client import GPTClient
from symbiot_lib.objects.step_record import StepRecord
from symbiot_server.control.client_builder import ClientBuilder
from symbiot_server.control.services.symbiot_service import SymbiotService
from symbiot_server.database.repositories.gpt_client_repository import GPTClientRepository


class ClientService(SymbiotService):
    division_name = "client"

    # noinspection PyTypeChecker
    @inject
    def __init__(self,
                 client_builder: ClientBuilder,
                 client_repository: GPTClientRepository):
        super().__init__()
        self._builder: ClientBuilder = client_builder
        self._repository: GPTClientRepository = client_repository
        self._active_step: StepRecord = None

    @staticmethod
    def distribute_keys(open_ai=None):
        def check_clear(key):
            if key == "clear":
                key = None
            return key

        if open_ai is not None:
            GPTClient.set_api_key(check_clear(open_ai))

    def open_chat(self, step_id):
        step: StepRecord = self.mediator("operation").get_record(step_id)
        step.client = self._builder\
            .new("gpt", step.client)\
            .add_step(step).get()
        self._active_step = step

    def close_chat(self):
        self.mediator("operation").save_record(self._active_step)
        self._active_step = None

    def calibrate(self, step: StepRecord, wish: str):
        step.client = self._builder.new("gpt", "calibrator").get()
        step.add_to_status("calibration")
        self._active_step = step
        self.continue_chat(wish)
        self.close_chat()

    def continue_chat(self, prompt: str):
        step = self._active_step

        if not step:
            # TODO: implement
            raise NotImplementedError("no active step")
        response = step.client.chat(prompt)
        step.add_entry(prompt, response)
        return step.body

    def calibration_ended(self, nord_star: str, name: str):
        self._active_step.inputs.append(name)
        self._active_step.outputs.append(nord_star)
        self._active_step.add_to_status("done")
        self.mediator("operation").calibration_ended(self._active_step)

    def new_client(self, by: str, content) -> GPTClient:
        match by:
            case "name": return self._builder.new("gpt", content).get()
