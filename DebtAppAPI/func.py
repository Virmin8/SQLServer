import mysql.connector
import hashlib

mydb = mysql.connector.connect(
    host="sql.virmin8.uk",
    user="root",
    password="Firesailma2010",
    database="Services",
    port=3307
)

cursor = mydb.cursor(buffered=True)

def getNameUsers(user_id: str):
    select_query = "SELECT Name FROM users WHERE ID = %s"
    cursor.execute(select_query,(user_id,))
    result = cursor.fetchone()
    return result

def getIDUserServices(user_id: str, service_id: str):
    values = (user_id,service_id)
    select_query = "SELECT ID FROM user_services WHERE UserID = %s AND ServiceID = %s"
    cursor.execute(select_query,values)
    result = cursor.fetchone()
    return result

def getNameServices(service_id: str):
    select_query = "SELECT Name FROM services WHERE Service_ID = %s"
    cursor.execute(select_query,(service_id,))
    result = cursor.fetchone()
    return result

def deleteUserService(user_id: str):
    delete_query = "DELETE FROM user_services WHERE UserID = %s"
    cursor.execute(delete_query,(user_id,))
    mydb.commit()