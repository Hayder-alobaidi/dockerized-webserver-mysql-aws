# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY templates /app/templates
COPY  app.py .

# Expose port 5001
EXPOSE 5000

#Run the app 
CMD ["python", "app.py"]


