# Use an official Python runtime as a parent image
FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Copy project
COPY . /app/

RUN pip install --upgrade pip && pip install -r requirements.txt

# Make entrypoint.sh executable
RUN chmod +x /app/entrypoint.sh

# Expose port 8000 to the outside world
EXPOSE 8000

# Run entrypoint.sh when the container launches
ENTRYPOINT ["/app/entrypoint.sh"]
