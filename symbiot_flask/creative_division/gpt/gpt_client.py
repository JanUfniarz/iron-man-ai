import openai


# noinspection PyTypeChecker
class GPTClient:
    def __init__(
            self,
            model: str = "gpt-3.5-turbo",
            functions=None,
            function_call: str = "auto",
            temperature: float = 0.1,
            n: int = 1,
            max_tokens: int = 3000,
            init_prompt: str = None):
        self.model = model
        self.functions = functions
        self.function_call = function_call
        self.temperature = temperature
        self.n = n
        self.max_tokens = max_tokens
        self.messages = [dict(
            role="system", message=init_prompt
        )] if init_prompt else []

    @staticmethod
    def set_api_key(api_key):
        openai.api_key = api_key

    def chat(self, message: str, role="system"):
        self.messages.append(dict(role=role, message=message))
        return openai.ChatCompletion(**self.__dict__.copy())
