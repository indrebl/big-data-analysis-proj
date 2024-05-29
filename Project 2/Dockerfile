# Parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy current directory contents into the container
COPY . .

# Install packages
RUN pip install --no-cache-dir -r requirements.txt

# Run the application
CMD ["python", "./big_data_2assign.py"]
