# multitenancy-four-levels
Multitenant apps allow us to serve multiple host/users/instance/organisations with one install of the application. 

The various approached to multi tenancy
  1. Shared database with shared schema
  2. Shared database with isolated schema
  3. Isolated database with a shared app server
  4. Completely isolated tenants using Docker
  
This app would take the default django pools and use the four level multitenancy


__installation__
   
`activate virtualenv`
`pip install -r requirement.txt`
`python3 manage.py makemigrations`
`python3 manage.py migrate`
`python3 manage.py runserver`
