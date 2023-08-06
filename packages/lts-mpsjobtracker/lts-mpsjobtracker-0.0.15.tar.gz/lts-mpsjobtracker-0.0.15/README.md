# mps-job-tracker

## Introduction

A job tracker service for Media Preservation Services that provides standard methods to create and manage job tracker files in the Asset Ingest message queue.

## Technology Stack
##### Language
Python

##### Development Operations
Docker Compose

## Configuration

This package reads configuration values from environment variables.

### Jobs directory

#### When importing this package in another project
The package writes job tracker files to a directory specified in the environment variable `JOB_DATA_BASEDIR`. When importing this package into another project, set this environment variable to the path of the jobs directory.

#### When using this project
In this project, the job tracker directory is set in the environment variables configuration file `.env`. The job tracker directory should be set to the jobs directory inside the container.

`JOB_DATA_BASEDIR=/home/appuser/jobs/`

The docker-compose file in this project mounts the jobs directory from inside the container to a local directory on the host filesystem. In this configuration, the jobs will be written to `/home/appuser/jobs` inside the container and that directory is mounted to the `./jobs` directory on the host filesystem.

```
    volumes:
      # App
      - './:/home/appuser'
      # Jobs
      - './jobs:/home/appuser/jobs'
```

## Installation

```
$ pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ lts-mpsjobtracker==0.0.3
$ python
>>> import mpsjobtracker.trackers.jobtracker as jobtracker
>>> jt = jobtracker.JobTracker()
>>> jt.init_tracker_file('create_asset')
{'job_ticket_id': '39aa64a5-7451-45fc-b5bd-68d1bf02b31e-43e85fab1540', 'job_name': 'create_asset', 'job_management': {'current_step': 1, 'steps': {'1': 'generate_mock_manifest', '2': 'retrieve_image_from_origin', '3': 'check_jp2_compliance', '4': 'create_thumbnails', '5': 'save_to_storage', '6': 'save_data'}, 'job_status': '', 'previous_step_status': ''}, 'context': {}, 'creation_date': '2020-11-10 22:24:00', 'last_modified_date': '2020-11-10 22:24:00'}
```

## Local Development Environment Setup Instructions

### 1: Clone the repository to a local directory
git clone git@github.huit.harvard.edu:LTS/mps-job-tracker.git

### 2: Create app config

##### Create config file for environment variables
- Make a copy of the config example file `./env-example.txt`
- Rename the file to `.env`
- Replace placeholder values as necessary

*Note: The config file .env is specifically excluded in .gitignore and .dockerignore, since it contains credentials it should NOT ever be committed to any repository.*

### 3: Start

##### START

This command builds the docker image runs the container specified in the docker-compose.yml configuration.

```
docker-compose up --build --force-recreate
```

### 4: Open a shell in the container

##### Run docker exec to execute a shell in the container by name

Open a shell using the exec command to access the mps-job-tracker container.

```
docker exec -it mps-job-tracker bash
```

### 5: Install dependencies
This step is only required if additional python dependencies must be installed. Update the requirements.txt inside the container to install new python packages in the project. If the dependencies are required for the package to run, they also must be included in the `install_requires` section of setup.py.

##### Install a new pip package

Once inside the mps-job-tracker container, run the pip install command to install a new package and update the requirements text file.

```
pip install packagename && pip freeze > requirements.txt
```

##### Add dependencies to setup

Add the names of the dependencies to the `install_requires` section of setup.py. Read more about adding dependencies in this article [Specifying dependencies](https://python-packaging.readthedocs.io/en/latest/dependencies.html).

### 6: Build and publish the package

#### Step 6A: Prepare the distribution
* Update the version number in `setup.py`
* Remove the old `dist/` directory from the previous build if necessary

#### Step 6B: Build the distribution

Once inside the container, build the distribution.

`python3 setup.py sdist bdist_wheel`

A new directory `dist` will be created in the container.

#### Step 6C: Register for an account

[Register for an account](https://test.pypi.org/account/register/) on the test python package repository. Enable two-factor authentication for logins. [Create a token](https://test.pypi.org/manage/account/#api-tokens).

#### Step 6D: Upload package to the test repository

Publish the package to the test repository `testpypi` before publishing it to the production repository.

`python3 -m twine upload --repository testpypi dist/*`

#### Step 6E: Test the package
Open the package in the repository and view the version history.

https://test.pypi.org/project/lts-mpsjobtracker/0.0.1/

Read [Installation](#installation) in this document for instructions on how to install and test the package in another project or environment.

### 7: Stop

##### STOP AND REMOVE

This command stops and removes all containers specified in the docker-compose-local.yml configuration. This command can be used in place of the 'stop' and 'rm' commands.

```
docker-compose -f docker-compose-local.yml down
```

## More information
Read the documenation for more information on building and publishing the distribution.

* [Generating distribution archives](https://packaging.python.org/tutorials/packaging-projects/#generating-distribution-archives)

* [Uploading the distribution archives](https://packaging.python.org/tutorials/packaging-projects/#uploading-the-distribution-archives)

* https://tom-christie.github.io/articles/pypi/