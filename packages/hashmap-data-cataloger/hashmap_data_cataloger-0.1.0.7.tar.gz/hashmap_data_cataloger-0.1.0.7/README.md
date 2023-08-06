<!---
Copyright © 2020 Hashmap, Inc

Licensed under the Apache License, Version 2.0 the \("License"\);
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
--->

# Hashmap Data Cataloger

Table of Contents

* [About](#about)
* [Using hdc](#using-hashmap-data-cataloger)

## About
The Hashmap Data Cataloger utility is used for data cataloging and asset mapping.

## Using Hashmap Data Cataloger
The Hashmap Data Cataloger(hdcm) can be used in two ways 
* as an API call
* run from CLI 


To use the Hashmap Data Cataloger(hdcm) you must first

1. If it does not already exist in the deployment environment, create a hidden directory in the 'user' root. give any name example .hashmap_data_-cataloger
2. Within the directory created in step 2 above, you must create a [connection profile YAML](#connection-profile-yaml). This will hold the necessary connection information to connect Netezza, BigQuery and other data sources. Out of the box, at this time, there is no key management solution integrated. This is on the feature roadmap.


#### As an API Call
Install hashmap-data-cataloger and all of its dependencies. This is a pypi package and can be installed as

```bash
pip install hashmap-data-cataloger
```

The API has 3 methods:
```
  catalog - get and return a tuple of databases, schemas, tables, columns
      params -
            source (source connection name in profile yml file) | required
            path (profile yml file) | required
      retuns - 
            data_tuple

  map - generate sql queries from a tuple of databases, schemas, tables, columns returned by catalog method
      params - 
            data_tuple | required
      retuns - 
            sql_tuple

  write - execute sql queries generated from map method
      params - 
            destination_env (destination connection name in profile yml file) | required
            path (profile yml file) | required
            sql_tuple | required
      retuns - 
            None
```
Call the API methods
```
from hdcm.factory.package_factory import PackageFactory

def run_cataloging(self):
    source_env = "netezza_jdbc"
    destination_env = "snowflake_admin_schema"
    data_tuple = PackageFactory.catalog(source_env, path)
    if data_tuple:
        sql_tuple = PackageFactory.map(data_tuple)
        PackageFactory.write(destination_env, path, sql_tuple)
```

#### Run from CLI
Install hashmap-data-cataloger and all of its dependencies. This is a pypi package and can be installed as
```bash
pip install hashmap-data-cataloger
```

Now that the environment is specified, pipeline defined, and so on, all that remains is to run the code. The code is executed from bash (or at the terminal) through

```
python -m hdc.hashmap_data_cataloger -p {path} -s{source} -d{destination} -l {log settings} -e {env}

e.g. 
python -m hdc.hashmap_data_cataloger -p C:\Users\xxxx\.hashmap_data_migrator\hdm_profiles.yml -s netezza_jdbc -d snowflake_admin_schema -e dev

```

The parameters are:

* path - profile yml file 
* source - source connection name in profile yml file
* destination - destination connection name in profile yml file
* log_settings - log settings path , default value ="log_settings.yml"
* env - environment to take connection information , default value ="prod"

## Connection Profile YAML

This files stores the connection information to the source and destination.
Its stored in local FS and its path is set in environment variable "HOME".
```yaml
dev:
  netezza_jdbc:  * Note:Add this section if using JDBC driver
    host: <host>
    port: <port>
    database: <database_name>
    user: <user_name>
    password: <password>
    driver:
      name: <driver_name>
      path: <driver_path>
  netezza_odbc:  * Note:Add this section if using ODBC driver
    host: <host>
    port: <port>
    database: <database_name>
    user: <user_name>
    password: <password>
    driver: <driver_name>
  snowflake_admin_schema:
    authenticator: snowflake
    account: <account>
    role: <role>
    warehouse: <warehouse_name>
    database: <database_name>
    schema: <schema_name>
    user: <user_name>
    password: <password>
```

