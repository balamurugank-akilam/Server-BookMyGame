# ---------------------------------------
# Dockerfile for Django + MSSQL (Waitress)
# ---------------------------------------

# Use slim Python image
FROM python:3.11.9-slim

# Set working directory
WORKDIR /app

# Install dependencies and ODBC Driver 18 for SQL Server
RUN apt-get update && apt-get install -y \
    curl gnupg apt-transport-https unixodbc-dev gcc g++ lsb-release software-properties-common \
    && curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/microsoft.gpg \
    && echo "deb [arch=amd64] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for Docker caching)
COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose Django port
EXPOSE 8000

# ✅ Start Django app using Waitress with more threads (improves concurrency)
# Replace `bookmygame.wsgi:application` with your actual WSGI module path if different.
CMD ["waitress-serve", "--listen=0.0.0.0:8000", "--threads=8", "bookmygame.wsgi:application"]
