"""Google Cloud Storage (GCS) utilities.
"""
import os

from google.cloud import storage
from google.auth.credentials import AnonymousCredentials


def download_agent_data(bucket_name, export_file_key) -> str:
    if os.getenv("STORAGE_EMULATOR_HOST") is not None:
        # We're operating in a test context.
        storage_client = storage.Client(project="test", credentials=AnonymousCredentials())
    else:
        # In dev and prod, credentials are inferred from the environment.
        storage_client = storage.Client()

    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(export_file_key)
    filename = '/tmp/agent_data.json'
    blob.download_to_filename(filename)
    return filename
