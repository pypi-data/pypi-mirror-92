## Simple python api using flask and sqlalchemy
### Create/update with PUT 
Description: Saves/updates the given user's name and date of birth in the database. 
Request: PUT /hello/<username> {“dateOfBirth": "YYYY-MM-DD" }
Response: 204 No Content
 
Note:
<usemame> must contains only letters. 
YYYY-MM-DD must be a date before the today date. 

### See message with GET
Description: Returns hello birthday message for the given user 
Request: Get /hello/<username> 
Response: 200 OK 

Response Examples: 
A. If username's birthday is in N days: { "message": "Hello, <username>! Your birthday is in N day(s)" } 
B. If username's birthday is today: { "message": "Hello, <username>! Happy birthday!" } 
### APP variables
Application listens on localhost:5000 by default, but you can set environment variables
```
APP_HOST=someadress
APP_PORT=8080
```

### APP dependencies
**Application uses postgresql and need following environment values:**
```
SQLALCHEMY_DATABASE_URI="postgresql://user:somestrongpassword@localhost:5432/users"
```
