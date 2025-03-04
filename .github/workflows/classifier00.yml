name: Product Classification

on:
  push:
    branches:
      - main
  workflow_dispatch:  # Allows manual trigger of the workflow

jobs:
  classify_products:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v2

      - name: Set up SSH key
        uses: webfactory/ssh-agent@v0.5.3
        with:
          ssh-private-key: ${{ secrets.SSH_PRIVATE_KEY }}

      - name: Set up Python environment
        uses: actions/setup-python@v2
        with:
          python-version: 3.8

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt  # Assuming you have this file with required packages like 'requests', 'gitpython'

      - name: Run product classifier script
        run: |
          python prd_classifier.py --limit 50

      - name: Push changes if any
        run: |
          git add .
          git commit -m "Automated product classification update" || echo "No changes to commit"
          git push
