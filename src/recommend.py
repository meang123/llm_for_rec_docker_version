from together_function import *
from rag_content import *
from operator import itemgetter
from langchain.schema.output_parser import StrOutputParser
from langchain.prompts import ChatPromptTemplate

import urllib.request

from papago import *

# set prompt
sys_prompt = """You are a helpful, mentor mentee matching recommender assistant. Always answer as helpfully as possible using the context text provided. Your answers should only answer the question once and not have any text after the answer is done.
If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information. """

instruction = """
Answer the question based on following information.

Question:/n/n {question}/n
Please provide the reasonable matching result between the mentor and mentee based on their Python dictionary attributes: Personality, Values, Expertise, Experience, and Interests

Task is Recommend system about mentor, mentee information.

Please provide a reasonable matching result between the mentor and mentee.
Not have any text after reason for the answer is done.

Question: Provide a reasonable matching result between the mentor and mentee based on their each respective attributes, given the following each information :

Mentor Personality: {mentor_p},
Mentor Values: {mentor_v},
Mentor Expertise: {mentor_e},
Mentor Experience: {mentor_ee},
Mentor Interests: {mentor_i},


Mentee Personality: {mentee_p},
Mentee Values : {mentee_v},
Mentee Expertise: {mentee_e},
Mentee Experience: {mentee_ee},
Mentee Interests: {mentee_i},

Answer Format: Reason: Positive Opinion: Negative Opinion:

Please provide the positive and negative opinions regarding the reasonable matching result of the mentor and mentee.
Please don't share false information.
and MUST IMPORTANT is answer in the following Answer Format Resone : Positive Opinion: Negative Opinion: ".
"""

#set llama2
llm = TogetherLLM(
    model= together_model_name,
    temperature=0.0,
    max_tokens=1024
)

# 우선 작동을 위해 임의의 데이터 사용하고 있다 프론트 연결을 뒤로 미루고 해결하면 여기 다시 고쳐라

def recommend(mentor_attribute_dic,mentee_attr_dic,retrival_mentee_obj="Aiden",flag=False):

    prompt_template = get_prompt(instruction, sys_prompt)
    prompt = ChatPromptTemplate.from_template(prompt_template)  # or template
    obj_dic = {}  # obj에 대한 딕셔너리 각 멘토들과 obj와의 매칭 결과가 저장 된다
    result_front_txt=""""""

    retriever = rag_advice()
    chain = {
                "question": itemgetter("question") | retriever,
                "mentor_p": itemgetter("mentor_p"),
                "mentor_v": itemgetter("mentor_v"),
                "mentor_e": itemgetter("mentor_e"),
                "mentor_ee": itemgetter("mentor_ee"),
                "mentor_i": itemgetter("mentor_i"),
                "mentee_p": itemgetter("mentee_p"),
                "mentee_v": itemgetter("mentee_v"),
                "mentee_e": itemgetter("mentee_e"),
                "mentee_ee": itemgetter("mentee_ee"),
                "mentee_i": itemgetter("mentee_i"),
            } | prompt | llm | StrOutputParser()


    for k, v in mentor_attribute_dic.items():
        time.sleep(0.001)
        for mk, mv in mentee_attr_dic.items():

            if (mk == retrival_mentee_obj):

                # 주석 처리 나중에 해야함
                # print(k, " ", mk)
                # print()

                temp_text = chain.invoke({"question": f"Is mentor and {mk} mentee matching valid? Tell me the reason, too",
                                          "mentor_p": v["Personality"],
                                          "mentor_v": v["Values"],
                                          "mentor_e": v["Expertise"],
                                          "mentor_ee": v["Experience"],
                                          "mentor_i": v["Interests"],

                                          "mentee_p": mv["Personality"],
                                          "mentee_v": mv["Values"],
                                          "mentee_e": mv["Expertise"],
                                          "mentee_ee": mv["Experience"],
                                          "mentee_i": mv["Interests"],
                                          })


                obj_dic[k] = temp_text

                result_front_txt+="#"+recomend_papago(obj_dic,k)+"$\n\n"

    #둘다 리턴 해야함
    return obj_dic,result_front_txt

