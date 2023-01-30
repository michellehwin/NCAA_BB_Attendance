# create venv: python3 -m venv env
# activate venv: source env/bin/activate
# deactivate: deactivate
# npm start: react
# start flask: flask --app main --debug run

import os
from flask import Flask, request, render_template
from TX_WBB_Attendance import attendance_graph, plotly_attendance_graph
import json
from flask_cors import CORS, cross_origin


team_id_file = open('espn_team_ids.json')
team_ids = json.load(team_id_file)

template_dir = os.path.abspath('.')
app = Flask(__name__, template_folder=template_dir)
CORS(app)


@app.route("/")
def attedance():
    # team_stats = attendance_graph(251)
    # context = {"attendance_graph": team_stats['chart'],
    #            "avg_home_attendance": team_stats['avg_home_attendance'], "team_ids": team_ids}
    # return render_template('index.html', context=context)
    return plotly_attendance_graph(251)


@app.route('/', methods=['POST'])
def get_team_id():
    team_id = request.form['team_id']
    print(f"team_id: {team_id}")
    if (team_id.isnumeric()):
        team_stats = attendance_graph(team_id)
        context = {"attendance_graph": team_stats['chart'],
                   "avg_home_attendance": team_stats['avg_home_attendance'], "team_ids": team_ids}
        return render_template('index.html', context=context)
    return ('', 204)


@app.route('/NCAA_WBB_Attendance_Graph')
@cross_origin()
def generate_attendance_graph():
    args = request.args
    team_id = args.get('team_id')
    if (team_id.isnumeric()):
        print(f"team_id: {team_id}")
        return attendance_graph(team_id, args.get('team_name'))
    return ('', 204)


@app.route('/ESPNTeams')
def returnTeams():
    return team_ids


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))