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