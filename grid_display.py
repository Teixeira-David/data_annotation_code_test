"""
Project Name: Decoding Secret Message
Developer: David Teixeira
Date: 11/06/2024
Abstract: 
    You are given a Google Doc like that contains a list of Unicode characters and their positions in a 2D grid. 
    Your task is to write a function that takes in the URL for such a Google Doc as an argument, retrieves and parses the 
    data in the document, and prints the grid of characters. When printed in a fixed-width font, the characters in the 
    grid will form a graphic showing a sequence of uppercase letters, which is the secret message.

    Example URL: https://docs.google.com/document/d/e/2PACX-1vRMx5YQlZNa3ra8dYYxmv-QIQ3YJe8tbI3kqcuC7lQiZm-CSEznKfN_HYNSpoXcZIV3Y_O3YoUB1ecq/pub
        Expected Results:
            █▀▀▀
            █▀▀ 
            █      
    Test URL: https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub
        Expected Results:
            ████████░     ████████░   ██████████░    ███████░  ██░           ███░ ███░    ███░ ██░     ██░
            ██░     ██░ ███░     ███░ ██░          ███░    ██░ ███░   ███░   ██░    ██░  ██░   ██░     ██░
            ██░     ██░ ██░       ██░ ██░         ███░          ██░  █████░ ███░     ██░██░    ██░     ██░
            ████████░   ██░       ██░ ████████░   ██░           ███░ ██░██░ ██░       ███░     ██████████░
            ██░     ██░ ██░       ██░ ██░         ███░           ██░██░ ██░██░       ██░██░    ██░     ██░
            ██░     ██░ ███░     ███░ ██░          ███░    ██░   ████░   ████░      ██░  ██░   ██░     ██░
            ████████░     ████████░   ██████████░    ███████░     ██░     ██░     ███░    ███░ ██░     ██░     
            
    Requirements:
        - The document specifies the Unicode characters in the grid, along with the x- and y- coordinates of each character.
        - The minimum possible value of these coordinates is 0. There is no maximum possible value, so the grid can be arbitrarily large.
        - Any positions in the grid that do not have a specified character should be filled with a space character.
        - You can assume the document will always have the same format as the example document linked above.
        - Your code must be written in Python (preferred) or JavaScript.
        - You may use external libraries.
        - You may write helper functions, but there should be one function that:

    Arguments:
        1. Takes in one argument, which is a string containing the URL for the Google Doc with the input data, AND
        2. When called, prints the grid of characters specified by the input data, displaying a graphic of correctly oriented uppercase letters.        
"""

# Import Python Libraries
import pandas as pd
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup


class DecodeSecretMessage():
    """
    Class to decode the secret message from a Google Doc grid.
    """
    def __init__(self, url):
        self.url = url
        self.response = None
        self.grid = None

    @property
    def url(self):
        return self._url
    
    @url.setter
    def url(self, url): 
        if not isinstance(url, str):
            raise TypeError('URL must be a string') 
        if url.isspace():
            raise ValueError('URL cannot be empty') 
        
        # Validate the URL format
        parsed_url = urlparse(url)
        if parsed_url.scheme != "https" or parsed_url.netloc != "docs.google.com":
            raise ValueError("Invalid URL. Please provide a valid Google Doc URL.")
        self._url = url
    
    def verify_public_url(self):
        # Verify if the URL has a valid response
        try:
            self.response = requests.get(self.url) # Status code should be 200
            self.response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error accessing the URL: {e}")
            return False
        return True
        
    def get_data(self):
        # Make a GET request to the URL and extract the HTML content
        if not self.response:
            print("No response found.")
            return
            
        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(self.response.text, 'html.parser')
        table = soup.find('table')
        
        # Check if a table was found in the HTML content
        if not table:
            print("No table found in the document.")
            return
        
        # Extract data from the table
        grid_data = []
        rows = table.find_all('tr')
        
        # Get all the cells and append them to the grid data
        for row in rows[1:]:
            cells = row.find_all('td')
            if len(cells) >= 3:
                try:
                    x = int(cells[0].text.strip())
                    y = int(cells[2].text.strip())
                    char = cells[1].text.strip()
                    grid_data.append((x, y, char))
                except ValueError:
                    print("Error in parsing coordinates or character data.")
                    continue

        # Create DataFrame
        self.grid = pd.DataFrame(grid_data, columns=["x", "y", "char"])

    def display_grid(self):
        # Display the grid data
        if self.grid is None:
            self.get_data()
            
        # Check again if grid is empty after trying to fetch the data
        if self.grid is None:
            print("No data to display.")
            return
        
        # Get the dimensions of the grid
        max_x = self.grid["x"].max()
        max_y = self.grid["y"].max()

        # Create an empty grid
        grid = [[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)]

        # Fill in the grid with the characters
        for _, row in self.grid.iterrows():
            x = row["x"]
            y = row["y"]
            char = row["char"]
            grid[y][x] = char

        # Display the grid image
        for y in range(max_y, -1, -1):
            print("".join(grid[y]))
            

def Main():
    # Test the DecodeSecretMessage class
    #url = "https://docs.google.com/document/d/e/2PACX-1vRMx5YQlZNa3ra8dYYxmv-QIQ3YJe8tbI3kqcuC7lQiZm-CSEznKfN_HYNSpoXcZIV3Y_O3YoUB1ecq/pub"
    url = "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub"
    decode_message = DecodeSecretMessage(url)
    
    try:
        # Verify URL accessibility
        if not decode_message.verify_public_url():
            raise ValueError("Failed to access the URL. Please check the URL and make sure it is public.")
        
        # Retrieve and display data
        decode_message.get_data()
        decode_message.display_grid()
        
    except ValueError as e:
        print(f"Error: {e}")
        print("This might be due to a private or incorrect URL. Ensure the document is publicly accessible.")
    except Exception as e:
        print("An unexpected error occurred while processing the document.")
        print(f"Details: {e}")
    
    
if __name__ == '__main__':
    Main()    