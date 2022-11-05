# CONTRIBUTING

## How to build the Dockerfile locally

....
docker build -t IMAGE_NAME .
....

## How to run the Dockerfile locally

....
docker run -dp 5000:5000 -w /app -v "$(pwd):/app" IMAGE_NAME sh -c "flask run --host 0.0.0.0"
....



# the next thing how to create env and so on