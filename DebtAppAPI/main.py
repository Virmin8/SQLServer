
from func import getNameUsers, getNameServices, getIDUserServices, mydb, cursor, mysql, deleteUserService
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status

app = FastAPI()

class DBServices(BaseModel):
    name: str
    monthly: int
    day: int
    month: int
    year: int
    cost: float
    currency: str

class DBUsers(BaseModel):
    name: str
    admin: int


@app.get("/services", status_code=status.HTTP_302_FOUND)
def select_services():
    select_query = "SELECT * FROM services"
    cursor.execute(select_query)
    results = cursor.fetchall()
    return results

@app.get("/services/{service_id}", status_code=status.HTTP_200_OK)
def get_service_by_id(service_id: str):
    if(service_id.isdigit()):
        select_query = "SELECT * FROM services WHERE Service_ID = %s"
    else:
        select_query = "SELECT * FROM services WHERE Name = %s"
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
def delete_service(service_id: str):
    if(service_id.isdigit()):
        delete_query = "DELETE FROM services WHERE Service_ID = %s"
    else:
        delete_query = "DELETE FROM services WHERE Name = %s"
    cursor.execute(delete_query, (service_id,))
    mydb.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Service not found")
    return {"message": "Service deleted successfully"}

@app.put("/services/{service_id}", status_code=status.HTTP_200_OK)
def update_service(service_id: str, user: DBServices):
    if(service_id.isdigit()):
        update_query = """
        UPDATE services
        SET Name = %s, Monthly = %s, Day = %s, Month = %s, Year = %s, Cost = %s, Currency = %s
        WHERE Service_id = %s
        """
    else:
        update_query = """
        UPDATE services
        SET Name = %s, Monthly = %s, Day = %s, Month = %s, Year = %s, Cost = %s, Currency = %s
        WHERE Name = %s
        """
    values = (user.name, user.monthly, user.day, user.month, user.year, user.cost, user.currency, service_id)

    cursor.execute(update_query, values)
    mydb.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Service not found")
    return {"message": "Service updated successfully"}

@app.get("/users/", status_code=status.HTTP_200_OK)
def get_users():
    select_query = "SELECT * FROM users"
    cursor.execute(select_query)
    result = cursor.fetchall()
    return result

@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
def get_user_name(user_id: str):
    if(user_id.isdigit()):
        select_query = "SELECT Name FROM users WHERE ID = %s"
    else:
        select_query = "SELECT Name FROM users WHERE Name = %s"
    cursor.execute(select_query,(user_id,))
    result = cursor.fetchone()

    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
@app.post("/users", status_code=status.HTTP_201_CREATED)
def insert_user(user: DBUsers):

    insert_query = """
    INSERT INTO users (Name,Admin) 
    VALUES (%s, %s)
    """
    values = (user.name, user.admin)

    try:
        cursor.execute(insert_query, values)
        mydb.commit()
    except mysql.connector.Error as err:
        raise HTTPException(status_code=400, detail=f"Error: {err}")

    return {"message": "User inserted successfully"}

@app.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: str):
    if (user_id.isdigit()):
        delete_query = "DELETE FROM users WHERE ID = %s"
    else:
        delete_query = "DELETE FROM users WHERE Name = %s"
        select_query = "SELECT ID FROM users WHERE Name = %s"
        cursor.execute(select_query,(user_id,))
        result = cursor.fetchone()
        user_id = result[0]
    cursor.execute(delete_query, (user_id,))
    mydb.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    deleteUserService(user_id)

    return {"message": "User deleted successfully"}

@app.get("/userservices/{user_id}", status_code=status.HTTP_200_OK)
def get_user_service(user_id: str):
    select_query = "SELECT services.Service_ID,services.Name,services.Monthly,services.Day,services.Month,services.Year,services.Cost,services.Currency FROM user_services JOIN users ON user_services.UserID = users.ID JOIN services ON user_services.ServiceID = services.Service_ID WHERE UserID = %s"
    cursor.execute(select_query,(user_id,))
    result = cursor.fetchall()
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="User Services not found")
    
@app.post("/userservices/{user_id}/{service_id}", status_code=status.HTTP_201_CREATED)
def add_user_service(user_id: str, service_id: str):
    values = (user_id, service_id)
    result = getNameUsers(user_id)
    
    if (result != None):
        result = getNameServices(service_id)

        if (result != None):
            result = getIDUserServices(user_id,service_id)

            if(result == None):
                insert_query = "INSERT INTO user_services (UserID,ServiceID) VALUES (%s,%s)"
                try:
                    cursor.execute(insert_query, values)
                    mydb.commit()
                except mysql.connector.Error as err:
                    raise HTTPException(status_code=400, detail=f"Error: {err}")

                return {"message": "User Service inserted successfully"}
            else:
                return {"message": "User Service already exists"}
        else:
            return {"message": "User Service not found"}
    else:
        return{"message": "User not found"}
    