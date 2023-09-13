import requests
from bs4 import BeautifulSoup

def fetch(url: str):
    try:
        response = requests.get(url)
        html = response.text
        #print(html)
        soup = BeautifulSoup(html,'html.parser')
        p = soup.select("body > main > div > section > div.border-r10 > p:nth-child(3)")[0].text
        print(p)
        return f"Act as a summarizer. Please summarize {url}. The following is the content: \n\n{p}"
    except:
        print("fetch error")
        return "fetch error"
    


if __name__ == "__main__":
    fetch("https://dev.qweather.com/en/help")