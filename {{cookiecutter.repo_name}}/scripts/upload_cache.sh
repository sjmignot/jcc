docker build . -t {{cookiecutter.repo_name}} --ssh default

docker run -it \
	-v $GOOGLE_APPLICATION_CREDENTIALS:/tmp/keys/key.json:ro \
	-v $PWD/.cache:/.cache \
	-v ./output:/output \
	-v $PWD/{{cookiecutter.repo_name}}:/{{cookiecutter.repo_name}} \
	-e GOOGLE_APPLICATION_CREDENTIALS=/tmp/keys/key.json \
	poetry run upload_cache
