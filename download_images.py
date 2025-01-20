
from icrawler import ImageCrawler
from icrawler.builtin import GoogleImageCrawler

def download_images():
    crawler = GoogleImageCrawler(storage={'root_dir': 'downloaded_images'})
    crawler.crawl(keyword='San Francisco', max_num=10)  # You can adjust the keyword and number of images

if __name__ == "__main__":
    download_images()
