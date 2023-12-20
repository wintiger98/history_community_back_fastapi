# Use a Python image
FROM python:3.11

# Set the working directory
WORKDIR /code/fastapi

# Copy the requirements file into the container
COPY ./requirements.txt /code/fastapi/requirements.txt

# Install system dependencies
RUN apt-get update && apt-get -y install libgl1-mesa-glx && apt-get -y install libpq-dev

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade -r /code/fastapi/requirements.txt

# Copy the app code into the container
COPY ./ /code/fastapi

# Specify the command to run when the container starts
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]