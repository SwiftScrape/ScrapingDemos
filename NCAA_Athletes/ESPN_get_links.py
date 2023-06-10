import requests
from bs4 import BeautifulSoup as bs
import json

def main():
    while 1:
        try:
            if (type_ := input('Basketball or Football: Enter b or f\n').rstrip().lower()) in ['b', 'f']:
                break
        except ValueError:
            pass
    try:
        if type_ == 'b':
            save_as, url = 'team_urls_basketball.json', 'http://www.espn.com/mens-college-basketball/players'
        elif type_ == 'f':
            save_as, url = 'team_urls_football.json', 'http://www.espn.com/college-football/players'
        else:
            print('Error')
            return
    except FileNotFoundError:
        print('File not found. Be sure the json file is in the directory.')
        return
    
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    }
    
    response = requests.get(url, headers=headers)
    links = {}
    soup = bs(response.content, 'html.parser')

    for w in soup.find_all('a', {'style': 'padding-left:0px;'}):
        links.update({w.text.lower().replace("'",''): w['href']})
    
    with open(save_as, 'w') as f:
        json.dump(links, f)

if __name__ == '__main__':
    main()