from langchain.output_parsers import ResponseSchema
from together_function import get_prompt
from langchain.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser
from langchain.schema.output_parser import StrOutputParser
# Set 5 schema
Personality_schema = ResponseSchema(name="Personality",
                                    description="Personality is a term used to describe the unique patterns of thoughts, feelings, and behaviors that distinguish one person from another"
                                    )

Value_schema = ResponseSchema(name="Values",
                              description="Values are the guiding principles that shape our lives and influence our behavior. They are the beliefs and ideals that we hold dear, and they help us make decisions about what is important to us "
                              )

Expertise_schema = ResponseSchema(name="Expertise",
                                  description="Expertise is a term used to describe a high level of knowledge or skill in a particular field"
                                  )

Experience_schema = ResponseSchema(name="Experience",
                                   description="Experience is a term used to describe the process of gaining knowledge or skill from doing, seeing, or feeling things"
                                   )
Interests_schema = ResponseSchema(name="Interests",
                                  description="Interest is a term used to describe the feeling of wanting to give your attention to something or of wanting to be involved with and to discover more about something"
                                  )


response_schemas = [Personality_schema,
                    Value_schema,
                    Expertise_schema,
                    Experience_schema,
                    Interests_schema
                    ]

schema_output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

# instruct
instruction = """
Extract the information about Personality, Values, Expertise, Experience, and Interests from the provided text. If any information cannot be extracted, leave it blank.

Text: {text}

Format Instructions: {format_instructions}

each keys must Finish with one sentence. 1 line, 1 column.

most important thing is Follow JSON FORMAT!

Format the output as JSON with the following keys :

"""

def schema_prompt():
    schema_template = get_prompt(instruction)
    schema_format_instructions = schema_output_parser.get_format_instructions()
    schema_prompt = PromptTemplate(template=schema_template,input_variables=["text"],
                                   partial_variables={"format_instructions": schema_format_instructions})
    return schema_prompt





