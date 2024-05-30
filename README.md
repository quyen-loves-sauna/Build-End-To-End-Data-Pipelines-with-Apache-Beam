Welcome to the repository for building an end-to-end data pipeline tailored for an online food ordering platform. This project demonstrates the process of ingesting, processing, and reporting transactional data using Google Cloud Platform (GCP) services and the Python client library for BigQuery.

Project Overview
This repository contains the code and resources needed to set up and run a data pipeline that processes daily transactional data files from an online food ordering platform. The pipeline handles data ingestion, processing, and generation of both daily and monthly reports.

Use Case Description
An online food ordering company generates a daily batch file containing transaction data in the following format:

Customer ID: ID of the customer who placed the order.
Order Date: Date on which the order was placed.
Order Time: Time when the order was placed.
Order ID: Unique ID of the order.
Items Ordered: List of items ordered, separated by a colon.
Order Amount: Total amount of the order.
Payment Mode: Mode of payment (card, wallet, net banking, etc.).
Restaurant: Restaurant from which the order was placed.
Order Status: Status of the order (delivered, not delivered, canceled, on hold).
Rating: Customer rating out of five for the order.
Feedback: Predefined feedback provided by the customer.
The objective is to ingest this data, process it, and generate the following reports:

Daily Reports:

Percent split of payment modes.
Breakdown of ratings received by each restaurant.
Monthly Reports:

Month-wise breakdown of total ratings.
Month-wise breakdown of customer feedback.
Repository Structure
data_pipeline/: Contains the implementation of the data pipeline using the Python client library.
scripts/: Utility scripts for setting up and managing GCP resources.
docs/: Documentation and resources for understanding the data pipeline and reporting process.
samples/: Sample data files for testing and demonstration purposes.
Key Components
BigQuery
BigQuery is a fully managed data warehouse that allows fast SQL queries using the processing power of Google's infrastructure. We use it to store and analyze the transactional data.

Python Client Library
The Python client library for BigQuery allows us to interact with BigQuery, perform data operations, and generate reports programmatically.

Getting Started
Prerequisites
Google Cloud Platform account
Python 3.x
Google Cloud SDK
BigQuery API enabled on your GCP project
