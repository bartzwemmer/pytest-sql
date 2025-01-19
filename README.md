# SQL Testing in CI/CD pipelines
Many data pipelines include a SQL component. Especially the traditional ETL pipeline. These often consist of a (python) orchestration component and a SQL and Python processing component. While it is easy and standard practice to test the Python component, it is often not the case for the SQL component. This is inherently the case, where a running database is required, which can be used for testing without impacting production data.

To overcome that, we can use a temporary database for testing. This can be done by using a docker container, which can be started and stopped in the CI/CD pipeline, or by utilizing a database schema dedicated to testing. In order to run tests independant, it is important to tear down all resources after testing, in order to be able to run the tests on a clean state again.

This repository contains a mock data pipeline, to show a typicial repository layout with SQL files that are executed during the execution of the data pipeline. For the CI/CD pipeline, tests with `pytest` are used. 

## Repository layout
Under the `src` directory, the Python code is located. The `process.py` file contains the main function of the pipeline, which is called by the orchestration component. One of the pipeline steps is to execute the SQL files in the `sql` directory.

The tests are located under the `tests` directory. The `conftest.py` file contains the configuration for the tests. The `test_sql_functions.py` file contains the tests for the SQL functions.
```
.
├── README.md
├── sql
│   ├── format_pc_wpl.sql
├── src
│   ├── __init__.py
│   ├── process.py
|── tests
│   ├── conftest.py
│   ├── test_sql_functions.py
```
## Testing