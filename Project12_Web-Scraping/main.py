from bs4 import BeautifulSoup
import requests
import csv

response = requests.get("https://www.nba.com/stats").text
soup = BeautifulSoup(response, 'html.parser')

with open('player_data_nba.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    def scrape_section(section_name):
        section = soup.find('h2', text=section_name)
        if section:
            parent = section.find_parent('div', class_='LeaderBoardCard_lbcWrapper__e4bCZ')
            writer.writerow(['Player', section_name])
            rows = parent.find_all('tr', class_='LeaderBoardPlayerCard_lbpcTableRow___Lod5')
            for row in rows:
                name_tag = row.find('a', class_='Anchor_anchor__cSc3P')
                value_tag = row.find('td', class_='LeaderBoardWithButtons_lbwbCardValue__5LctQ')
                if name_tag and value_tag:
                    name = name_tag.text.strip()
                    value = value_tag.text.strip()
                    print(f"Player: {name}, {section_name}: {value}")
                    writer.writerow([name, value])
            writer.writerow([])
        else:
            print(f"{section_name} section not found.")

    scrape_section('Points')
    scrape_section('Rebounds')
    scrape_section('Assists')
    scrape_section('Blocks')
    scrape_section('Steals')
    scrape_section('Turnovers')

print("Scraping complete. Data saved to player_data_nba.csv.")
