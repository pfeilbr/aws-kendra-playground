import os
import sys
import boto3
from botocore.exceptions import ClientError
import pprint
import time
from dotenv import load_dotenv
load_dotenv()

accountId = os.getenv("ACCOUNT_ID")
index_role_arn = os.getenv("INDEX_ROLE_ARN")
data_source_role_arn = os.getenv("DATA_SOURCE_ROLE_ARN")
bucket_name = os.getenv("BUCKET_NAME")

kendra = boto3.client("kendra")

print("Create an index")

description = "Getting started index"
index_name = "python-getting-started-index"

try:

    # check if index exists
    list_indices_response = kendra.list_indices()
    if ("IndexConfigurationSummaryItems" in list_indices_response) and (len(list_indices_response["IndexConfigurationSummaryItems"]) > 0):
        index_response = list_indices_response["IndexConfigurationSummaryItems"][0]
    else:
        index_response = kendra.create_index(
            Description=description,
            Name=index_name,
            RoleArn=index_role_arn
        )

    pprint.pprint(index_response)

    index_id = index_response["Id"]

    print("Wait for Kendra to create the index.")

    while True:
        # Get index description
        index_description = kendra.describe_index(
            Id=index_id
        )
        # When status is not CREATING quit.
        status = index_description["Status"]
        print("    Creating index. Status: "+status)
        time.sleep(5)
        if status != "CREATING":
            break

    print("Create an S3 data source")

    data_source_name = "python-getting-started-data-source"
    data_source_description = "Getting started data source."
    s3_bucket_name = f"{bucket_name}"
    data_source_type = "S3"

    configuration = {"S3Configuration":
                     {
                         "BucketName": s3_bucket_name
                     }
                     }

    # check if data source exists
    list_data_sources_response = kendra.list_data_sources(IndexId=index_id)
    if ("SummaryItems" in list_data_sources_response) and (len(list_data_sources_response["SummaryItems"]) > 0):
        data_source_response = list_data_sources_response["SummaryItems"][0]
    else:
        data_source_response = kendra.create_data_source(
            Configuration=configuration,
            Name=data_source_name,
            Description=description,
            RoleArn=data_source_role_arn,
            Type=data_source_type,

            IndexId=index_id
        )

    pprint.pprint(data_source_response)

    data_source_id = data_source_response["Id"]

    print("Wait for Kendra to create the data source.")

    while True:
        data_source_description = kendra.describe_data_source(
            Id=data_source_id,
            IndexId=index_id
        )
        # When status is not CREATING quit.
        status = data_source_description["Status"]
        print("    Creating data source. Status: "+status)
        time.sleep(5)
        if status != "CREATING":
            break

    print("Synchronize the data source.")

    sync_response = kendra.start_data_source_sync_job(
        Id=data_source_id,
        IndexId=index_id
    )

    pprint.pprint(sync_response)

    print("Wait for the data source to sync with the index.")

    while True:

        jobs = kendra.list_data_source_sync_jobs(
            Id=data_source_id,
            IndexId=index_id
        )

        # There should be exactly one job item in response
        status = jobs["History"][0]["Status"]

        print("    Syncing data source. Status: "+status)
        if status != "SYNCING":
            break
        time.sleep(60)

except ClientError as e:
    print("%s" % e)

print("Program ends.")
