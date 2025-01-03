name: Download YouTube Video with yt-dlp and Cookies

on:
  push:
    branches:
      - main

jobs:
  download-video:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install yt-dlp
          sudo apt-get update
          sudo apt-get install -y ffmpeg

      - name: Download YouTube video using cookies and proxy
        run: |
          yt-dlp --cookies yt_cookies.txt --proxy "socks5://127.0.0.1:9050" \
                 --download-sections "*0-10" -o "video.mp4" \
                 "https://youtu.be/3vW-l8XbVoU?si=A7I2Fu_QUiJ9PpJj"

      - name: Upload video as artifact
        uses: actions/upload-artifact@v3
        with:
          name: downloaded-video
          path: video.mp4