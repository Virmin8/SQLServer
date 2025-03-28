from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import mysql.connector
import hashlib

# Connect to the database
mydb = mysql.connector.connect(
    host="sql.virmin8.uk",
    user="root",
    password="Firesailma2010",
    database="Services"
)

# Create a cursor object
cursor = mydb.cursor()

app = FastAPI()

class DBServices(BaseModel):
    name: str
    monthly: int
    day: int
    month: int
    year: int
    cost: float
    currency: str

@app.get("/services", status_code=status.HTTP_302_FOUND)
def select_services():
    select_query = "SELECT * FROM services"
    cursor.execute(select_query)
    results = cursor.fetchall()
    return results

@app.get("/services/{service_id}", status_code=status.HTTP_200_OK)
def get_service_by_id(service_id: int):
    select_query = "SELECT * FROM services WHERE Service_ID = %s"
    cursor.execute(select_query, (service_id,))
    result = cursor.fetchone()
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Service not found")
    
@app.post("/services", status_code=status.HTTP_201_CREATED)
def insert_service(user: DBServices):

    insert_query = """
    INSERT INTO services (Name,Monthly,Day,Month,Year,Cost,Currency) 
    VALUES (%s, %s, %s,%s, %s, %s, %s)
    """
    values = (user.name, user.monthly, user.day, user.month, user.year, user.cost, user.currency)

    try:
        cursor.execute(insert_query, values)
        mydb.commit()
    except mysql.connector.Error as err:
        raise HTTPException(status_code=400, detail=f"Error: {err}")

    return {"message": "Service inserted successfully"}

@app.delete("/services/{service_id}", status_code=status.HTTP_200_OK)
def delete_service(service_id: int):
    delete_query = "DELETE FROM services WHERE Service_ID = %s"
    cursor.execute(delete_query, (service_id,))
    mydb.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Service deleted successfully"}

@app.put("/services/{service_id}", status_code=status.HTTP_200_OK)
def update_service(service_id: int, user: DBServices):

    update_query = """
    UPDATE services
    SET Name = %s, Monthly = %s, Day = %s, Month = %s, Year = %s, Cost = %s, Currency = %s
    WHERE Service_id = %s
    """
    values = (user.name, user.monthly, user.day, user.month, user.year, user.cost, user.currency, service_id)

    cursor.execute(update_query, values)
    mydb.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User updated successfully"}

@app.get("/users/", status_code=status.HTTP_200_OK)
def get_users():
    select_query = "SELECT * FROM users"
    cursor.execute(select_query)
    result = cursor.fetchall()
    return result

@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
def get_user_name(user_id: int):
    select_query = "SELECT Name FROM users WHERE ID = %s"
    cursor.execute(select_query,(user_id,))
    result = cursor.fetchone()
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.get("/users/admin/{user_name}", status_code=status.HTTP_200_OK)
def get_user_admin_status(user_name: str):
    select_query = "SELECT Admin FROM users WHERE Name = %s"
    cursor.execute(select_query, (user_name,))
    result = cursor.fetchone()
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.get("/users/id/{user_name}", status_code=status.HTTP_200_OK)
def get_user_id(user_name: str):
    select_query = "SELECT ID FROM users WHERE Name = %s"
    cursor.execute(select_query, (user_name,))
    result = cursor.fetchone()
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.get("/users/list/", status_code=status.HTTP_200_OK)
def get_user_list():
    select_query = "SELECT ID,Name FROM users"
    cursor.execute(select_query)
    result = cursor.fetchall()
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
