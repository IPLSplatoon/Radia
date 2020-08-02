"""
This tool is used for creating the map list images for Low Ink
"""
from PIL import Image, ImageDraw, ImageFont
import boto3
import botocore.config as bcc
from boto3.s3.transfer import S3Transfer
import botocore.exceptions as be
import datetime
import os
from dotenv import load_dotenv
import uuid
from typing import Optional
import json

load_dotenv("files/.env")

# Initiate session
# Config to limit retry attempts
boto3Config = bcc.Config(connect_timeout=5, read_timeout=60, retries={'max_attempts': 1})
session = boto3.session.Session()
client = session.client('s3', region_name=os.environ.get("S3_region_name"),
                        endpoint_url=os.environ.get("endpoint_url"),
                        aws_access_key_id=os.environ.get("S3_access_key_id"),
                        aws_secret_access_key=os.environ.get("S3_secret_access_key"),
                        config=boto3Config)
transfer = S3Transfer(client)


class MapSetUpload:
    def __init__(self):
        self.aws_bucket = os.environ.get("S3_bucket")
        self.CDNLink = os.environ.get("CDNLink")

    async def uploadJSON(self, mapDict: dict) -> Optional[str]:
        fileID = str(uuid.uuid4().hex)
        with open('temp/{}.json'.format(fileID), 'w') as json_file:
            json.dump(mapDict, json_file, indent=4)
        try:
            # Upload files to S3
            client.upload_file("temp/{}.json".format(fileID),
                               self.aws_bucket,
                               "LowInk/delivery/{}.json".format(fileID),
                               ExtraArgs={'ACL': 'public-read'})
            os.remove("temp/{}.json".format(fileID))  # remove temp file
            return "{}/LowInk/delivery/{}.json".format(self.CDNLink, fileID)
        except be.ClientError:
            os.remove("temp/{}.json".format(fileID))
            return None
        except Exception:
            os.remove("temp/{}.json".format(fileID))
            return None
