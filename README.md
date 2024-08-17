# Big Data Processing with Google Cloud Functions and Terraform

This project demonstrates how to upload a dataset and Python scripts to Google Cloud Storage (GCS), and deploy Cloud Functions using Terraform to process data in parallel. The dataset contains tweets, and the Python scripts analyze this data to extract various insights such as most influential users, most used emojis, and the days with the most tweets.

## Project Structure
```
/terraform
├── main.tf
├── variables.tf
└── outputs.tf
/data
└── tweets.json.zip
/src
├── q1_memory.py
├── q1_time.py
├── q2_memory.py
├── q2_time.py
├── q3_memory.py
└── q3_time.py
```

- **terraform/**: Contains Terraform scripts that define infrastructure on Google Cloud (GCS bucket, Cloud Functions).
- **data/**: Contains the zipped dataset `tweets.json.zip`.
- **src/**: Contains the Python scripts that perform data processing on the tweets dataset.

## Cloud Functions Overview

Each Python script in the `src` folder corresponds to a Cloud Function. These functions are automatically deployed via Terraform. They process the dataset located in the GCS bucket and return insights based on the specific analysis (e.g., top emojis, top users, etc.).

- **q1_memory.py / q1_time.py**: Analyze the top 10 dates with the most tweets, identifying the user with the most tweets per day.
- **q2_memory.py / q2_time.py**: Analyze the top 10 most used emojis in the tweets.
- **q3_memory.py / q3_time.py**: Identify the top 10 most influential users based on the number of mentions they received.

## Setup

1. **Install Terraform**: Make sure Terraform is installed. You can download it from [here](https://www.terraform.io/downloads.html).

2. **Initialize Terraform**:
    ```bash
    terraform init
    ```

3. **Apply Terraform configuration**: 
    This will create the necessary GCS bucket, upload the dataset and scripts, and deploy the Cloud Functions.
    ```bash
    terraform apply
    ```

4. **Output**: 
   After deployment, Terraform will output the URLs of the deployed Cloud Functions. You can use these URLs to trigger the functions.

## Usage

Once the Cloud Functions are deployed, you can invoke each function via HTTP. The functions will process the dataset located in GCS and return results based on their respective logic.

### Example Request

To invoke a Cloud Function (replace `<URL>` with the Cloud Function URL output from Terraform):

```bash
curl -X GET <URL>
```

This will trigger the corresponding function and return the analysis results in the response.

Requirements
Google Cloud Account: You'll need access to a Google Cloud project with billing enabled.
Terraform: Terraform CLI should be installed locally to manage the infrastructure.
Python 3.x: All functions are written in Python 3.x, and Cloud Functions are deployed with Python 3.9 runtime.
Notes
Ensure that the Google Cloud Service Account used for deploying Cloud Functions has the correct permissions to read from the GCS bucket.
You can modify the chunk size in the memory-optimized scripts to balance between performance and memory usage.