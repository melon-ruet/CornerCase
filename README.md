##Lunch Menu Selector
A Django based web app with REST api. This app will help company to choose a menu from a 
restaurant each day before lunch.

### Features
* Admin can add employees and restaurant managers
* Restaurant managers can add their restaurants. One manager can add multiple restaurants
* Employees can vote only one menu each day. Also they can edit their vote.
* Can be multiple winners based on same number of vote
* A restaurant can not be winner for 3 consecutive days
* Has login and logout option

### Requirements
* Python >= 3.6
* Django (compatible versions with python)
* Django Rest Framework (DRF) 
* Docker

### Make ready virtual environment
Create virtual environment to lint, test or develop the project
Assuming these commands will run from either Linux or macOS
```shell
cd /path/to/CornerCase
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt --upgrade pip
touch lunch_selector/db.sqlite3
python lunch_selector/manage.py migrate
python lunch_selector/manage.py create_groups

```
Then all the below commands should run from project root path

### How to test
For unittest, django default test module and DRF test modules are used. To run all tests
```shell
(cd lunch_selector && python manage.py test)
```
### How to lint
Additional pylint is used to lint codes. A python file is used to check lint.
```shell
python check_lint.py
```

### How to run dev server
#### using manage.py
Make sure the virtual env is ready with database and default django groups.
Then for running dev server using manage.py
```shell
python lunch_selector/manage.py runserver
```

#### using docker
Check `.env.dev` file for docker dev environment variables    

From project root folder run this to build docker image
```shell
docker build -t lunch_selector .
```

Run this command to start dev server.
Note that we are providing superuser username and password with the command.
Without superuser username and password docker container will not run.
```shell
docker run --name lunch_app -d -p 8000:8000 -e DJANGO_SUPERUSER_USERNAME=<username> -e DJANGO_SUPERUSER_PASSWORD=<password>  --env-file .env.dev lunch_selector
```

To stop container
```shell
docker stop lunch_app
```

To rerun dev server
```shell
docker start lunch_app
```

To completely remove old server
```shell
docker stop  lunch_app
docker container rm lunch_app
```

### Swagger
Added a swagger view to check visually all endpoints and request from a 
nice UI. After running dev server the swagger view is accessble from here    
[http://127.0.0.1:8000/swagger](http://127.0.0.1:8000/swagger)

### Logging
Django logging is implemented with DEBUG to a file and INFO to console but
More logging should be added that I missed

### Authentication
Token based authentication is used in this application. The default django rest framework's `ObtainAuthToken` view is used for that.
There is no refresh token or token timeout system is added. But it can be improved. 
For requesting to endpoints requests should contain a header with token. Example header
```
Authorization: Token <token key>
```

### Using the api endpoints
* Get the token
```shell
curl -X POST "http://127.0.0.1:8000/user/token/" -H  "Content-Type: application/json" -d "{  \"username\": \"username\",  \"password\": \"password\"}"
```
or from swagger `/user/token` endpoint with username and password    
A response will be looked like this   
```json
{
  "token": "f64ed8a4263114f73b3479c6386e34466d0e5374"
}
```
* Now this token value will be used in other endpoints. For example in get restaurant list 
```shell
curl -X GET "http://127.0.0.1:8000/restaurants/" -H  "accept: application/json" -H  "Authorization: Token f64ed8a4263114f73b3479c6386e34466d0e5374"
```
* To use token in swagger simply hit the endpoint `/user/token`, get the token. 
  Then click `Authorize` button on upper right of UI. Set the `value` as
  `Token <token key>` and click `Authorize`. Then all APIs can be usable from swagger UI.
  

### Drawbacks
* No throttling is used within the entire application
* Less logging
* No refresh token, no token expiration