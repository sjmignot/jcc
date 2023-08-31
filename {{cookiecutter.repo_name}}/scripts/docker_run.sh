docker build . -t {{cookiecutter.repo_name}} --ssh default

random_port={{ range(2000, 65000) | random }}

/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --app=http://localhost:$random_port/lab/ &

docker run -it \
	-v $GOOGLE_APPLICATION_CREDENTIALS:/tmp/keys/key.json:ro \
	-v $PWD/.cache:/{{cookiecutter.repo_name}}/.cache \
	-v ./output:/output \
	-v $PWD/{{cookiecutter.repo_name}}:/{{cookiecutter.repo_name}} \
	-e GOOGLE_APPLICATION_CREDENTIALS=/tmp/keys/key.json \
	-p $random_port:8888 \
	{{cookiecutter.repo_name}}
