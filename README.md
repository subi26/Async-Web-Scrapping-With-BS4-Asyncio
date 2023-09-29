# Async-Web-Scrapping-With-BS4-Asyncio
Effortlessly scrape and download images from web pages with this versatile Python tool. Automate batch downloads, exclude unwanted content, and boost your web scraping productivity. Simplify image collection for research, archiving, and more. Try it now!

## Features

- Asynchronously fetches and downloads images from a specified web page.
- Supports excluding specific keywords in URLs to filter unwanted content.
- Downloads images in batches to optimize performance.
- Easily customizable for different web scraping tasks.

## Usage

1. Clone this repository to your local machine:

```bash
git clone https://github.com/subi26/Async-Web-Scrapping-With-BS4-Asyncio

```

2.Install the required Python packages:

```bash
pip install grequests beautifulsoup4
```

3.Modify the script to suit your needs:

- Adjust the base_url variable to the URL of the web page you want to scrape.
- Customize the exclude_keywords list to exclude specific keywords from the scraped URLs.
- Set the batch_size to control the number of requests made in each batch.
- Modify the download_dir to specify the directory where downloaded images will be saved.

4.Run the script:
```bash
python main.py
```

## Example

Here's an example of how to use the web scraper:

```bash
from scraper import ImageScraper

base_url = 'http://example.com'
exclude_keywords = ['exclude', 'keywords']
batch_size = 100
download_dir = 'images'

scraper = ImageScraper(base_url, exclude_keywords, batch_size, download_dir)
scraper.scrape_images()

```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Acknowledgments
- Thanks to [Beautiful](https://www.crummy.com/software/BeautifulSoup/) Soup for the HTML parsing.
- Inspired by web scraping tutorials and examples from the Python community.
- Feel free to contribute, report issues, or suggest improvements to this project!

Happy web scraping!
