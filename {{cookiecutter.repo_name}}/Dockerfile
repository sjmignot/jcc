FROM python:3.10-slim

RUN apt-get update \
	&& apt-get install -y sudo fzf software-properties-common curl wget tar git libc6-dev gfortran unzip libhdf5-dev parallel gcc g++ musl-dev python3-dev libffi-dev libgdal-dev gdal-bin openssh-client

# download public key for github.com
RUN mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts

ENV POETRY_VERSION=1.1.13
RUN python3 -m pip install poetry

COPY pyproject.toml ./
RUN poetry config virtualenvs.in-project true --local
RUN --mount=type=ssh poetry install

COPY {{cookiecutter.repo_name}} /{{cookiecutter.repo_name}}

ENV PYTHONPATH "${PYTHONPATH}:/"

CMD ["poetry", "run", "jupyter-lab", ".", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''"]
