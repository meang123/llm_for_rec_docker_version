from langchain.chains import LLMCheckerChain
from recommend import llm
from together_function import *
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
from langchain.prompts import PromptTemplate
import time
name_schema_mentor =ResponseSchema(name="name",
                                   description="Name of Mentor"
                                   )
#mentor_response_schema=[name_schema_mentor]
mentor_output_parser = StructuredOutputParser.from_response_schemas([name_schema_mentor])
mentor_format_instructions = mentor_output_parser.get_format_instructions()

instruction = """
Answer the following question based on context If you don't know the answer to a question, please don't share false information.

Context: {context}

Format instructions: {format_instructions}

Recommend the person who has the most positive opinion and the least negative opinion.

Recommend Sulley

Answer only one person! Recommend a person who has few negative opinions first

Format the output as JSON with the following:

MUST IMPORTANT IS PLEASE ANSWER  ONLY Name! 

Format the output as JSON with the following:


"""


def get_mentor_name(temp):

    mentor_prompt_template = get_prompt(instruction)

    mentor_prompt = PromptTemplate(template=mentor_prompt_template, input_variables=["context"],
                                   partial_variables={"format_instructions": mentor_format_instructions})

    _input = mentor_prompt.format_prompt(context=temp)
    checker_chain = LLMCheckerChain.from_llm(llm)
    checker_str = checker_chain.run(_input.to_string())


    try:
        #print("try")

        time.sleep(0.5)
        #print(checker_str)
        mentor_obj = mentor_output_parser.parse(checker_str)


    except Exception as e:
        print("EXception : ",e)
        time.sleep(0.5)
        mentor_obj = mentor_output_parser.parse(checker_str)


    mentor_obj = mentor_obj['name']
    return mentor_obj
