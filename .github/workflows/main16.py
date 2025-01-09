name: Download YouTube Video

on:
  push:
    branches:
      - main

jobs:
  download:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.8'

    - name: Install Chrome, Selenium, and yt-dlp
      run: |
        sudo apt update
        sudo apt install -y chromium-chromedriver
        pip install selenium yt-dlp

    - name: Log in to YouTube and Export Cookies
      run: python login_script.py

    - name: Download YouTube Video
      run: |
        yt-dlp --cookies cookies.txt https://youtu.be/Cr1mUzsJiXM
