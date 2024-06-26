# Guidance for livestreams with digital humans on AWS


https://github.com/aws-solutions-library-samples/guidance-for-live-streams-hosted-by-digital-humans-on-aws/blob/main/README.md
## Table of Content 

1. [Overview](#overview-required)
2. 5. [Cost](#Cost)
3. [Prerequisites](#prerequisites-required)
4. [Deployment Validation and Deployment Validation ](#Deployment-Steps-and-Deployment-Validation)
5. [Clearup the guidance ](#Clearup-the-guidance)




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

## Cost

You are responsible for the cost of the AWS services used while running this Guidance. As of June-2024, the cost for running this Guidance with the default settings in the ap-northeast-1 region is approximately $378.74 per month.

| AWS service  | Dimensions | Cost [USD] |
| ----------- | ------------ | ------------ |
| Amazon API Gateway | 1,000,000 REST API calls per month  | $ 1.0 month |
| Amazon Polly | 100,000 calls each call 100 Character per month  | $ 40.0 month |
| Amazon Lambda | 1,000,000 Lambda Call  | $ 0.2 month |
| Amazon DynamoDB | 1,000,000 Write/Read totally 1T per month  | $ 1.63 month |
| Amazon S3 | 100G per month  | $ 2.30 month |
| Amazon EC2 | g4dn.xlarge  | $ 333.61 month |


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



```json
[ 

    { 
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["PUT", "POST", "DELETE"], 
        "AllowedOrigins": ["*"],
        "ExposeHeaders": [] 
    },
    { 
        "AllowedHeaders": [], 
        "AllowedMethods": ["GET"], 
        "AllowedOrigins": ["*"],
        "ExposeHeaders": [] 
    } 
]
```


e.	Create a new distribution in Amazon CloudFront

Set original domain as the newly created Amazon S3 above and make the corresponding settings, as shown in the figure

![Alt text](https://github.com/aws-solutions-library-samples/guidance-for-live-streams-hosted-by-digital-humans-on-aws/blob/main/assets/images/Picture1.png)

Click Create distribution

And markdown as {distribution address} distribution domain name in Amazon CloudFront 
 


### CloudFormation Stack deployment

a.	Download all files from /guidance-for-live-streams-hosted-by-digital-humans-on-aws
/deployment/   and Upload all the code *.zip and *.json files to the S3 created in the above steps

b. Enter the template's Amazon S3 address of the json file
 
Enter the Amazon S3 name {bucket name} and Amazon CloudFront {delivery address}, (Note that all distribution addresses must start with ‘https’, and end with‘/’
![Alt text](https://github.com/aws-solutions-library-samples/guidance-for-live-streams-hosted-by-digital-humans-on-aws/blob/main/assets/images/Picture2.png)

c Give the stack a name, use the default values for the others settings, and click summit


Automatically execute the template to establish a digital human control serverless architecture  After successful deployment, there will be an API Gateway root address in the output. Please remember that this address is {API root address} 


### Deploy Test Static Web Page
Download all files from /guidance-for-live-streams-hosted-by-digital-humans-on-aws/frontend
User any local IDE tool(for example vscode) to Open the file /assets/frontend/out/_next/static/chunks/pages/index-f6c2c2f2684f1078.js
replace the below part "https://image_endpoint.cloudfront.net/" and https://root_path.amazonaws.com/prod/" with  {distribution address} and {API root address} 
```json
[
    {"img_end_point":"https://image_endpoint.cloudfront.net/",
    "root_path":"https://root_path.amazonaws.com/prod/"
    }
]
```
for example
```json
[
    {
    "img_end_point":"https://d2f722a22c7b5y.cloudfront.net/",
    "root_path":"https://wlj2111c051.execute-api.ap-east-1.amazonaws.com/prod/"
    }
]
```
and save the file

Upload all files and folder in assets/frontend/out/ to S3 Bucket rootpath
![Alt text](https://github.com/aws-solutions-library-samples/guidance-for-live-streams-hosted-by-digital-humans-on-aws/blob/main/assets/images/frontendfiles.png)

Now you can enter the url
```
{distribution address}/index.html
```
in browser and go to the test page

in this example,  the address is  https://d2f722a22c7b5y.cloudfront.net/index.html

### Validation with the test page

Go into test page 
```
{distribution address}/index.html
```
Create the new digital human metadata

1. Select digital human character 3D module you want to use
2. Input text in different language which you want to digital human say
3. Upload the digital human backgroud picture, have to be width 1920, height 1080, jpg or png format
4. Select the language and gender
5. Select the Virtual Camera position
6. you can use default value of VR module and Item

List the digital human metadata

   After create a metadata, you can see digital human metadata create in the page

Delete the digital human metadata

   Click delete button the metadata will disappear 

![Alt text](https://github.com/aws-solutions-library-samples/guidance-for-live-streams-hosted-by-digital-humans-on-aws/blob/main/assets/images/testpage.png)

## Clearup the guidance

in Amazon CloudFormation console, delete the stack of  you have created in the step of " CloudFormation Stack deployment"

![Alt text](https://github.com/aws-solutions-library-samples/guidance-for-live-streams-hosted-by-digital-humans-on-aws/blob/main/assets/images/deletestack.png)

delete the static page stored in the S3 bucket

![Alt text](https://github.com/aws-solutions-library-samples/guidance-for-live-streams-hosted-by-digital-humans-on-aws/blob/main/assets/images/deletetestpage.png)

