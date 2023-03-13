# online shop

## installation
### basic
1. install postgres and rabbitmq and redis and add their information to ".env" and "setting.py" file.
2. run commands which mentioned below:
    1. ` python manage.py makemigrations ` 
    2. ` python manage.py migrate `
    3. ` python manage.py runserver `


### docker
dockerfile and docker-compose file are added to project before, if docker was installed in your pc run this command: 
- ` docker-compose up ` 
- based on docker information change enviroment variable in source code(the .env file)