from icrawler.builtin import GoogleImageCrawler

def download_images():
    # Create a GoogleImageCrawler instance
    crawler = GoogleImageCrawler(storage={'root_dir': 'downloaded_images'})
    
    # Start crawling for images related to "San Francisco"
    crawler.crawl(keyword='San Francisco', max_num=10)  # You can adjust the number of images

if __name__ == "__main__":
    download_images()
