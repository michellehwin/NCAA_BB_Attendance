
import requests as rq
from bs4 import BeautifulSoup as bs
import pandas as pd
import altair as alt
from cachetools import cached, TTLCache

cache = TTLCache(maxsize=100, ttl=86400)


@cached(cache)
def attendance_graph(team_id):
    team_color = "#bf5700"
    season = 2023
    url = f"http://www.espn.com/womens-college-basketball/team/schedule/_/id/{team_id}/season/{season}"

    page = rq.get(url)
    soup = bs(page.content, features="lxml")
    table = soup.table

    home_game_count = 0
    home_attendance = 0
    data = {'Opponent': [],
            'Attendance': [],
            'Location': []}
    # loop through all games played this season
    for row in table.find_all('tr')[2:]:
        row_cells = row.find_all('td')
        try:
            opponent = row_cells[1].find_all('a')[1].contents[0]
            game_link = row_cells[2].find('a')['href']
            if (row_cells[1].find_all('span')[2].contents[-1] == "*"):
                location = "Neutral"
            else:
                location = "Home" if row_cells[1].find_all(
                    'span')[0].contents[0] == "vs" else "Away"

        except:
            break
        game_page = rq.get(game_link)
        game_soup = bs(game_page.content, features="lxml")
        atndnce = game_soup.find('div', {"class": "Attendance__Numbers"})
        atndnce = atndnce.contents[4] if atndnce != None else 0
        atndnce = ''.join(filter(str.isdigit, atndnce)
                          ) if atndnce != 0 else atndnce
        # add current row data to dictionary
        if atndnce != 0:
            data["Opponent"].append(opponent)
            data["Attendance"].append(float(atndnce))
            data["Location"].append(location)
            if location == "Home":
                home_game_count += 1
                home_attendance += int(atndnce)

    df = pd.DataFrame(data)
    if (home_game_count > 0):
        home_attendance = home_attendance/home_game_count  # calculate avg home attendance

    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Opponent', sort=data["Opponent"]),
        y='Attendance',
        color=alt.Color('Location',
                        scale=alt.Scale(
                            domain=['Home', 'Away', 'Neutral'],
                            range=[team_color, 'darkgray', 'lightgray']))
    )
    chart_json = chart.to_json()
    stats = {'chart': chart_json, 'avg_home_attendance': home_attendance}
    return stats
