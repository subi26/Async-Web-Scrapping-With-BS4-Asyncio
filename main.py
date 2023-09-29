def main():
    base_url = 'http://192.168.1.5:12345'
    exclude_keywords = ['Private', 'Sent', '..']
    batch_size = 100
    download_dir = 'images'

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    scraper = ImageScraper(base_url, exclude_keywords, batch_size, download_dir)
    scraper.scrape_images()

if __name__ == "__main__":
    main()
