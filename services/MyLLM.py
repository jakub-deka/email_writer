from haystack.components.generators.chat import OpenAIChatGenerator
from haystack.utils import Secret
from haystack.dataclasses import ChatMessage
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, meta


class MyTemplater:
    def __init__(self, dir: str):
        self.env = Environment(loader=FileSystemLoader(dir))

    def _get_template(self, template_name: str):
        return self.env.get_template(template_name)

    def list_template_variables(self, template_name: str):
        template_source = self.env.loader.get_source(self.env, template_name)
        parsed_content = self.env.parse(template_source)
        return meta.find_undeclared_variables(parsed_content)

    def generate(self, template_name: str, **kwargs):
        provided_params = kwargs.keys()
        required_params = self.list_template_variables(template_name)
        if not set(required_params).issubset(set(provided_params)):
            raise Exception(
                f"You must provide {required_params} to render this template"
            )

        prompt = self._get_template(template_name).render(**kwargs)
        return prompt


class MyLLM:
    def __init__(self, system_prompt: str):
        self.messages = [ChatMessage.from_system(system_prompt)]
        self.generator = OpenAIChatGenerator(
            model="meta-llama/llama-3.1-8b-instruct:free",
            api_base_url="https://openrouter.ai/api/v1",
            api_key=Secret.from_env_var("OPENROUTER_API_KEY"),
        )

    def generate(self, prompt, keep_history: bool = True):
        self.messages.append(ChatMessage.from_user(prompt))
        response = self.generator.run(self.messages)
        self.messages.append(response["replies"][0])

        if not keep_history:
            self.messages = [self.messages[0]]

        return response["replies"][0].content

    def print_messages(self):
        for m in self.messages:
            print(f"{m.role}\n{m.content}")

    def print_last_message(self):
        m = self.messages[-1]
        print(f"{m.role}\n{m.content}")
