import requests
from bs4 import BeautifulSoup as bs
import json
import csv

def read(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data

def find_team(name, data):    
    return data.get(name.lower().replace("'", ''))

def main():
    while 1:
        try:
            if (type_ := input('Basketball or Football: Enter b or f\n').rstrip().lower()) in ['b', 'f']:
                break
        except ValueError:
            pass
    try:
        if type_ == 'b':
            data = read('team_urls_basketball.json')
        elif type_ == 'f':
            data = read('team_urls_football.json')
        else:
            print('Error')
            return
    except FileNotFoundError:
        print('File not found. Be sure the json file is in the directory.')
        return
    csv_save_as = f"{type_}_data.csv"
    with open(csv_save_as, 'w', newline='') as f:
        pass

    with open(csv_save_as, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Picture', 'Name', 'Position', 'Height', 'Weight', 'Class', 'Birthplace', "Location", "TeamName"])
        for key in data:   
            print(key)
            url = data[key] 
            headers = {
                'authority': 'www.espn.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'en-US,en;q=0.9',
                'referer': 'http://www.espn.com/',
                'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'cross-site',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            }

            response = requests.get(url, headers=headers)
            soup = bs(response.content, 'html.parser')
            players = soup.find_all('tr', {'class': 'Table__TR Table__TR--lg Table__even'})

            for player in players:
                icon = player.find('img', {'data-mptype': 'image'})['alt']
                if 'nophoto.png' in icon:
                    icon = 'N/A'
                table = player.find_all('td', {'class': 'Table__TD'})
                name = table[1].find('a', {'class': 'AnchorLink'}).text
                pos = table[2].find('div', {'class': 'inline'}).text
                ht = table[3].find('div', {'class': 'inline'}).text
                wt = table[4].find('div', {'class': 'inline'}).text
                class_ = table[5].find('div', {'class': 'inline'}).text
                birthplace = table[6].find('div', {'class': 'inline'}).text
                team_name = url.split("/")[-1]
                writer.writerow([icon, name, pos, ht, wt, class_, birthplace, key, team_name])
        
if __name__ == '__main__':
    main()
