# {{cookiecutter.project_name}}

## Setup

To setup, install dependencies using poetry.

```sh
poetry install
```

## Running

It is recommended to run the FAM code in Docker. This can either be done directly in bash or you can leverage a helper script

> **Note**
>
> Both the helper script and the recommended docker commands include the `--ssh default` flag.
> This is only necessary if a private git repo is being built in the image.

### Through Helper Script

```bash
poetry run dj
```

> **Note**
>
> This is a shortcut for running `./scripts/docker_run.sh`

### Directly through Script

To run the container without

```bash
docker build . -t {{cookiecutter.repo_name}} --ssh default

docker run -it \
	-v $GOOGLE_APPLICATION_CREDENTIALS:/tmp/keys/key.json:ro \
	-v ./output:/output \
	-v $PWD/{{cookiecutter.repo_name}}:/{{cookiecutter.repo_name}} \
	-e GOOGLE_APPLICATION_CREDENTIALS=/tmp/keys/key.json \
	-p 8888:8888 \
	{{cookiecutter.repo_name}}
```

## Managing Cloud Platform Caching

This project scaffold includes helper functions for uploading and downloading cached data from GCP. These steps require that you are authenticated and that the following bucket, **specified in the project setup**, exists:
`gs://{{cookiecutter.data_bucket_folder}}/{{cookiecutter.repo_name}}`

## Download cached data from a specific run of the analysis

To download cached data from a specific analysis run. If data from a past analysis has been uploaded, it can be redownloaded.

```sh
poetry download_cache
```

## To save cached data from a rerun of the notebook

To download cached data from a specific analysis run:

```sh
poetry upload_cache
```
