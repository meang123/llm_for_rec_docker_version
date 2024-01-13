import time

import mysql.connector
# Creating connection object
def mysql_connector():
    try:
        mydb = mysql.connector.connect(
            host="",
            user="master",
            password="finwave2023",
            database = "finwaveDB"
        )
        print(mydb)

        cursor = mydb.cursor(buffered=True)
        cursor.execute("SELECT introduce,name FROM mentor;")

        rows = cursor.fetchall()
        mentor_tmp = """"""

        for row in rows:
            mentor_tmp+=f"# {row[1]}\n\n{row[0]}\n\n"

        cursor.close()

        with open("/tmp/data/mentor_info.txt","w",encoding="utf-8") as file:
            file.write(mentor_tmp)



        cursor2 = mydb.cursor(buffered=True)
        cursor2.execute("SELECT introduce,name FROM mentee;")

        rows = cursor2.fetchall()
        mentee_tmp = """"""

        for row in rows:
            mentee_tmp+=f"# {row[1]} \n\n{row[0]}\n\n"

        cursor2.close()
        mydb.close()


        with open("/tmp/data/mentee_info.txt", "w", encoding="utf-8") as file:
            file.write(mentee_tmp)


    except mysql.connector.Error as err:
        print("MYSQL CONNECT FAILED!!")



def update_mentee_info(mentee_attribute_dic,best_mentor_id):

    try:
        mydb = mysql.connector.connect(
            host="",
            user="master",
            password="finwave2023",
            database="finwaveDB"
        )


        cursor = mydb.cursor(buffered=True)

        cursor.execute("SELECT mentee_id,mentor_id FROM review;")

        rows = cursor.fetchall()

        result_id = []
        for row in rows:
            if best_mentor_id == row[1]:
                result_id.append(int(row[0]))


        cursor.close()
        if(len(result_id)==0):
            print("no mentee review")
            return

        time.sleep(0.5)

        name_result=[]
        cursor2 = mydb.cursor(buffered=True)

        for i in result_id:
            cursor2.execute("SELECT name,mentee_id FROM mentee;")
            rows2 = cursor2.fetchall()

            #print("AAAA ",rows2)
            for row in rows2:
                if i == row[1]:
                    name_result.append(row[0])

        cursor2.close()
        mydb.close()

        temp = """"""
        for i in name_result:

            temp += "# " + i + "\n\n"
            temp += str(mentee_attribute_dic[i])
            temp += "\n\n"

        with open("/tmp/data/mentee_info.txt", "w", encoding="utf-8") as file:
            file.write(temp)


    except mysql.connector.Error as err:
        print("MYSQL updatae mentee id CONNECT FAILED!!")
        print(err)



# name -> db-> get id
def find_id(Name,target):
    try:
        mydb = mysql.connector.connect(
            host="",
            user="master",
            password="finwave2023",
            database="finwaveDB"
        )

        print(mydb)
        cursor = mydb.cursor(buffered=True)

        #cursor.execute("SELECT mentor_id,name FROM mentor;")

        cursor.execute(f"SELECT {target}_id,name FROM {target};")

        rows = cursor.fetchall()

        result =0
        for row in rows:
            #print("aaa ",row)
            if(Name==row[1]):
                result =row[0]

        cursor.close()

        mydb.close()
        return result

    except mysql.connector.Error as err:
        print("MYSQL find id CONNECT FAILED!!")
        print(err)

# retrival mentee txt upload
def get_review(mentor_id,mentee_id):
    try:
        mydb = mysql.connector.connect(
            host="",
            user="master",
            password="finwave2023",
            database="finwaveDB"
        )


        cursor = mydb.cursor(buffered=True)
        cursor.execute("SELECT content,mentor_id,mentee_id FROM review;")

        rows = cursor.fetchall()

        review_content=""
        for row in rows:
            if row[1]==mentor_id and mentee_id==row[2]:
                review_content=row[0]

        cursor.close()

        mydb.close()
        return review_content

    except mysql.connector.Error as err:
        print("MYSQL CONNECT FAILED!!")
        print(err)