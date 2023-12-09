import pymysql
import pymysql.cursors

#Connect to database
con = pymysql.connect(host='localhost',
        user='root',
        password='',
        db='database',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)
print(con)

def setData(fields:list,datas:list)->str:
    if len(fields)==len(datas):
        i:int=0
        s:str='`'
        for field in fields:
            s+=field+"`='"+datas[i]+"',`"
            i+=1
        return s[0:len(s)-2]
    else:
        return "The fields doesn match, please try again"
    
#Add record to database
def add_record(table:list,fields:list,datas:list)->bool:
    flag:bool=False
    if len(fields)==len(datas):
        try:
            with con.cursor() as cur:
                field:str='`,`'.join(fields)
                data:str="','".join(datas)
                sql = f"INSERT INTO `{table}` (`{field}`) VALUE ('{data}')"
                cur.execute(sql)
                con.commit()
                flag=True
        except Exception:
            print("Something went wrong adding-function")
        finally:
            cur.close()
    else:
        print("Fields doesn`t match...")
    return flag
    
def update_record(table:list,fields:list,datas:list,field:str,idno:str)->bool:
    flag:bool=False
    setrecord:str=''
    if len(fields)==len(datas):
        setrecord=setData(fields,datas)
        try:
            with con.cursor() as cur:
                sql = f"UPDATE `{table}` SET {setrecord} WHERE `{field}`='{idno}' LIMIT 1"
                cur.execute(sql)
                con.commit()
        except Exception:
            print("Something went wrong in updating-function")
            flag=False
        finally:
            cur.close()
            flag=True
    else:
        print("Fields doesn`t match...")
    return flag

def delete_record(table:list,field:str,idno:str)->bool:
    flag:bool=False
    try:
        with con.cursor() as cur:
            sql:str = f"DELETE FROM `{table}` WHERE `{field}`={idno} LIMIT 1"
            cur.execute(sql)
            con.commit() 
    except Exception:
        print("Something went wrong with deleterecord-function")
    finally:
        cur.close()
        flag =True
    return flag
    
def search_record(table:str,field:str,value:str)->bool:
    slist:list=[]
    try:
        with con.cursor() as cur:
            sql:str = f"SELECT * FROM `{table}` WHERE `{field}`='{value}'"
            cur.execute(sql)
            slist:list = cur.fetchall()
    except Exception:
        print("Something went wrong in Search-function")
    finally:
        cur.close()
    return len(slist)>0


def get_record(table:str,field:str,value:str)->list:
    slist:list=[]
    try:
        with con.cursor() as cur:
            sql:str = f"SELECT * FROM `{table}` WHERE `{field}`='{value}'"
            cur.execute(sql)
            slist:list = cur.fetchall()
    except Exception:
        print("Something went wrong in getrecord-function")
    finally:
        cur.close()
    return slist

def get_all_records(table:str)->list:
    try: 
        with con.cursor() as cur:
            sql:str = f"SELECT * FROM `{table}`"
            cur.execute(sql)
            slist:list = cur.fetchall()
    finally:
        cur.close()
    return slist

def validate_user(username:str,password:str)->bool:
    try:
        with con.cursor() as cur:
            sql = f"SELECT * FROM `user` WHERE `username`='{username}' and `password`='{password}'"
            cur.execute(sql)
            slist:list = cur.fetchall()
    finally:
        cur.close() 
    return len(slist)>0


if __name__ == "__main__":
    #studentData:list=['19925775','manos','ryan mark','course','4','defualt.jpg']
    #studentField:list=['idno','lastname', 'firstname', 'course', 'level','images']
    #search:bool=delete_record("tblstudent",'id',7)
    #print(search)
    try:
        ids:str='8'
        print("Id:",ids) 
        search_student:bool = search_record('tblstudent','id',ids)
        if search_student==False:
            print("Student doesn't exist:", search_student)
        delete_student: bool = delete_record('tblstudent','id',int(ids))
        if delete_student==False:
            print("error: deleting", delete_student)
        print("success deleting", delete_student)  
    except Exception:
        print("error: exception")
    """
    try:
        idno = "19999551"
        lastname = "nadela"
        firstname = "wilson"
        course = "bsit"
        level = "3"
        images = f"default.jpg"  # Using f-string for string formatting

        existing_student = search_record('tblstudent', 'idno', idno)
        print("Search:", existing_student)
        
        student_fields = ['idno','lastname', 'firstname', 'course', 'level','images']
        student_data = [idno, lastname, firstname, course, level, images]
        print("Student Data:", student_data)
        if existing_student:
            updated = update_record('tblstudent', student_fields, student_data, 'idno', idno)
            message = "Student Updated" if updated else "Failed to update student"
            print("Updated:", updated)
        else:
            added = add_record('tblstudent', student_fields, student_data)
            message = "New Student Added" if added else "Failed to add student"
            print("Added:", added)
       
    except Exception as e:
        print(f"Error: {str(e)}", 'error')
    """
    """
    rec=setData(['lastname','firstname'],['re','re'])
    sql = f"UPDATE `tblstudent` SET "+rec+" WHERE `idno`='idno'"
    print(sql)
    try:
        updaterecord("tblstudent",['lastname','firstname'],['yu','yu'],'idno','19925775')
        if updaterecord:
            print("Updated")
    except Exception:
        print("Something went wrong...")
    """

