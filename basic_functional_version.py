import grequests
import os
import asyncio
from bs4 import BeautifulSoup
from pprint import pprint
import urllib.parse

# Define the list of URLs pointing to JPEG images
image_urls = []

image_data = {}

href_urls = []

# Define the URL to fetch HTML content from
# url = 'http://192.168.1.5:12345/Android%2Fmedia%2Fcom.whatsapp%2FWhatsApp%2FMedia%2FWhatsApp+Images'
url = 'http://192.168.1.5:12345/inShare%2Ffiles%2FWhatsApp+Images'

# Send a GET request to the URL using grequests
response = grequests.get(url).send().response

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all <a> tags
    a_tags = soup.find_all('a')

    # Extract href URLs from the <a> tags
    for a in a_tags:
        if 'Private' in a.text or 'Sent' in a.text or '..' in a.text:
            continue
        href_urls.append(f"http://192.168.1.5:12345/{a.get('href')}")

    print(f"{len(href_urls)} Images Found")
else:
    print(f"Failed to fetch HTML content from {url}. Status code: {response.status_code}")

# # Create a set of unsent Requests
# print('starting async')
# rs = (grequests.get(url) for url in href_urls)
# print('ending async')

# # Send the requests asynchronously and get the responses
# print('start mapping')
# responses = grequests.map(rs)
# # pprint(responses)
# print('end mapping')

# Directory where you want to save the downloaded images
download_dir = 'images'

# Ensure the download directory exists
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Initialize success and failure counts
s_count = 0
f_count = 0
failed_urls = []

# Function to send requests and process responses for a batch of URLs
async def process_batch(batch_urls):
    global s_count, f_count, failed_urls  # Declare these variables as global

    # Create a list of Requests for this batch
    rs = (grequests.get(url) for url in batch_urls)
    
    # Send the requests asynchronously and get the responses
    responses = grequests.map(rs)
    
    # Process the responses for this batch
    for url, response in zip(batch_urls, responses):
        if response is not None and response.status_code == 200:
            # Extract the filename from the URL
            filename = os.path.basename(url.split('%2F')[-1])
            # Construct the local path to save the image
            local_path = os.path.join(download_dir, filename)
            
            # Save the image to the local path
            with open(local_path, 'wb') as file:
                file.write(response.content)
            s_count += 1
            print(f"Success : {s_count} && Failed : {f_count} && Downloaded: {url} -> {local_path}")
        else:
            f_count += 1
            print(f"Success : {s_count} && Failed : {f_count} && Failed to download: {url}")
            failed_urls.append(url)

# Create an event loop for asynchronous operations
loop = asyncio.get_event_loop()

# Define the batch size (e.g., 200)
batch_size = 200

# Split href_urls into batches
url_batches = [href_urls[i:i+batch_size] for i in range(0, len(href_urls), batch_size)]

# Loop through the batches and process them one by one
patch_count = 1
for batch_urls in url_batches:
    # Run the task for this batch asynchronously
    print(f"Processing Patch -> {patch_count}")
    loop.run_until_complete(process_batch(batch_urls))
    patch_count += 1

# Close the event loop
loop.close()

print(f"Success : {s_count} && Failed : {f_count}")
pprint(failed_urls)
