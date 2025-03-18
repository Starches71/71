
FROM python:3.9-slim

# Install dependencies
RUN apt update && apt install -y ffmpeg && \
    pip install yt-dlp

# Set the working directory
WORKDIR /app

# Default command to run yt-dlp inside the container
CMD ["yt-dlp", "ytsearch2:Samsung S25", "-o", "samsung_s25_%(title)s.%(ext)s", "--format", "mp4"]
