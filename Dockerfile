FROM python:3.8

# Set the working directory inside the container
WORKDIR /app

# Copy your Python code into the container
COPY . /app

# Install any dependencies (if needed)
RUN pip install -r requirements.txt

# Specify the command to run your Python script
CMD ["python", "bot.py"]