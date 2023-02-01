
import requests as rq
from bs4 import BeautifulSoup as bs
import pandas as pd
import altair as alt
from cachetools import cached, TTLCache
import plotly.express as px
import plotly
import json

cache = TTLCache(maxsize=100, ttl=86400)


class teamAttendanceInfo:
    def __init__(self, df: pd.DataFrame, aha, w: bool, x: list[str]):
        self.df = df
        self.avg_home_attendance = aha
        self.women = w
        self.xSort = x


@cached(cache)
def plotly_attendance_graph(team_id):

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

    fig = px.bar(df, x='Opponent', y='Attendance')
    graphJSON = plotly.io.to_json(fig, pretty=True)
    return graphJSON

# processes string women to boolean women


@cached(cache)
def get_attendance_df(team_id, women) -> teamAttendanceInfo:
    season = 2023
    url = ""
    if (women == "True" or women == "true"):
        url = f"http://www.espn.com/womens-college-basketball/team/schedule/_/id/{team_id}/season/{season}"
        women = True
    else:
        url = f"http://www.espn.com/mens-college-basketball/team/schedule/_/id/{team_id}/season/{season}"
        women = False

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
    return teamAttendanceInfo(df, home_attendance, women, data["Opponent"])


@cached(cache)
def attendance_graph(attendance_info: teamAttendanceInfo, team_name: str) -> dict:
    team_color = "#bf5700"

    women = attendance_info.women
    df = attendance_info.df
    xSort = attendance_info.xSort

    title = ""
    if (women):
        title = team_name + " (W)"
    else:
        title = team_name + " (M)"

    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Opponent:O', sort=xSort),
        y='Attendance',
        color=alt.Color('Location',
                        scale=alt.Scale(
                            domain=['Home', 'Away', 'Neutral'],
                            range=[team_color, 'darkgray', 'lightgray']))
    ).resolve_scale(
        x='independent'
    ).properties(
        title=title
    )
    chart_json = chart.to_json()
    stats = {'attendance_graph': json.loads(chart_json),
             'avg_home_attendance': attendance_info.avg_home_attendance}
    return stats
