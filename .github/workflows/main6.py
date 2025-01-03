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

      - name: Install yt-dlp
        run: |
          python -m pip install --upgrade pip
          pip install yt-dlp

      - name: Download YouTube video using cookies
        run: |
          yt-dlp --cookies yt_cookies.txt --download-sections "*0-10" -o "video.mp4" "https://youtu.be/3vW-l8XbVoU?si=A7I2Fu_QUiJ9PpJj"
        env:
          YT_COOKIES_FILE: yt_cookies.txt