# BMO Discover
<div align = "center"> 
  
![BMO_Discover_Logo.png](Media/BMO_Discover_Logo.png)

</div>

###### Bank of Monetary Obligations (BMO)

<!-- TOC -->
* [BMO_Discover](#bmo-discover)
  * [Inspiration, Purpose and Goals](#inspiration-purpose-and-goals)
  * [What It Does / Overview](#what-it-does--overview)
  * [File Organization / How It's Made](#file-organization--how-its-made)
  * [Challenges Faced](#challenges-faced)
  * [Accomplishments To Be Proud Of](#accomplishments-to-be-proud-of)
  * [Next Steps](#next-steps)

## Inspiration, Purpose and Goals

Modern BI analytics dashboards often come with the cost of many queries being made to cloud data warehouses. As an alternative, what if instead queries could be made only at set periods (daily, weekly, etc.) to update a broad knowledge base, for which an in-house retriveal augmented generative (RAG) AI chatbot could reference for basic user questions that don't require loading in several queries every time that user accesses the dashboard?

This is a small project that I personally created for the purpose of getting familiar with ETL pipelines and exploring the applications of AI alongside BI analytics. It's goals are to model and handle mock batch datasets as well as streamed input data and produce a practical dashboard and chatbot where information on mock customer insights are consolidated and can be referenced with ease.

## What It Does / Overview

The Apache Superset platform both consolidates and breaks down the input data into 4 major categories:
1. Customer Location and Credit Data
2. Customer Loans
3. Customer ATM Activity
4. Customer Complaints (anonymized)

For each of these, except anonymous customer complaints, the dashboard can be filtered in real time to a subset of or single customer id.

<div align="center">
  <img src="Media/Apache_Superset/image%20(1).png" style="width: 500px;" />
  <img src="Media/Apache_Superset/image%20(2).png" style="width: 500px;" /> <br \>
  <img src="Media/Apache_Superset/image%20(3).png" style="width: 500px;" />
  <img src="Media/Apache_Superset/image%20(4).png" style="width: 500px;" /> 
</div><br /><br />


Additionally, the Bedrock platform allows for a user to query specific or broad questions about chunks of user data as shown here, including but not limited to credit score distributions, types of loans owed, calculating the total of all individual loans still owed of a particular customer, and even ATM activity patterns. 

<div align="center">
  <img src="Media/AWS_Bedrock/Chatbot_Test1.png" style="width: 500px;" />
  <img src="Media/AWS_Bedrock/Chatbot_Test2.png" style="width: 500px;" />
</div>

### Design Breakdown

Here you can see an overview of the design. All inputs are randomly generated data that consist of large batch data and live streamed data. The batch data was done in python to generate unstructured csv data on ATM activity, semi-structed json data on credit information and loans, and a structured psql database containing basic customer info. The streamed data was done through a docker kafka (KRaft-managed) server that would receive randomly generated customer complaints every 5 seconds from a kafka producer, which would be read by a kafka consumer and uploaded to AWS DynamoDB in batches of at most 25. The customer data, after being uploaded to S3 for staging would be further processed, flattened and transformed into one table/parquet file by a PySpark program. Additionally, a separate PySpark program would use this combined table to create a json file of each customer's data. These two files would be uploaded back to S3, where a AWS Glue crawler can comb through the combined table and make it queryable by AWS Athena, while the combined json file would serve as a knolwedge base for the AWS Bedrock chatbot. Lastly, Apache Superset is able to connect to both AWS DynamoDB and Athena to query all of the customer data and complaints.

<div align = "center"> 
  
![BMO_Discover_FlowDiagram.png](Media/BMO_Discover_FlowDiagram.png)

</div>

## File Organization / How It's Made

It should be noted that about 50% of the project's setup is on AWS (Glue, Athena, DynamoDB, Bedrock) and Apache Superset configurations along with cloud SQL queries which are not stored in this repository. All of the local processing done in python however is archived here.

Refer to Inputs for the batch dataset of ~50 mock customers' information split up between json, csv, and psql data

Refer to Kafka_Stream for kafka producer, the docker kafka KRaft server / data broker, and kafka consumer which transmits the live stream of data to DynamoDB

Refer to Processing for pulling the batch inputs from S3 staging and converting them into a single parquet for Superset and a json for the Bedrock knowledge base

Refer to Media for images of the dashboard and exmaples of the chatbot

## Challenges Faced

Initially I was very concerned about the costs of cloud computing and how having to stick to AWS free tier would limit the project. This did pose some limitations with what RAG-AI models I could use and the AWS database hosts available such as having to use AWS Athena over Redshift. Also due to storage constraints, I had to ensure all my inputs were text, especially the streamed data; no images or videos. However, thanks to my vigilence while learning and experimenting with the free tier limits, I kept my costs limited to $0.11 CAD total, which were taken out of my starting $200 worth of free tier credits.

Also when starting this project, I had given myself a 1-week timeline, as part of my reason for undertaking it was to practice my SQL fundamentals in preparation for an interview. Although I enjoyed the crunch and finished the project to an acceptable level, I couldn't spend as much time refining charts, generating more interesting and diversified data to work with, or configuring a more advanced AI chatbot.

More impcatfully, a lot of this project's dependencies were designed with Linux in mind and not Windows 11. This lead to several hours of development time spent on resolving errors and warnings from Hadoop and Superset that blocked portions of my ETL pipeline.

## Accomplishments To Be Proud Of

Despite previous experience working with databases for AI purposes, this would be my first time actually working with SQL, along with AWS and a lot of parts like PySpark and Superset. Doing and learning as much as I did within the 1 week timeline is something I'm proud of and notably my interviewers felt the same.

I would also like to emphasize the end-to-end nature of this project and its scalability. Although I'm working with a relatively small batch of data for the sake of a mock test, in a real use case the amount of input and processing that runs through Spark and AWS is capable of handling much, much larger data loads. I would argue, after consulting with a more senior expert in SQL and AWS for any cost optimizations that could be made, that this project could scale up to the throughput capacity needed for a bank to yield customer insights.

## Next Steps
1. Consolidating the chatbot into the dashboard directly, and having it's knowledge base adjust dynamically to be able to pull from what's being filtered on-screen would make this pipeline significantly more pragmatic for real-world use cases
2. Despite attempts to do so within the project's 1 week timeline, chunking the json data for the knowledge base is still not per customer and there's some overlap that can cause confusion if a customer name is not given within the prompt.
3. 
