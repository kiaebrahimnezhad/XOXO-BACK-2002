from fastapi import FastAPI , HTTPException , Body , Path
from pydantic import BaseModel
from typing import List
from db.database import User , SessionLocal 

app = FastAPI()

# ---------- Desc:
# UsersStatus class , created for geting users data from 
# a function with methode() = post and change users data
# in DataBase or create a new User if we don't have a inserted
# userName before
# ----------

class UsersStatus(BaseModel): #BaseModel , because it's Query Parameter
    name : str = Body(Ellipsis , title = 'Please declare your userName' , alias = 'name' , min_length = 5 , max_length = 20)  
    status : str = Body(default = 'WIN' , title = 'WIN or LOSE ???' , alias = 'userStatus') 

# -----------

@app.post(
            "/users/update_or_insert_points/" ,
            tags = ['users'] ,
            summary = "Update each users statusCount or Insert a new users" ,
            description = "Update each users statusCount or Insert a new users  in List of users that you give to API"
         )
async def updating (resultList : List[UsersStatus]):
    myDataBase = SessionLocal()
    try :
        for result in resultList :
            myUser = (myDataBase.query(User).filter(User.userName == result.name)).first()
            if myUser : # if there is user with ((result.name)):userName , EXIST !!!
                if result.status == "WIN" : 
                    myUser.victorieCount += 1  # type: ignore
                else :
                    myUser.victorieCount -= 1  # type: ignore
                myDataBase.commit()
                returningUser = myUser
            else :
                if result.status == "WIN" :
                    newUser = User(userName = result.name , victorieCount = 1)
                else :
                    newUser = User(userName = result.name)
                myDataBase.add(newUser)
                myDataBase.commit()
                returningUser = newUser
        return {
            "Message" : "Update or Insert was successfully !!!" ,
            "detail" : {
                "userName" : returningUser.userName ,
                "id" : returningUser.id ,
                "point" : returningUser.victorieCount
            }
        }
    except Exception as exception :
        raise HTTPException(status_code = 404 , detail = str(exception) + " - maybe there is no result !!!")
    finally :
        myDataBase.close()

# ---------- get top limited users

@app.get(
            "/users/top_users/{limit}" ,
            tags = ['users'] ,
            summary = 'Finding top users with custom limit of count'
        )
async def findTopUsers(
                        limit : int = Path(title = 'Please write your limitation number')
                      ):
    myDataBase = SessionLocal()
    try :
        topLimitUsers = myDataBase.query(User).order_by(User.victorieCount.desc()).limit(limit)
        topUsers = myDataBase.execute(topLimitUsers).fetchall()
        return [{"userName" : user[0].userName , "point" : user[0].victorieCount} for user in topUsers]
    except Exception as exception:
        raise HTTPException(status_code = 500, detail = str(exception))
    finally :
            myDataBase.close()

@app.get("users/{userName}" , tags = ['users'])
async def findUserPoints(id : int):
        myDataBase = SessionLocal()
        try :
            myUser = (myDataBase.query(User).filter(User.id == id)).first()
            return {
            "Message" : "your user details are !!!" ,
            "detail" : {
                "userName" : myUser.userName , # type: ignore
                "id" : myUser.id , # type: ignore
                "point" : myUser.victorieCount # type: ignore
                }
            }
        except Exception as exception:
                raise HTTPException(status_code = 500, detail = str(exception))
        finally :
            myDataBase.close()
        


    