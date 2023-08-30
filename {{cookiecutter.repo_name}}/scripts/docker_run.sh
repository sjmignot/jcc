docker build . -t {{cookiecutter.repo_name}} --ssh default

/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --app=http://localhost:8888/lab/ &

random_port=$(shuf -i 2000-65000 -n 1)

docker run -it \
	-v $GOOGLE_APPLICATION_CREDENTIALS:/tmp/keys/key.json:ro \
	-v $PWD/.cache:/{{cookiecutter.repo_name}}/.cache \
	-v ./output:/output \
	-v $PWD/{{cookiecutter.repo_name}}:/{{cookiecutter.repo_name}} \
	-e GOOGLE_APPLICATION_CREDENTIALS=/tmp/keys/key.json \
	-p $random_port:8888 \
	{{cookiecutter.repo_name}}
