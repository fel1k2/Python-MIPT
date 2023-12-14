import requests
from bs4 import BeautifulSoup
from database import Database


def extract_review_text(review_tag):
    tooltip_html = review_tag.get('data-tooltip-html', '')
    soup_tooltip = BeautifulSoup(tooltip_html, 'html.parser')
    return soup_tooltip.get_text(strip=True)


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Content-Type': 'text/html; charset=UTF-8'
}

dbase = Database()


def parse():
    if dbase.has_data():
        dbase.clear_data()
    with dbase.connect() as con:
        cur = con.cursor()
        for item in range(1, 15, 1):
            url = f'https://store.steampowered.com/search/?page={item}'
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            game_titles = soup.find_all('span', attrs={'class': 'title'})
            game_date_of_release = soup.find_all('div',
                                                 attrs={'class': 'col search_released responsive_secondrow'})
            game_prices = soup.find_all('div', attrs={'class': 'discount_final_price'})
            game_reviews = soup.find_all('span', attrs={'class': 'search_review_summary positive'})
            game_url = []
            data = soup.find_all('a', class_='search_result_row ds_collapse_flag')

            games_descriptions = []
            games_developers = []
            games_publishers = []
            games_minimal_requirements = []

            for urls in data:
                new_url = urls.get('href')
                game_url.append(new_url)

            for game in game_url:
                game_minimal_req = []
                new_response = requests.get(game, headers=headers)
                new_soup = BeautifulSoup(new_response.text, 'html.parser')
                game_description = new_soup.find('div', attrs={'class': 'game_description_snippet'})
                game_developer = new_soup.find('div', class_='grid_content')
                minimal_requirements = new_soup.find('div', class_='sysreq_contents')

                if minimal_requirements:
                    # minimal_requirements_text = []
                    minimal_requirements = minimal_requirements.find('ul', class_='bb_ul')
                    if minimal_requirements is None:
                        games_minimal_requirements.append("None")
                    else:
                        minimal_requirements_text = minimal_requirements.find_all('li')
                        for req in minimal_requirements_text:
                            game_minimal_req.append(req.text.strip())
                    games_minimal_requirements.append(game_minimal_req)
                else:
                    games_minimal_requirements.append("cannot be displayed because verification is required "
                                                      "THE GAME MAY CONTAIN CONTENT THAT IS NOT SUITABLE FOR ALL AGES"
                                                      " OR TO WATCH AT WORK.")

                if game_developer:
                    game_developer = game_developer.find('a')
                if game_developer is None:
                    games_developers.append("cannot be displayed because verification is required "
                                            "THE GAME MAY CONTAIN CONTENT THAT IS NOT SUITABLE FOR ALL AGES"
                                            " OR TO WATCH AT WORK.")
                    games_publishers.append("cannot be displayed because verification is required "
                                            "THE GAME MAY CONTAIN CONTENT THAT IS NOT SUITABLE FOR ALL AGES"
                                            " OR TO WATCH AT WORK.")
                else:
                    games_developers.append(game_developer.text.strip())
                    game_publisher = game_developer.find_next('div', class_='grid_content').find('a')
                    if game_publisher is None:
                        games_publishers.append("None")
                    else:
                        games_publishers.append(game_publisher.text.strip())

                if game_description is None:
                    games_descriptions.append("cannot be displayed because verification is required "
                                              "THE GAME MAY CONTAIN CONTENT THAT IS NOT SUITABLE FOR ALL AGES"
                                              " OR TO WATCH AT WORK.")
                else:
                    games_descriptions.append(game_description.text.strip())
            min_req_str_list = [', '.join(map(str, req_list)) for req_list in games_minimal_requirements]
            # counter = 0
            for counter in range(min(len(game_titles), len(game_date_of_release), len(game_prices), len(game_reviews),
                                     len(games_descriptions), len(games_developers), len(games_publishers),
                                     len(min_req_str_list))):
                text_content = extract_review_text(game_reviews[counter])
                cur.execute('''
                    INSERT INTO games (titles, release_date, price, review, description, developer, publisher, min_req)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (game_titles[counter].text.strip(), game_date_of_release[counter].text.strip(),
                      game_prices[counter].text.strip(), text_content,
                      games_descriptions[counter].strip(), games_developers[counter].strip(),
                      games_publishers[counter].strip(),
                      min_req_str_list[counter]))
            con.commit()


def start():
    dbase.create()
    parse()
    return 'success'


if __name__ == "__main__":
    start()
