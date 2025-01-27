
name: Run Starches Script

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  run-starches:
    runs-on: ubuntu-latest

    steps:
      # Step 1: Check out the repository
      - name: Checkout code
        uses: actions/checkout@v3

      # Step 2: Set up Python environment
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.9  # Specify Python 3.9

      # Step 3: Install dependencies
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install groq  # Install the Groq client library
          # Add any other dependencies if required

      # Step 4: Set up SSH key for GitHub authentication
      - name: Set up SSH key
        run: |
          mkdir -p ~/.ssh
          echo "$SSH_PRIVATE_KEY" > ~/.ssh/id_rsa
          chmod 600 ~/.ssh/id_rsa
          ssh-keyscan github.com >> ~/.ssh/known_hosts

      # Step 5: Run the starches.py script
      - name: Run starches.py
        run: python starches.py

      # Step 6: List output files (optional for debugging)
      - name: List output files
        run: ls -R
