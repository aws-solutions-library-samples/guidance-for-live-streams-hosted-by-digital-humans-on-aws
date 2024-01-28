## Overview (required)

1. Description
   
This guidance helps customers to build an end-to-end virtual human live streaming solution with cloud rendering, cloud live streaming and AI components. Customers can use this guidance to meet their needs on 1) quickly building the management platform of digital human which can control digital human’s language, voice and intonation according to business scenarios; 2) pushing livestreaming video to various types of terminals based on IVS.

2.Customer value
1.fulfill the requirement of high-quality digital human to be talking in typical scenes and a large number of C-end users can watch; 2. Using cloud rendering for digital humans and virtual scenes to reduce the pressure of client development and compatibility. 3. Using standard video streams for live streaming of digital human scenes, distributed through edge networks, with auto scaling capability . 4. Supporting real-time live streaming control. 5. Supporting live streaming on-demand to provide an end-to-end loosely coupled architecture, Convenient for customers to connect with technology 6. Customers can conduct secondary development based on the interface framework 7. The cost is relatively low and suitable for innovative projects


3. Architecture

   ![Alt text](https://github.com/aws-solutions-library-samples/guidance-for-live-streams-hosted-by-digital-humans-on-aws/blob/main/assets/images/architecture.jpg)
   
1.Operator use APIs or front-end pages that encapsulate APIs to send stream setting command and digital human control command or  Question message to Amazon API Gateway

Amazon API Gateway passes the input query to the GenAI QA component .The Lambda function inputs the prompt which combines the query to the large language model (LLM) hosted as a  SageMaker endpoint  and returns the suggested answer
Amazon Lambda function  use Amazon Polly to convert  answer into voice file, store assets in Amazon Simple Storage Service (Amazon S3) and save metadata in Amazon DynamoDB


The VR module hosted by Amazon Elastic Compute Cloud (Amazon g4dn series EC2 recommended) obtains digital human control command through Amazon API Gateway

The VR modul hosted by Amazon EC2 runs the virtual reality program, rendering images into video streams and pushes streams to Amazon EC2 hosting the Streaming Module

Digital human live streams are distributed to end-users in various clients  such as Mobile or PC  (clients prefer to have Amazon IVS SDK)by using Amazon IVS (and IVS Real-Time Streaming feature is recommended) .![image](https://github.com/aws-solutions-library-samples/guidance-for-live-streams-hosted-by-digital-humans-on-aws/assets/27773057/f6c51487-f665-444e-8c1d-62bcb0d6c642)
