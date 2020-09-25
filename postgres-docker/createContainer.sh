docker run -p 5432:5432 -d -e POSTGRES_USER="tradebotv4" -e POSTGRES_PASSWORD="a-password" -e POSTGRES_DB="tradebotv4" -v pg-data:/var/lib/postgresql/data --name tradebotv4-container postgres
