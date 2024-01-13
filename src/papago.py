import os
import sys
import ast
import urllib.request
import time
from output_scheam import schema_prompt,schema_output_parser
from together_function import TogetherLLM,together_model_name
client_id = "" # 개발자센터에서 발급받은 Client ID 값
client_secret = "" # 개발자센터에서 발급받은 Client Secret 값
url = ""

llm = TogetherLLM(

    model= together_model_name,
    temperature=0.3,
    max_tokens=1024

)

# Flag for en -> ko
def papago_api(header_splits,doc_dict,attribute_dic):
    flag =True
    for i in range(int(len(header_splits))):

        encText = urllib.parse.quote(header_splits[i].page_content)


        data = "source=ko&target=en&text=" + encText


        request = urllib.request.Request(url)
        request.add_header("X-NCP-APIGW-API-KEY-ID", client_id)
        request.add_header("X-NCP-APIGW-API-KEY", client_secret)

        response = urllib.request.urlopen(request, data=data.encode('utf-8'))
        rescode = response.getcode()



        if (rescode == 200):
            response_body = response.read()

            # mentor_markdown_doc[mentor_md_header_splits[i].metadata["Name"]]=ast.literal_eval(response_body.decode('utf-8'))["message"]["result"]["translatedText"]

            #mentor_mentee_name.append(header_splits[i].metadata["Name"])
            doc_dict[header_splits[i].metadata["Name"]] = ast.literal_eval(response_body.decode('utf-8'))["message"]["result"]["translatedText"]

            _input = schema_prompt().format_prompt(text=ast.literal_eval(response_body.decode('utf-8'))["message"]["result"]["translatedText"])

            ot = llm(_input.to_string())
            # print("DEBUG : ",ot)
            # print()


            try:
                #print("ppago try")
                attribute_dic[header_splits[i].metadata["Name"]] = schema_output_parser.parse(ot)
                flag =False

                time.sleep(0.5)

            except Exception:
                print("papago Exception")
                time.sleep(0.5)
                print("DEBUG : ",ot)

                try:
                    time.sleep(0.5)
                    attribute_dic[header_splits[i].metadata["Name"]] = schema_output_parser.parse(ot)
                except Exception:
                    print("Exception2 ")
                    time.sleep(0.5)
                    attribute_dic[header_splits[i].metadata["Name"]] = schema_output_parser.parse(ot)
                    # attribute_dic[header_splits[i].metadata["Name"]] = schema_output_parser.parse(ot)
                    # time.sleep(0.5)
                    try:
                        time.sleep(0.5)
                        attribute_dic[header_splits[i].metadata["Name"]] = schema_output_parser.parse(ot)
                    except Exception:
                        print("Exception3")

        else:
            print("Error Code:" + rescode)


def recomend_papago(obj_dic,k):

    korText = urllib.parse.quote(obj_dic[k])
    time.sleep(0.001)

    data = "source=en&target=ko&text=" + korText

    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID", client_id)
    request.add_header("X-NCP-APIGW-API-KEY", client_secret)

    response = urllib.request.urlopen(request, data=data.encode('utf-8'))
    rescode = response.getcode()

    if (rescode == 200):

        response_body = response.read()
        time.sleep(0.001)
        # 이 결과를 프론트로 보내야하는데
        return ast.literal_eval(response_body.decode('utf-8'))["message"]["result"]["translatedText"]  # ast.literal_eval(response_body.decode('utf-8'))["message"]["result"]["translatedText"]

    else:
        print("Error Code:" + rescode)



    return



def review_papago2(txt_data):

    enTxt = urllib.parse.quote(txt_data)
    data = "source=en&target=ko&text=" + enTxt

    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID", client_id)
    request.add_header("X-NCP-APIGW-API-KEY", client_secret)

    response = urllib.request.urlopen(request, data=data.encode('utf-8'))
    rescode = response.getcode()

    if (rescode == 200):

        response_body = response.read()
        time.sleep(0.001)
        # 이 결과를 프론트로 보내야하는데
        return ast.literal_eval(response_body.decode('utf-8'))["message"]["result"]["translatedText"]  # ast.literal_eval(response_body.decode('utf-8'))["message"]["result"]["translatedText"]

    else:
        print("Error Code:" + rescode)

def review_papago(txt_data):

    korText = urllib.parse.quote(txt_data)

    time.sleep(0.001)


    data = "source=ko&target=en&text=" + korText


    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID", client_id)
    request.add_header("X-NCP-APIGW-API-KEY", client_secret)

    response = urllib.request.urlopen(request, data=data.encode('utf-8'))
    rescode = response.getcode()

    if (rescode == 200):

        response_body = response.read()
        time.sleep(0.001)
        # 이 결과를 프론트로 보내야하는데
        return ast.literal_eval(response_body.decode('utf-8'))["message"]["result"]["translatedText"]  # ast.literal_eval(response_body.decode('utf-8'))["message"]["result"]["translatedText"]

    else:
        print("Error Code:" + rescode)