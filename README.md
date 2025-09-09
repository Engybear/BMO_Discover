# BMO Discover
<div align = "center"> 
  
![BMO_Discover_Logo.png](Media/BMO_Discover_Logo.png)

</div>

(WORK IN PROGRESS)

<!-- TOC -->
* [BMO_Discover](#bmo-discover)
  * [Inspiration, Purpose and Goals](#inspiration-purpose-and-goals)
  * [What It Does / Overview](#what-it-does--overview)
  * [File Organization / How It's Made](#file-organization--how-its-made)
  * [Challenges Faced](#challenges-faced)
  * [Accomplishments To Be Proud Of](#accomplishments-to-be-proud-of)
  * [Next Steps](#next-steps)

## Inspiration, Purpose and Goals

- made to put sql skills into an actual process
- model batch and streamed input data and how to handle it
- integrate AI into datasets that could update in real time

An end-to-end ETL pipeline built to service mock customer insights to a dashboard and AI query bot for a bank

## What It Does / Overview

- chatbot
- dashboard
- filtering

MrGrabs is a medium-sized (16x16x20'') robot, capable of driving through doors with at lest 2' of clearance. It is built primarily out of PLA, with plexiglass and wood used to reinforce the chassis. The robot is controlled via a custom bluetooth APP on an Andriod phone, and integrated with a Microsoft Surface Pro running an application of another project to scan for, greet and wave to students on campus. It also has four HC-SR04 Ultrasonic Sensors that are unused but intended to be a safety feature to prevent collisions.

<div align="center">
  <img src="MrGrabs%20Pics/IMG_2423.JPG" style="transform: rotate(180deg); width: 450px;" />
  <img src="MrGrabs%20Pics/IMG_2418.JPG" style="transform: rotate(180deg); width: 253px;" />
</div>

### Design Breakdown

- www

Here you can see an overview of the design. The phone connects to the principal controller of the robot (Arduino Nano 33 BLE), which directly manages the motors through the IRF3205. There are also 2 agent controllers, as the Adafruit Feather 32u4 BluefruitLE, that receive simple commands from the principal controller, which are individually used to control the 2 robotic arms, made up of 7 daisy chained AX12-A servos. The Arduino Nano itself is powered by and can recieve data from a mounted laptop, if desired. Lastly, there are HC-SR04 sensors that can be controlled by the Arduino Nano as well to lock up the motors if a collision is imminent.

<div align = "center"> 
  
![BMO_Discover_FlowDiagram.png](Media/BMO_Discover_FlowDiagram.png)

</div>

- Refer to MrGrabs Pics for more images of the robot

## File Organization / How It's Made

- a lot of queries are stored on AWS (Glue, Athena, DynamoDB, Bedrock) and Apache Superset
- kafka_stream for kafka producer, the docker kafka KRaft server / data broker, and kafka consumer which sends off to DynamoDB
- inputs for the batch dataset of ~50 customer information split up between json, csv, and psql data
- processing for pulling those inputs from s3 and converting them into a single parquet for SUperset and a json for the Bedrock knowledge base
- Media for images of the dashboard and exmaples of the chatbot


Refer to User Guide for setup and usage information

Refer to Construction Guide for system design information

Refer to ArduinoCode/MainSketches for the code controlling the robot's code written in `C++`

Refer to BluetoothApp for the BLE5.aia file used to configure the andriod app remote controller created through `MIT App Inventor`

Refer to Step and Print files for CAD design and 3D printing files created in `Fusion360`

## Challenges Faced

1-week timeline
Windows 11 setup, many hours sunk resolving errors and warnings from Spark and Hadoop
Costs; utilizing AWS free tier and being careful to stay in free tier posed some limitations with what RAG-AI models I could use and databases that were available; Everything had to be text, no images or videos
Being careful I kept costs limited to $0.11 CAD total


## Accomplishments To Be Proud Of
- learning as much as I did in this time period?

## Next Steps
- consolidating the chatbot into the dashboard directly, and having it be able to pull from what's being filtered would make this pipeline significantly more applicable to real world use cases
- despite attempts to do so, chunking for the knowledge base is still not per customer and there's some overlap that can cause confusion
