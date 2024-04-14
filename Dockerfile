# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN pip install --upgrade pip
# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port on which script2.py will listen
EXPOSE 9000

# Define environment variables
ENV PYTHONUNBUFFERED=1

# Run script2.py when the container launches
CMD ["python", "Script2.py", "9000"]
