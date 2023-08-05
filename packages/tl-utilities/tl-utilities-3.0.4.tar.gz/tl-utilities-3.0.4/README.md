## Utility package for Cloudless Resource Monitoring Framework

- singleton.py: provides Singleton metaclass that is used in various systems.
- tinydb_wrapper.py: provides HostTinyDbWrapper & QueryCriteriaTinyDbWrapper classes that is used to interact with tinydb, and encapsulates useful methods to store/retrieve/remove hosts as well as necessary daemon information of each hosts.
- helper.py: provides useful helper methods (e.g., convert yaml to json, extract docker configuration from yaml)

#### Versions:
- `1.x.x`: used with vrmjobs-ver2
- `2.x.x`: used with vrmjobs-ver3
- `3.0.3`: used with vrmjobs-ver3 for **combined collector-monitor system**
- `3.0.4`: used with crm-dtos
