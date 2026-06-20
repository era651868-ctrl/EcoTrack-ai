# Use the official lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the local code files into the container
COPY . /app

# Install all required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the standard Cloud Run port variable
EXPOSE 8080

# Execute Streamlit with precise routing variables matching Google Cloud requirements
CMD ["sh", "-c", "streamlit run app.py --server.port=${PORT:-8080} --server.address=0.0.0.0"]

