

together_model_name = "togethercomputer/llama-2-70b-chat"
import together
import os
from api_key import *
from pydantic import Extra, Field, root_validator
from langchain.llms.base import LLM

# hugging face pipe line처럼 together pipe line 만들기
os.environ["TOGETHER_API_KEY"] = together_api_key
class TogetherLLM(LLM):

    # set model
    model:str = together_model_name

    # set api key
    together_api_key:str = os.environ["TOGETHER_API_KEY"]

    # set temperature
    temperature:float = 0.5

    max_tokens:int = 1024


    class Config:
        extra = Extra.forbid

    # #@root_validator(skip_on_failure=True)
    #
    #
    # def validate_environment(cls,values: Dict)->Dict:

    #     # 등록한 together api를 validate한다
    #     api_key = get_from_dict_or_env(
    #         values,"together_api_key","TOGETHER_API_KEY"
    #     )
    #     values["together_api_key"] = api_key
    #     return values

    # llm type is together
    @property
    def _llm_type(self) -> str:
        """Return type of LLM."""
        return "together"

    # llm run 할때 call
    def _call(self,prompt,**kwargs) -> str:
        """Call to Together endpoint."""
        together.api_key = self.together_api_key
        output = together.Complete.create(prompt,
                                          model=self.model,
                                          max_tokens=self.max_tokens,
                                          temperature=self.temperature,
                                          )
        text = output['output']['choices'][0]['text']
        return text

# function of Together ai api model
import textwrap

B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
DEFAULT_SYSTEM_PROMPT = """\
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information."""

#라마2맞게 prompt조합

def get_prompt(instruction, new_system_prompt=DEFAULT_SYSTEM_PROMPT ):
    SYSTEM_PROMPT = B_SYS + new_system_prompt + E_SYS
    prompt_template =  B_INST + SYSTEM_PROMPT + instruction + E_INST
    return prompt_template

def cut_off_text(text, prompt):
    cutoff_phrase = prompt
    index = text.find(cutoff_phrase)
    if index != -1:
        return text[:index]
    else:
        return text

def remove_substring(string, substring):
    return string.replace(substring, "")



def parse_text(text):
        wrapped_text = textwrap.fill(text, width=100)
        print(wrapped_text +'\n\n')
        # return assistant_text


def stop_model():
    together.Models.stop(together_model_name)
    print("MODEL STOP")