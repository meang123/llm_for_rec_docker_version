import sys
import time
#
# # Importing module
#
from api_key import together_api_key,cohere_api_key
import os
from mentor_mentee_schema_parser import *
from recommend import *
import json
import cohere

from find_best_mentor import get_mentor_name
from find_similar_mentee import review_chain
from langchain.document_loaders import DirectoryLoader
import mysql.connector
import re
from cohere import Client
from db_to_file import *
from RCI import final_reputation

import nltk



# SET API KEY
os.environ["TOGETHER_API_KEY"] = together_api_key

os.environ["COHERE_API_KEY"] = cohere_api_key

os.environ["OPENAI_API_KEY"] = open_ai_api_key

co=Client(os.environ["COHERE_API_KEY"])


def lambda_handler(event, context):
    event = json.loads(event['body'])


    body = event['body']


    #body['flag'] == 0
    if body['flag'] == 0:
        dir_path = '/tmp/nltk_data'
        nltk.data.path=['/tmp/nltk_data']
        if not os.path.exists('/tmp'):
            os.makedirs('/tmp')


        if not os.path.exists(dir_path):
            os.makedirs(dir_path)



        nltk.download('stopwords', download_dir=dir_path)
        nltk.download('punkt', download_dir=dir_path)
        nltk.download('wordnet', download_dir=dir_path)
        nltk.data.path.append(dir_path)


        shutil.copytree('/var/task/src/data', '/tmp/data', dirs_exist_ok=True)




        print("Im flag 0 state")

        mysql_connector()
        print("mysql connetoc done")
        time.sleep(0.5)

        mydb = mysql.connector.connect(
            host="",
            user="master",
            password="finwave2023",
            database="finwaveDB"
        )

        cursor = mydb.cursor(buffered=True)

        temp_id = body['mentee_id']
        temp_id = int(temp_id)
        cursor.execute("SELECT name,mentee_id FROM mentee;")

        rows = cursor.fetchall()

        retrival_mentee_obj = ""

        for row in rows:
            if row[1] == temp_id:
                retrival_mentee_obj = row[0]




        mentor_attribute_dic = mentor_parser()


        mentee_attr_dic = mentee_parser()


        time.sleep(0.5)
        recommend_result,recommend_front_txt = recommend(mentor_attribute_dic, mentee_attr_dic,retrival_mentee_obj=retrival_mentee_obj)
        time.sleep(0.5)

        temp = ""
        for i, j in recommend_result.items():
            temp += f"{i} : {j}\n\n"

        print("recoomend done")
        # find best mentor
        time.sleep(0.5)

        try:
            best_mentor = get_mentor_name(temp)
            time.sleep(0.5)

            if best_mentor not in mentor_attribute_dic.keys():
                time.sleep(0.5)
                best_mentor = get_mentor_name(temp)
                time.sleep(0.5)

            q = ["Sulley", "Trex"]
            if best_mentor not in q:
                best_mentor = get_mentor_name(temp)
                time.sleep(0.5)

        except Exception:
            print("best mentor fail 1")
            time.sleep(1.0)
            try:

                best_mentor = get_mentor_name(temp)

            except Exception:
                print("best mentor fail 2")
                time.sleep(1.0)
                best_mentor = "Sulley"


        print("best mentor is ",best_mentor)

        # find similarity mentee
        time.sleep(0.5)

        mentor_id = find_id(best_mentor, "mentor")  # mentor id return

        time.sleep(0.5)
        update_mentee_info(mentee_attr_dic, mentor_id)
        time.sleep(0.5)


        similar_mentee = review_chain(retrival_mentee_obj=retrival_mentee_obj)
        time.sleep(0.5)
        print("similar mentee is ",similar_mentee)

        reviews=[]
        flag =False
        for name in similar_mentee:
            if name == retrival_mentee_obj:
                similar_mentee.remove(name)

            if len(similar_mentee)==0:
                print("No rivew ")
                flag=True
                break
            temp_mentee_id = find_id(name,"mentee")
            time.sleep(0.5)
            txt_data = get_review(mentor_id,temp_mentee_id)
            time.sleep(0.5)
            txt_data = review_papago(txt_data)
            time.sleep(0.5)
            reviews.append(txt_data)

        front_result = """"""
        if(flag):
            print("NO REVEIW")
        else:

            # mentor reputation

            front_result = final_reputation(similar_mentee, mentor_attribute_dic[best_mentor], mentee_attr_dic, reviews)
            time.sleep(0.5)

        # final result


        result = re.findall(r'#(.*?)\$', recommend_front_txt, re.DOTALL)


        if(flag):
            front_result = "NO REPUTATION Base on mentee"

        else:
            front_result = review_papago2(front_result)

        result_dic={
            'statusCode': 200,
            'best_mentor': json.dumps(best_mentor,ensure_ascii=False),
            'mentor_list': json.dumps(list(mentor_attribute_dic.keys()),ensure_ascii=False),
            'reson': json.dumps(result,ensure_ascii=False),
            'reputation': json.dumps(front_result,ensure_ascii=False)
        }
        print(result_dic)


        return{
            'statusCode': 200,
            'best_mentor': json.dumps(best_mentor),
            'mentor_list': json.dumps(list(mentor_attribute_dic.keys())),
            'reson': json.dumps(result),
            'reputation': json.dumps(front_result)
        }

    return {
        'statusCode': 200,
        'body': 'this is fail result'

    }



