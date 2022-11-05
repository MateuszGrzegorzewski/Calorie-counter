# CONTRIBUTING

## How to build the Dockerfile locally

....
docker build -t IMAGE_NAME .
....

## How to run the Dockerfile locally

....
docker run -dp 5000:5000 -w /app -v "$(pwd):/app" IMAGE_NAME sh -c "flask run --host 0.0.0.0"
....


### How to create .env

....
1. Fistly create .env
2. In .env: DATABASE_URL=postgresql://YOUR_DEVELOPMENT_URL
....
