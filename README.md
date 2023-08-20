# Cycling Training Camp Reporter

https://github.com/PhilipPaulJohnson/cycling-training-camp-reporter/assets/114535785/40f94431-4ea0-4746-ac3b-1606e36b5921

OVERVIEW: This Python app will monitor cycling team metrics as riders accomplish training routes. Rider attributes such as heart rate, watts, ect. are imported into a database for query and analysis of individual or group performance

HOW IT WORKS: Using the Strava API, the application administrator may view and select each team rider's Strava segment data then utilize the back-end connectivity of Django to post the cycling data into a PSQL database. The app is containerized with Kubernetes and hosted on Azure

WHERE IT'S GOING: Currently, individual rider authorization variables need to be declared whenver importing data for a different athlete. In a future version, each cyclist could be converted into a Python object with stored authorization data allowing the app to easily select different athlete authoriztion data for import. Additional functionality could also allow query of multiple segments for each API request

PERSONAL NOTE: This is my third portfolio project which explores using the back-end of Django to connect a database. Portfolio 2 used Flask to perform a similiar task but kept it local using Docker to containerize the server and database. For this project I pushed the app into Azure and connected to a Kubernets cluster

# TECHNOLOGIES

Python: base app

Django: framework

PostgreSQL: database system

Kubernetes: containerization

Azure: Kubernetes cluster host

# INSTALL (env & requirements)

prerequisites: Mac OS, Python, Docker, Azure CLI, Azure account, Kubectl, IDE instructions for VS Code

1. clone repository to local

2. create the main folder (cycling-training-camp-reporter *rename??? -delete:'-main') venv: 'python -m venv venv'

3. select venv interpreter

4. activate venv: '. venv/bin/activate'

5. cd into app/ folder and install requirements: 'pip install -r requirements.txt'

# INSTALL (variable names)
*examples shown -overwrite with actual values as the install proceeds
  - **resource_group_name:** *django-camp-reporter (name is self-generated)
  - **cluster_name:** *django-cr-cluster (name is self-generated)
  - **container_registry_name:** *ppjdjangocr (name is self-generated)
  - **login_server string:** *ppjdjangocr.azurecr.io
  - **Postgres_server_name:** *ppjdjangocr-server (name is self-generated)
  - **external-ip_address:** *20.121.152.43
  - **pod_name:** *cycling-training-camp-reporter-004b5cb-chzf2

# INSTALL (Azure env setup)

1. 'minikube stop' (if applicable)

2. 'az login'

3. 'az group create --name ***resource_group_name** --location eastus'

4. 'az aks create --resource-group ***resource_group_name** --name ***cluster_name** --node-count 1 --generate-ssh-keys'

5. 'az aks get-credentials --resource-group ***resource_group_name** --name ***cluster_name**' (overwrite if asked)

6. verify nodes status: 'kubectl get nodes'

7. 'az acr create --resource-group ***resource_group_name** --name ***container_registry_name** --sku Basic'

8. got to: Azure Console  / Container registries / ***container_registry_name** / copy login server string

9. open second Bash terminal and input the following:

10. verify Docker is running and login Docker CLI: 'docker login' or preffered 'docker login -u <username>'

11. 'az acr login --name ***container_registry_name**'

12. 'az aks update -n ***cluster_name** -g ***resource_group_name** --attach-acr ***container_registry_name**'

# INSTALL (local & push)

1. cd into app/ folder

2. verify Docker is running and login Docker CLI: 'docker login' or preffered 'docker login -u <username>'

3. 'docker build -t cycling-training-camp-reporter .'

4. 'az login'

5. 'az acr login --name ***container_registry_name**'

6. 'docker tag cycling-training-camp-reporter:latest ***login_server**/cycling-training-camp-reporter:v1'

7. 'docker push ***login_server**/cycling-training-camp-reporter:v1'

8. Azure Portal to find the page for the Azure container registry and confirm that the image was pushed (repository)

9. 'az postgres flexible-server create --name ***Postgres_server_name** --resource-group ***resource_group_name** --database-name camp_reporter_db --public-access all'

10. from task #9, copy the values for: "host", "password", and "username" -they will be added later to your Kubernetes deployment YAML file (step 12). Confirm that the "databaseName" is 'camp_reporter_db', and the "firewallName" contains 'AllowAll'

11. 'az aks get-credentials --resource-group ***resource_group_name** --name ***cluster_name**'

12. verify nodes status: 'kubectl get nodes'

13. update manifest (cycling-training-camp-reporter-deployment.yml) from task #8 database values copied:
  - **host:** "host"
  - **username:** "username"
  - **password:** "password"
  - **image location** (containers:image:@yml)(no quotes): **login_server**/cycling-training-camp-reporter:v1

14. In the app/ folder, create a file with the name .env

15. .env file / enter the following key=value database credentials copied from task #8 (no dashes or quotes):
  - #database settings
  - DB_NAME=camp_reporter_db
  - DB_USER=**username:**
  - DB_PASSWORD=**password:**
  - DB_HOST=**host:**
  - DB_PORT=5432

16. 'cd ..' (into cycling-training-camp-reporter folder)

17. 'kubectl apply -f cycling-training-camp-reporter-deployment.yml'

18. verify deployment status: 'kubectl get deployments'

19. copy external-ip address for cycling-training-camp-reporter-service: 'kubectl get services'

# INSTALL (migrations)

1. copy pod name: 'kubectl get pods'

2. FYI: 'kubectl exec ***pod_name** -- ls'

3. 'kubectl exec ***pod_name** -- python manage.py makemigrations'

4. 'kubectl exec ***pod_name** -- python manage.py migrate'

# INSTALL (PG Admin) 

1. PG Admin access: copy host, username, password from flex server create

# AUTHORIZATION (main_cr folder)

1. get client ID & client secret from strava.com/settings/api

2. follow instructions to obtain Strava API authorization and subsequent authorization code from: developers.strava.com/docs/getting-started/

3. insert client ID, client secret & authorization code into init_auth_strava_vars.py 

4. for initial authorization, run init_authorize.py *token will expire in 6 hours

5. for reauthorization (token expired after 6 hours), run re_authorize.py 

# RUN (main_cr / driver.py):

1. RUN and follow the prompts

1. enter Strava segment ID

3. enter search start & end date (year-mo-dy)

2. enter max number of efforts to fetch

5. enter effort number(s) seperated by a space i.e. 2 3 7

6. 'y' + enter if effort list is ready for insertion into json/database 
