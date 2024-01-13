
from together_function import get_prompt
from recommend import llm
from langchain.prompts import ChatPromptTemplate
from operator import itemgetter
from langchain.schema.output_parser import StrOutputParser


sys_prompt1 = """You are a helpful assistant. Always answer as helpfully as possible using the context text provided. Your answers should only answer the question once and not have any text after the answer is done.
If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
"""

instruction1 = """
Please analyze the reputation of a person based on the provided information. This is {reviews} written by other people as well as details about the person's {Personality}, {Values}, {Expertise}, {Experience}, and {Interests}. \n\n
ANSWER : Provide an objective assessment of the person's reputation, taking into account both positive and negative aspects.
There should be enough output to explain to others that this person is this kind of person\n\n
"""
chain1_prompt_template = get_prompt(instruction1, sys_prompt1)

chain1_prompt = ChatPromptTemplate.from_template(chain1_prompt_template)


chain1 = chain1_prompt | llm | StrOutputParser()


#critic part
sys_prompt2 = """
You are a helpful assistant that looks at answers and finds what is wrong with them based on the original question given.
"""

instruction2="""
Please review the previous answer you provided for the following context about the person who wants to know the reputation and identify any potential errors or issues:
Context:
{context}
Initial Answer:
{initial_answer}
Take a careful look at your initial answer and evaluate its accuracy, clarity, and completeness. Consider whether there are any relevant details or important points that may have been missed or incorrectly stated."""

chain2_prompt_template = get_prompt(instruction2, sys_prompt2)
chain2_prompt = ChatPromptTemplate.from_template(chain2_prompt_template)


# improve part
sys_prompt3="""
You are a helpful assistant that reviews answers and critiques based on the original question given and write a new improved final answer.
"""

instruction3="""
Please provide a revised answer to the following context about the person who wants to know the reputation , taking into account the constructive criticism provided:
Context:
{context}


Answer Given:
{initial_answer}

Constructive Criticism:
{constructive_criticism}

Based on the problems you found, improve your answer.
Final Answer: "
"""

chain3_prompt_template = get_prompt(instruction3, sys_prompt3)
chain3_prompt = ChatPromptTemplate.from_template(chain3_prompt_template)



#Combine RCI CHain


critque_chain = {"context": itemgetter("context"),
                 "reviews":itemgetter("reviews"),
                 "Personality":itemgetter("Personality"),
                 "Values":itemgetter("Values"),
                 "Expertise":itemgetter("Expertise"),
                 "Experience":itemgetter("Experience"),
                 "Interests":itemgetter("Interests"),
                 "initial_answer": chain1 } | chain2_prompt | llm | StrOutputParser()

chain3 = {"context": itemgetter("context"),
          "reviews":itemgetter("reviews"),
          "Personality":itemgetter("Personality"),
          "Values":itemgetter("Values"),
          "Expertise":itemgetter("Expertise"),
          "Experience":itemgetter("Experience"),
          "Interests":itemgetter("Interests"),
          "initial_answer": chain1,
          "constructive_criticism": critque_chain} | chain3_prompt | llm | StrOutputParser()


def final_reputation(similar_mentee,best_mentor_attribute,mentee_attr_dic,review_list):

    final_reputation=""""""

    for idx,mentee_member in enumerate(similar_mentee):
        review_ = review_list[idx]
        temp_mentee = mentee_attr_dic[mentee_member]
        final_reputation += chain3.invoke({"context":best_mentor_attribute,
                                           "reviews":review_,
                                           "Personality":temp_mentee["Personality"],
                                           "Values":temp_mentee["Values"],
                                           "Expertise":temp_mentee["Expertise"],
                                           "Experience":temp_mentee["Experience"],
                                           "Interests":temp_mentee["Interests"]})

        final_reputation+="\n\n"

    return final_reputation