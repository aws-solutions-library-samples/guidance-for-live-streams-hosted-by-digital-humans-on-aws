# Guidance for livestreams with digital humans on AWS



## Table of Content 

1. [Overview](#overview-required)
2. [Prerequisites](#prerequisites-required)
3. [Deployment Validation and Deployment Validation ](#Deployment-Steps-and-Deployment-Validation)



## Overview 

### 1. Description
This guidance helps customers to build an end-to-end virtual human live streaming solution with cloud rendering, cloud live streaming and AI components. Customers can use this guidance to meet their needs on 1) quickly building the management platform of digital human which can control digital human’s language, voice and intonation according to business scenarios; 2) pushing livestreaming video to various types of terminals based on IVS.
### 2.Customer value
Fulfill the requirement of high-quality digital human to be talking in typical scenes and a large number of C-end users can watch; 2. Using cloud rendering for digital humans and virtual scenes to reduce the pressure of client development and compatibility. 3. Using standard video streams for live streaming of digital human scenes, distributed through edge networks, with auto scaling capability . 4. Supporting real-time live streaming control. 5. Supporting live streaming on-demand to provide an end-to-end loosely coupled architecture, Convenient for customers to connect with technology 6. Customers can conduct secondary development based on the interface framework 7. The cost is relatively low and suitable for innovative projects

### 3. Architecture

![Alt text](https://github.com/aws-solutions-library-samples/guidance-for-live-streams-hosted-by-digital-humans-on-aws/blob/main/assets/images/architecture.jpg)


1.Operator uses APIs or front-end pages that encapsulate APIs to send control commands of the digital human streamer or question messages from viewers to Amazon API Gateway.

2.API Gateway passes the question messages to the LLM(Large Language Model)powered QA(Question and Answer) system, and gets suggested answer from the system. All APIs are configured with authentication. Amazon CloudWatch monitors for Lambda functions and API calls.

3.AWS Lambda uses Amazon Polly to convert  answers into a voice file, stores assets in Amazon Simple Storage Service (Amazon S3) and saves the metadata in Amazon DynamoDB.

4.The API Gateway passes the control commands of the digital human to a VR module running VR application hosted on Amazon Elastic Compute Cloud (Amazon EC2) - g4dn series are recommended. If the EC2 GPU usage is reaching threshold, Amazon EC2 Auto Scaling can launch a new instance within the Auto Scaling group.

5.The VR application runs the digital human module, renders images into video streams and pushes streams to the EC2s hosting a streaming module. . If the EC2 CPU usage is reaching threshold, Amazon EC2 Auto Scaling can launch a new instance within the Auto Scaling group.

6.Amazon Interactive Video Service (Amazon IVS low-latency) distributes the livestream to viewers’ mobile phone or web applications
IVS real-time streaming is recommended to reduce latency.


## Prerequisites 

### AMI preparation
-fpr this system's VR module part, we have prepared a default VR module with a few digital human 3D module samples, we will update the AMI name in different region in deployment guide


### AWS account requirements 

- Region ap-northeast-1
- G series EC2 instance's CPU Quota is larger than 16
- AWS Lambda, Amazon DynamoDB, Amazon APIGateway, Amazon S3, Amazon CloudFormation, Amazon CloudFront, Amazon CloudWatch.



## Deployment Steps and Deployment Validation 

### Create Amazon S3 and Amazon CloudFront and configure Amazon CloudFront to access Amazon S3
a.	Click to create a bucket in us-east-1  

b.	Name the bucket, and markdown as {bucket name}, click Create bucket

c.	Once created, set S3 cross-domain permissions and select the permission tab

d.	Edit CORS permissions as follow

[
{
“allowedHeaders”: [
“*”
],
“allowedMethods”: [
“PUT”,
“POST”,
“DELETE”
],
“allowedOrigins”: [
“*”
],
“exposeHeaders”: []
},
{
“allowedHeaders”: [
“*”
],
“allowedMethods”: [
“PUT”,
“POST”,
“DELETE”
],
“allowedOrigins”: [
“*”
],
“exposeHeaders”: []
},
{
“allowedHeaders”: [],
“allowedMethods”: [
“GET”
],
“allowedOrigins”: [
“*”
],
“exposeHeaders”: []
}
]

e.	Create a new distribution in Amazon CloudFront

set original domain as the newly created Amazon S3 above and make the corresponding settings, as shown in the figure

![Alt text](https://github.com/aws-solutions-library-samples/guidance-for-live-streams-hosted-by-digital-humans-on-aws/blob/main/assets/images/Picture1.png)

 
Click Create distribution

And markdown as {distribution address} distribution domain name in Amazon CloudFront 
 


### CloudFormation Stack deloyment

a.	Upload all the code *.zip and *.json files to the S3 created in the above steps

b. Enter the template's Amazon S3 address of the json file
 
Enter the Amazon S3 name {bucket name} and Amazon CloudFront {delivery address}, (Note that all distribution addresses must start with ‘https’, and end with‘/’
![Alt text](https://github.com/aws-solutions-library-samples/guidance-for-live-streams-hosted-by-digital-humans-on-aws/blob/main/assets/images/Picture2.png)
c Give the stack a name, use the default values for the others, and click summit


Automatically execute the template to establish a digital human control serverless architecture  After successful deployment, there will be an API Gateway root address in the output. Please remember that this address is {API root address} 




