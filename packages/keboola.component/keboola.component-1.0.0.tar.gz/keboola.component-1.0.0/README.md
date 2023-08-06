# Keboola Python Component library

## Introduction

This library provides a Python wrapper over the
[Keboola Common Interface](https://developers.keboola.com/extend/common-interface/). It simplifies all tasks related
 to the communication of the [Docker component](https://developers.keboola.com/extend/component/) with the Keboola Connection that is defined by the Common Interface. 
 Such tasks are config manipulation, validation, component state, I/O handling, I/O metadata and manifest files, logging, etc.
 
 It is being developed by the Keboola Data Services team and officially supported by Keboola. It aims to simplify the Keboola Component creation process,
 by removing the necessity of writing boilerplate code to manipulate with the Common Interface. 
 
 Another useful use-case is within the Keboola [Python Transformations](https://help.keboola.com/transformations/python/) to simplify the I/O handling.
 
 ### Links
 
 - API Documentation: [API docs](https://github.com/keboola/python-component/tree/main/docs/api-html/component/interface.html)
 - Source code: [https://github.com/keboola/python-component](https://github.com/keboola/python-component)
 - PYPI project code: [https://test.pypi.org/project/keboola.component-kds/](https://test.pypi.org/project/keboola.component-kds/)
 - Documentation: [https://developers.keboola.com/extend/component/python-component-library](https://developers.keboola.com/extend/component/)
 - Python Component template project: [https://bitbucket.org/kds_consulting_team/kbc-python-template/src/master/](https://bitbucket.org/kds_consulting_team/kbc-python-template/src/master/)


 ## Quick start
 
 ### Installation 
 
 The package may be installed via PIP:
 
 ```
pip install keboola.component
```


### Core structure & functionality 

The package contains two core modules:

- `keboola.component.interface` - Core methods and class to initialize and handle the [Keboola Common Interface](https://developers.keboola.com/extend/common-interface/) tasks
- `keboola.component.dao` - Data classes and containers for objects defined by the Common Interface such as manifest files, metadata, environment variables, etc.


### CommonInterface

Core class that serves to initialize the docker environment. It handles the following tasks:

- Environment initialisation
   - Loading all [environment variables](https://developers.keboola.com/extend/common-interface/environment/#environment-variables)
   - Loading the [configuration file](https://developers.keboola.com/extend/common-interface/config-file/) and initialization of the [data folder](https://developers.keboola.com/extend/common-interface/folders/)
   - [State file](https://developers.keboola.com/extend/common-interface/config-file/#state-file) processing.
   - [Logging](https://developers.keboola.com/extend/common-interface/logging/)
- [Data folder](https://developers.keboola.com/extend/common-interface/folders/) manipulation
    - [Manifest file](https://developers.keboola.com/extend/common-interface/manifest-files/) processing
    - Config validation
    - Metadata manipulation
    - [OAuth](https://developers.keboola.com/extend/common-interface/oauth/) configuration handling.

#### Initialization

The core class is `keboola.component.interface.CommonInterface`, upon it's initialization the environment is 
created. e.g.

- data folder initialized (either from the Environment Variable or manually)
- config.json is loaded
- All Environment variables are loaded

The class can be either extended or just instantiated and manipulated like object. 
The `CommonInterface` class is exposed in the `keboola.component` namespace:

```python
from keboola.component import CommonInterface
```

#### Loading configuration parameters:

The below example loads initializes the common interface class and automatically loading config.json from the 
[data folder](https://developers.keboola.com/extend/common-interface/folders/) which is defined by an environment variable `KBC_DATADIR`,
 if the variable is not present, and error is raised. To override the data folder location provide the `data_folder_path` parameter into constructor. 

```python
from keboola.component import CommonInterface
# Logger is automatically set up based on the component setup (GELF or STDOUT)
import logging

SOME_PARAMETER = 'some_user_parameter'
REQUIRED_PARAMETERS = [SOME_PARAMETER]

# init the interface
# A ValueError error is raised if the KBC_DATADIR does not exist or contains non-existent path.
ci = CommonInterface()

# Checks for required parameters and throws ValueError if any is missing.
ci.validate_configuration(REQUIRED_PARAMETERS)

# print KBC Project ID from the environment variable if present:
logging.info(ci.environment_variables.project_id)

# load particular configuration parameter
logging.info(ci.configuration.parameters[SOME_PARAMETER])
```


#### Processing input tables

Tables and their manifest files are represented by the `keboola.component.dao.TableDefinition` object and may be loaded 
using the convenience method `get_input_tables_definitions()`. The result object contains all metadata about the table,
such as manifest file representations, system path and name.

```python
from keboola.component import CommonInterface
import logging

# init the interface
ci = CommonInterface()

input_tables = ci.get_input_tables_definitions()

# print path of the first table (random order)
first_table = input_tables[0]
logging.info(f'The first table named: "{first_table.name}" is at path: {first_table.full_path}')



# get information from table manifest
logging.info(f'The first table has following columns defined in the manifest {first_table.columns}')

```


#### Processing state files

[State files](https://developers.keboola.com/extend/common-interface/config-file/#state-file) can be easily written and loaded 
using the `get_state_file()` and `write_state_file()` methods:
 
```python
from keboola.component import CommonInterface
from datetime import datetime
import logging

# init the interface
ci = CommonInterface()

last_state = ci.get_state_file()

# print last_updated if exists
logging.info(f'Previous job stored following last_updated value: {last_state.get("last_updated","")})')

# store new state file
ci.write_state_file({"last_updated": datetime.now().isoformat()})
```


#### I/O table manifests and processing results

The component may define output [manifest files](https://developers.keboola.com/extend/common-interface/manifest-files/#dataouttables-manifests) 
that define options on storing the results back to the Keboola Connection Storage. This library provides methods that simplifies 
the manifest file creation and allows defining the export options and metadata of the result table using helper objects `TableDefinition` 
and `TableMetadata`.


`TableDefinition` object serves as a result container containing all the information needed to store the Table into the Storage. 
It contains the manifest file representation and initializes all attributes available in the manifest.


This object represents both Input and Output manifests. All output manifest attributes are exposed in the class.

There are convenience methods for result processing and manifest creation `CommonInterface.write_table_def_manifest`. 
Also it is possible to create the container for the output table using the `CommonInterface.create_out_table_definition()`.

![TableDefinition dependencies](docs/imgs/TableDefinition_class.png)


**Example:**

```python
from keboola.component import CommonInterface
from keboola.component import dao

# init the interface
ci = CommonInterface()

# create container for the result
result_table = ci.create_out_table_definition('my_new_result_table', primary_key=['id'], incremental=True)

# write some content
with open(result_table.full_path, 'w') as result:
    result.write('line')

# add some metadata
result_table.table_metadata.add_table_description('My new table description')
# add column datatype
result_table.table_metadata.add_column_data_type('id', dao.SupportedDataTypes.STRING, 
                                                 source_data_type='VARCHAR(100)', 
                                                 nullable=True,
                                                 length=100)

# write manifest
ci.write_tabledef_manifest(result_table)
```

##### Get input table by name

```python
from keboola.component import CommonInterface


# init the interface
ci = CommonInterface()
table_def = ci.get_input_table_definition_by_name('input.csv')

```

##### Initializing TableDefinition object from the manifest file

```python
from keboola.component import dao

table_def = dao.TableDefinition.build_from_manifest('data/in/tables/table.csv.manifest')

# print table.csv full-path if present:

print(table_def.full_path)

# rows count

print(table_def.rows_count)
```

##### Retrieve raw manifest file definition (CommonInterface compatible)

To retrieve the manifest file representation that is compliant with Keboola Connection Common Interface 
use the `table_def.get_manifest_dictionary()` method. 


```python
from keboola.component import dao

table_def = dao.TableDefinition.build_from_manifest('data/in/tables/table.csv.manifest')

# get the  manifest file representation
manifest_dict = table_def.get_manifest_dictionary()

```




#### Processing input files

Similarly as tables, files and their manifest files are represented by the `keboola.component.dao.FileDefinition` object and may be loaded 
using the convenience method `get_input_files_definitions()`. The result object contains all metadata about the file,
such as manifest file representations, system path and name.

The `get_input_files_definitions()` supports filter parameters to filter only files with a specific tag or retrieve only the latest file of each. 
This is especially useful because the KBC input mapping will by default include all versions of files matching specific tag. By default, the method 
returns only the latest file of each.

```python
from keboola.component import CommonInterface
import logging

# init the interface
ci = CommonInterface()

input_files = ci.get_input_files_definitions(tags= ['my_tag'], only_latest_files=True)

# print path of the first file (random order) matching the criteria
first_file = input_files[0]
logging.info(f'The first file named: "{input_files.name}" is at path: {input_files.full_path}')


```


When working with files it may be useful to retrieve them in a dictionary structure grouped either by name or a tag group. 
For this there are convenience methods `get_input_file_definitions_grouped_by_tag_group()` and `get_input_file_definitions_grouped_by_name()`


```python
from keboola.component import CommonInterface
import logging

# init the interface
ci = CommonInterface()

# group by tag
input_files_by_tag = ci.get_input_file_definitions_grouped_by_tag_group(only_latest_files=True)

# print list of files matching specific tag
logging.info(input_files_by_tag['my_tag']) 


# group by name
input_files_by_name = ci.get_input_file_definitions_grouped_by_name(only_latest_files=True)

# print list of files matching specific name
logging.info(input_files_by_name['image.jpg'])

```