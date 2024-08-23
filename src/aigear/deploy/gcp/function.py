from google.cloud import functions_v2


def get_function_request(configuration, function_name, topic_path):
    deployment_settings = configuration.get("deployment_settings", {})
    env_vars = configuration.get("env_vars", {})
    project_id = env_vars.get("GCP_PROJECT_ID")
    
    print(f"Deployment Settings:\n{deployment_settings}")
    print(f"Env vars:\n{env_vars}")
    region = deployment_settings.get("region", "us-central1")
    parent = f"projects/{project_id}/locations/{region}"
    function_id = function_name.lower()
    bucket_name = deployment_settings.get("bucket_name")
    source_code_path = deployment_settings.get("source_code_path")
    
    project_id = 'ssc-ape-staging'
    topic = 'aigear-test'
    topic_path = f'projects/{project_id}/topics/{topic}'
    
    storage_source = functions_v2.types.StorageSource(
        bucket=bucket_name,
        object_=source_code_path
    )
    
    source = functions_v2.types.Source(
        storage_source=storage_source
    )
    
    build_config = functions_v2.types.BuildConfig(
        entry_point="main",
        runtime="python38",
        source=source
    )
    event_trigger = functions_v2.types.EventTrigger(
        event_type="google.cloud.pubsub.topic.v1.messagePublished",
        pubsub_topic=topic_path,
        retry_policy=functions_v2.types.EventTrigger.RetryPolicy.RETRY_POLICY_RETRY
    )
    service_config = functions_v2.types.ServiceConfig(
        vpc_connector=deployment_settings.get("vpc_connector"),
        service_account_email=deployment_settings.get("service_account"),
        environment_variables=env_vars,
        available_cpu=deployment_settings.get("cpu", "1"),
        min_instance_count=deployment_settings.get("min_instances", 0),
        max_instance_count=deployment_settings.get("max_instances", 2),
        max_instance_request_concurrency=deployment_settings.get("concurrency", 4),
        timeout_seconds=120
    )
    # Define the function
    function = functions_v2.types.Function(
        name=f"{parent}/functions/{function_id}",
        description="A serverless dispatcher",
        build_config=build_config,
        event_trigger=event_trigger,
        service_config=service_config
    )
    request = functions_v2.CreateFunctionRequest(
        parent=parent,
        function=function,
        function_id=function_id
    )
    return request
