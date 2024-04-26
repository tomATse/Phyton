import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Function to crawl and download all MP3 files from a website
def download_mp3_files(url, download_path):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all <a> tags with href attribute containing '.mp3'
    mp3_links = soup.find_all('a', href=lambda href: href and href.endswith('.mp3'))
    
    # Create download directory if it doesn't exist
    os.makedirs(download_path, exist_ok=True)
    
    # Get local list of files
    downloaded_files = os.listdir(download_path)
    
    # Download each MP3 file
    for link in mp3_links:
        mp3_url = urljoin(url, link['href'])
        mp3_filename = os.path.basename(mp3_url)
        mp3_filepath = os.path.join(download_path, mp3_filename)
    
        # If not already downloaded
        if mp3_filename not in downloaded_files:
            
            # Download MP3 file 
            print("Downloading:", mp3_filename)
            with open(mp3_filepath, 'wb') as f:
                response = requests.get(mp3_url,stream=True)
                f.write(response.content)
        else:
            print("Exsiting:", mp3_filename)
            
# Example usage 
#website_url = "https://archive.org/download/BBC_Essential_Mix_Collection" #player url
website_url = "https://ia803107.us.archive.org/20/items/BBC_Essential_Mix_Collection/" #forwarded real download url
download_directory = "E:\\"
download_mp3_files(website_url, download_directory)



