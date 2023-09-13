import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch

def search(content: str):
    params={
        "engine":"bing",
        "q":content,
        "cc":"US",
        "api_key":"06c729ea4c6c4ab9e1d3f35c94c3f6b231f164cbc5966bc10c31e855b88a3d28"
    }
    searching=GoogleSearch(params)
    results=searching.get_dict()
    final_value=f"Please answer "+content+" based on the search results: \n\n"+results['organic_results'][0]['snippet']
    return final_value

if __name__ == "__main__":
    print(search("Sun Wukong"))