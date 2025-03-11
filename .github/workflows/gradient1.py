name: Apply Gradient Effect to Image

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main
  workflow_dispatch:

jobs:
  apply_gradient:
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
          pip install pillow

      - name: Apply gradient effect to image
        run: |
          python apply_gradient.py

      - name: Upload modified image as artifact
        uses: actions/upload-artifact@v4
        with:
          name: output-image
          path: output_gradient_image_upwards_white_text_pillow.jpeg
