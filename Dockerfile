# Use the official Python image as the base image
FROM python:3.10.10-slim

# Set the working directory in the container
WORKDIR /app
RUN echo "Working directory set to /app"

# Copy all files excluding the venv directory
COPY . /app
RUN echo "Files copied to /app"

# Install ffmpeg by apt-get
RUN apt-get update
RUN apt-get install -y ffmpeg wget
RUN echo "ffmpeg installed"

# Install the required dependencies
RUN pip install -r requirements.txt
RUN echo "Python packages installed"

# download files to whisper_models directory
RUN mkdir whisper_models
RUN wget -O whisper_models/base.pt https://jf-open-prod-1301446188.cos.ap-guangzhou.myqcloud.com/media/P/24/0223/models/whispermodels/base.pt
RUN wget -O whisper_models/tiny.pt https://jf-open-prod-1301446188.cos.ap-guangzhou.myqcloud.com/media/P/24/0223/models/whispermodels/tiny.pt
RUN wget -O whisper_models/small.pt https://jf-open-prod-1301446188.cos.ap-guangzhou.myqcloud.com/media/P/24/0223/models/whispermodels/small.pt
RUN wget -O whisper_models/medium.pt https://jf-open-prod-1301446188.cos.ap-guangzhou.myqcloud.com/media/P/24/0223/models/whispermodels/medium.pt
RUN wget -O whisper_models/large-v3.pt https://jf-open-prod-1301446188.cos.ap-guangzhou.myqcloud.com/media/P/24/0223/models/whispermodels/large-v3.pt

# Expose the port that the web service will be running on
WORKDIR /app
EXPOSE 8000
RUN echo "Port 8000 exposed"

# Start the web service using uvicorn
CMD ["python", "main.py"]