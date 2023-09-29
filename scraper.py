import grequests
import os
import asyncio
from bs4 import BeautifulSoup
import urllib.parse

class ImageScraper:
    def __init__(self, base_url, exclude_keywords, batch_size, download_dir):
        # Constructor to initialize the ImageScraper object with parameters
        self.base_url = base_url
        self.exclude_keywords = exclude_keywords
        self.batch_size = batch_size
        self.download_dir = download_dir

    def fetch_image_urls(self, url):
        # Function to fetch image URLs from a web page
        image_urls = []
        
        # Send a GET request to the specified URL using grequests
        response = grequests.get(url).send().response

        if response.status_code == 200:
            # If the request is successful (status code 200), parse the HTML content
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            a_tags = soup.find_all('a')

            for a in a_tags:
                text = a.text.strip()
                if any(keyword in text for keyword in self.exclude_keywords):
                    continue
                href_url = urllib.parse.urljoin(self.base_url, a.get('href'))
                image_urls.append(href_url)

            print(f"{len(image_urls)} Images Found")
        else:
            print(f"Failed to fetch HTML content from {url}. Status code: {response.status_code}")

        return image_urls

    async def process_batch(self, batch_number, batch_urls):
        # Function to send requests and process responses for a batch of URLs
        success_count = 0
        failure_count = 0
        failed_urls = []

        # Create a list of Requests for this batch
        rs = (grequests.get(url) for url in batch_urls)
        
        # Send the requests asynchronously and get the responses
        responses = grequests.map(rs)

        for url, response in zip(batch_urls, responses):
            if response is not None and response.status_code == 200:
                # Extract the filename from the URL
                filename = os.path.basename(urllib.parse.unquote(url).split('/')[-1])
                # Construct the local path to save the image
                local_path = os.path.join(self.download_dir, filename)

                # Save the image to the local path
                with open(local_path, 'wb') as file:
                    file.write(response.content)
                success_count += 1
                print(f"Batch {batch_number} - Success: {success_count} && Failed: {failure_count} && Downloaded: {url} -> {local_path}")
            else:
                failure_count += 1
                print(f"Batch {batch_number} - Success: {success_count} && Failed: {failure_count} && Failed to download: {url}")
                failed_urls.append(url)

        return success_count, failure_count, failed_urls

    def scrape_images(self):
        # Main function to initiate image scraping
        href_urls = self.fetch_image_urls(self.base_url)
        loop = asyncio.get_event_loop()
        
        # Split href_urls into batches
        url_batches = [href_urls[i:i + self.batch_size] for i in range(0, len(href_urls), self.batch_size)]

        total_success_count = 0
        total_failure_count = 0
        total_failed_urls = []

        for batch_number, batch_urls in enumerate(url_batches, start=1):
            # Run the task for this batch asynchronously
            success_count, failure_count, failed_urls = loop.run_until_complete(
                self.process_batch(batch_number, batch_urls)
            )

            total_success_count += success_count
            total_failure_count += failure_count
            total_failed_urls.extend(failed_urls)

        loop.close()

        print(f"Total Success: {total_success_count} && Total Failed: {total_failure_count}")
        print("Failed URLs:")
        print(total_failed_urls)
