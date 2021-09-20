# Cloud-Storage-Pubsub
Developed a containerized service which publishes a data as a message to pub sub and then push the container image to GCR and deploy  service using GKE



### Test Enviornment

``` bash 


http://34.94.209.219/

```
### Before you begin
1. You're new to Google Cloud, create an account.
2. The Google Cloud Console, on the project selector page, select or create a Google Cloud project (capstone1-project).
3. Create a bucket named currency-bucket-egen.
4. Enable the Artifact Registry, Cloud Build, Cloud Function and Google Kubernetes Engine APIs.
5. Install and initialize cloud SDK

### Create a PubSub topic and Cloud function to trigger the PubSub
1. Go to the Pub/Sub topics page in the Cloud Console.
2. Click Create a topic named currency.
3. Create a subscription
4. Leave the delivery type as Pull.
5. Create a cloud function, name the cloud function as loadStorage using US-west2 region and pubsub as a trigger.
6. upload main.py and entry point as currency and then deploy it.


### Get the data from API
1. install all the files required in requirements.txt
2. GetDataToPub.py is responsible to get data from the API and publish it to the Pub and from there cloud function will sense the event and trigger the subscription. and the data will get to the bucket. 

### Push container image to GCR 

#### Before you begin:
On the cloudshell- gcloud components install kubectl
create a directory on cloud shell editor (egen-capstone)
cd into the directory you just created.

#### Routing function
app.py has a restful api which works with the http and whenever that link is hit the GetDataToPub.py is triggred and then the data is stored to the Google cloud bucket. 

#### Containerizing an app with Cloud Build
1. To containerize the sample app, create a new file named Dockerfile in the same directory as the source files.
2. Add a .dockerignore file to ensure that local files don't affect the container build process (hidden file).
3. you will get the Dockerfile from this repository.

#### Store your container in Artifact Registry 
``` bash
gcloud artifacts repositories create capstone-repo \
    --project=capstone1-project-326220 \
    --repository-format=docker \
    --location=us-west2 \
    --description="Docker repository for captone project"
```

#### Build your container image using Cloud Build
``` bash 
gcloud builds submit \
    --tag us-west2-docker.pkg.dev/capstone1-project-326220/capstone-repo/egen-capstone
```
##### Now the image is stored in Artifact Registry.

### Creating a GKE cluster
``` bash
gcloud container clusters create egen-cluster  \
    --zone us-west2
```
##### Connect to GKE cluster

#### Verify that you have access to the cluster.
``` bash
kubectl get nodes
```

### Deploying to GKE
To deploy your app to the GKE cluster you created, you need two Kubernetes objects.

A Deployment - to define your app.
A Service - to define how to access your app.

#### Deploy an app
1. Copy the deployment.yaml file in the same directory as your other files.
2. Deploy the resource to the cluster:
``` bash
kubectl apply -f deployment.yaml
```
3. Track the deployment:
``` bash 
kubectl get deployments
```

#### Deploy a Service
1. Copy the file service.yaml in the same directory as your other source files.
2. Create the Hello World Service:
``` bash 
kubectl apply -f service.yaml
```
3. Get the external IP address of the Service:
``` bash 
kubectl get services
```
4. View a deployed app: http://<external_ip>

###### If the  http://<external_ip> worked then your data is successfully sent to the pubsub and has been stored in Google cloud storage.  


