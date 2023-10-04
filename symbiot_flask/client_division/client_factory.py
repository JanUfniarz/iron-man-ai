from client_division.gpt.gpt_client import GPTClient


class ClientFactory:
    def gpt(self, template: str):
        templates = dict(

            full_aware=dict(init_messages=[self._sys_prompt("""
                You are system manager of an application, 
                that makes scripts to fulfill the user requirements.
                Your goal is to talk to the user to get specific information 
                about what he need and call proper functions 
                to give him a working solution 
            """)]),

            scripter=dict(init_messages=[self._sys_prompt("""
                Your role is to create only python code!
            """)], max_tokens=4000),

            calibrator=dict(init_messages=[self._sys_prompt("""
                You are a senior developer, who has to write script 
                (or set of scripts) to automate some process.
                Your current job is to talk to the client, 
                understand his expectations and ask 
                him as many questions as you need to
                start project.   
            """)])
        )
        return GPTClient(**templates[template])

    @staticmethod
    def _sys_prompt(prompt):
        return dict(
            role="system",
            content=prompt)
