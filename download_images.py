from google_images_download import googleimagesdownload

def download_images(keyword, limit=10):
    response = googleimagesdownload()
    arguments = {
        "keywords": keyword,
        "limit": limit,  # Number of images to download
        "print_urls": True,
        "format": "jpg",
        "size": "medium",
        "output_directory": "downloaded_images",  # Directory to save images
    }
    response.download(arguments)

if __name__ == "__main__":
    keyword = "San Francisco"
    download_images(keyword, limit=1)
