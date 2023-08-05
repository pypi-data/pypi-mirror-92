# Citibox profiling
Python library to profiling inside Citibox backend team 

## How to use it?
Install via pip and initialize it as soon as possible with the following code:

````python 
from citibox.profiling import Profiling, GoogleConfig, ProfilerServiceGoogle

profiling_config = GoogleConfig(
    service_name="name_of_your_service",
    service_version="core-001",
    project_id="gcp_project_id",
    service_account_json_file="path/to/json_credentials-json",
)

profiling_service = ProfilerServiceGoogle(profiling_config)
profiling = Profiling(profiler_service=profiling_service)
profiling.start()

````

##Step-by-step guide:


1. Import library profiler, config and service implementation:

````python 
from citibox.profiling import Profiling, GoogleConfig, ProfilerServiceGoogle
````
2. Create config for your service
````python 
profiling_config = GoogleConfig(
    service_name="name_of_your_service",
    service_version="core-001",
    project_id="gcp_proyect_id",
    service_account_json_file="path/to/json_credentials-json",
)
````

3. Create the service with the previous configuration and pass it to profiling

````python 
profiling_service = ProfilerServiceGoogle(profiling_config)
profiling = Profiling(profiler_service=profiling_service)
````

4. Start collecting information

````python 
profiling.start()
````

5. Enjoy it

## How to use in django project?

Define config in settings
````python
PROFILING = {
    'ACTIVE': True,
    'SERVICE_NAME': 'app_service',
    'SERVICE_VERSION': 'core-001',
    'PROJECT_ID': 'gcp_project_id',
    'SERVICE_ACCOUNT_JSON_FILE': 'path/to/json_credentials-json',
}
````

Add middleware in config

```python
MIDDLEWARE = [
    'citibox.profiling.contrib.django.ProfilingMiddleware',
]
```
