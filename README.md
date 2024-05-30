This repository contains code and resources for setting up and running data pipelines on GCP. The project is divided into two main parts:

Batch Processing Pipeline: We start with building a batch pipeline using Apache Beam, running on GCP. This pipeline reads data from static files, processes it, and outputs the results to a desired storage solution.
Streaming Processing Pipeline: Next, we transition to a streaming data pipeline, capable of handling real-time data ingestion and processing. This pipeline demonstrates how to use GCP services like Google Cloud Pub/Sub for real-time messaging and Apache Beam for continuous data processing.
Repository Structure
batch_pipeline/: Contains the implementation of the batch processing pipeline using Apache Beam.
streaming_pipeline/: Contains the implementation of the streaming processing pipeline using Apache Beam and GCP Pub/Sub.
docs/: Additional documentation and resources, including the differences between batch and stream processing.
scripts/: Utility scripts for setting up and managing GCP resources.
Key Concepts
Batch Processing
Batch processing involves processing large volumes of data at scheduled intervals. This type of processing is suitable for scenarios where immediate data processing is not required.

Stream Processing
Stream processing involves continuous ingestion and processing of data in real-time. This approach is essential for applications requiring instant data insights and real-time analytics.

Apache Beam
Apache Beam is a unified model for defining both batch and streaming data processing pipelines. It provides a flexible framework for building complex data workflows and can run on various execution engines.

Google Cloud Pub/Sub
Google Cloud Pub/Sub is a messaging service for exchanging data among applications. It supports real-time messaging and is essential for stream processing architectures.

Getting Started
Prerequisites
Google Cloud Platform account
Apache Beam SDK
Python (for Beam pipelines)
Google Cloud SDK
