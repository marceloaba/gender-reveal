FROM python:3.10.0rc2-slim

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY src/requirements.txt /app/
RUN pip3 install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
RUN mkdir data
COPY src/static/ /app/static/
COPY src/templates /app/templates/
COPY src/main.py /app/

# Run the application
CMD ["python", "main.py"]