'''
Created on 13 Jan 2021

@author: jacklok
'''
from google.cloud import tasks_v2
from trexlib import conf as lib_conf
import logging, json
from datetime import datetime, timedelta
from google.protobuf import timestamp_pb2

logger = logging.getLogger('debug')


def create_task(task_url, queue_name, payload=None, in_seconds=None, http_method='get'): 
    client = tasks_v2.CloudTasksClient()
        
    parent = client.queue_path(lib_conf.TASK_GCLOUD_PROJECT_ID, lib_conf.TASK_GCLOUD_LOCATION, queue_name)
    
    logger.debug(">>>>>>>>>>>>>>>>create_task: task_url=%s", task_url)
    
    task = {
        "http_request": {  # Specify the type of request.
                         "http_method"  : tasks_v2.HttpMethod.POST if http_method=='post' else tasks_v2.HttpMethod.GET,
                         "url"          : task_url,  
                         "oidc_token"   : {"service_account_email": lib_conf.TASK_SERVICE_ACCOUNT_EMAIL},
                        }
        }
    
    if payload is not None:
        if isinstance(payload, dict):
            # Convert dict to JSON string
            payload = json.dumps(payload)
            # specify http content-type to application/json
            task["http_request"]["headers"] = {"Content-type": "application/json"}
    
        # The API expects a payload of type bytes.
        converted_payload = payload.encode()
        
        logger.debug('create_task: converted_payload=%s', converted_payload)
    
        # Add the payload to the request.
        task["http_request"]["body"] = converted_payload
        
    if in_seconds is not None:
        # Convert "seconds from now" into an rfc3339 datetime string.
        d = datetime.utcnow() + timedelta(seconds=in_seconds)
    
        # Create Timestamp protobuf.
        timestamp = timestamp_pb2.Timestamp()
        timestamp.FromDatetime(d)
    
        # Add the timestamp to the tasks.
        task["schedule_time"] = timestamp    
    
    response = client.create_task(request={"parent": parent, "task": task})
    
    return response
