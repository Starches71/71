
name: ImageMagick Gradient Filter Directly to Image

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  image-overlay:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Set up ImageMagick
      run: |
        sudo apt update
        sudo apt install -y imagemagick ffmpeg

    - name: Verify ImageMagick Installation
      run: |
        convert -version || { echo "convert not found!"; exit 1; }

    - name: List files in current directory (debugging)
      run: ls -l

    - name: Download Image from Repository
      run: cp "images (31).jpeg" base_image.jpeg

    - name: Verify that input image exists (debugging)
      run: |
        if [ ! -f "base_image.jpeg" ]; then
          echo "base_image.jpeg not found!"
          exit 1
        else
          echo "base_image.jpeg found!"
        fi

    - name: Get Image Dimensions
      id: dimensions
      run: |
        width=$(convert base_image.jpeg -format "%w" info:)
        height=$(convert base_image.jpeg -format "%h" info:)
        echo "Width: $width, Height: $height"
        echo "::set-output name=width::$width"
        echo "::set-output name=height::$height"

    - name: Apply Linear Gradient Filter Directly to Image
      run: |
        convert base_image.jpeg -size ${{ steps.dimensions.outputs.width }}x${{ steps.dimensions.outputs.height }} gradient:white-black -compose Multiply -gravity center -composite output.png

    - name: Add Text to Image using ffmpeg
      run: |
        # Variables for dynamic text wrapping
        MAX_WIDTH=${{ steps.dimensions.outputs.width }}
        TEXT="Samsung phones can now flip into two. This is based on CNN news."
        FONT_SIZE=30
        TEXT_X="(w-text_w)/2"
        TEXT_Y="h-text_h-10"
        
        # Calculate the dynamic font size and wrap text if needed
        ffmpeg -i output.png -vf "drawtext=text='${TEXT}':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:fontsize=${FONT_SIZE}:fontcolor=white:x=${TEXT_X}:y=${TEXT_Y}:wrap=word" -y output_with_text.png

    - name: Verify that output_with_text.png was created (debugging)
      run: |
        if [ ! -f "output_with_text.png" ]; then
          echo "output_with_text.png not created!"
          exit 1
        else
          echo "output_with_text.png created successfully!"
        fi

    - name: List files in current directory after applying text (debugging)
      run: ls -l

    - name: Upload Processed Image as Artifact
      uses: actions/upload-artifact@v4
      with:
        name: image-artifact
        path: output_with_text.png
