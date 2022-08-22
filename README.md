# Chicago Business Intelligence

## Microservice Architecture
![image_1.jpg](images/image_1.jpg)

This purpose of this project is to build a microservice in Golang to pull in data from various endpoints, clean the data, and insert the data into a postgres database hosted on GCP with Docker containers. The project source code is pushed to GitHub, after which a trigger is set off within GCP Cloud Build and pulls in the various images and builds the environments outlined within the cloudbuild.yaml file. A different way to set up the CI/CD pipeline is to utilize GitHub Actions, which can achieve the same thing, but not specific to GCP. From there, the services are run in GCP Cloud Run, which exposes endpoints for the various services that are created ("go-microservice" and "pg-admin").

## Set Up

### Postgres Database Setup

- Create a new project on the GCP console. Make a note of the project id and project name.
![image1.PNG](images/image1.PNG)

- Within your GCP console, click "Activate Cloud Shell" located at the top right of your console.
![image_2.PNG](images/image_2.PNG)

- Once the Cloud Shell terminal is launched, type the following command to set your project: "gcloud config set project {YOUR PROJECT ID}".

- Create the database instance of postgres using the following command: “gcloud sql instances create mypostgres --database-version=POSTGRES_14 --cpu=2 -- memory=7680MB --region=us-central”

- Create sql users on the database instance using the following command: “gcloud sql users set-password postgres --instance=mypostgres --password=root”

- Create a database for our microservice using the following command: “gcloud sql databases create chicago_business_intelligence --instance=mypostgres”

- Within the GCP consold, search for SQL and check to see if the database instance is up and running
![image6.PNG](images/image6.PNG)

### CI/CD Pipeline Setup

- Create your repository on GitHub

- Within the GCP console, search for Cloud Build and enable it for your project if it isn't already.
![image2.PNG](images/image2.PNG)

- After the API in enabled, navigate to Cloud Build --> Triggers and create a new trigger.
![image3.PNG](images/image3.PNG)

- Fill in the required details for the trigger, and connect it to the GitHub repository you just created, then create the trigger. Based off of the default settings, the trigger will set off when new code is pushed to the main brance of the repository.
![image4.PNG](images/image4.PNG)

### Containers for Microservices Setup

- Enable the Cloud Run API for your project (similar to how the Cloud Build API was enabled).

- Go to the IAM & Admin --> IAM page and make sure all the required roled are enabled for the project. Make sure your cloudbuild.gserviceaccount.com principal has roles: "Cloud Build Service Account", "Cloud Run Service Agent", and "Owner".
![image5.PNG](images/image5.PNG)


<br>
<br>
<br>

Once your microservices have been built and deployed, as seen in Cloud Run, click on the generated URL to access and run the microservices.
![image7.PNG](images/image7.PNG)