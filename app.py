import os
from flask import Flask, request, render_template
from TX_WBB_Attendance import attendance_graph
import json


team_id_file = open('espn_team_ids.json')
team_ids = json.load(team_id_file)

template_dir = os.path.abspath('.')
app = Flask(__name__, template_folder=template_dir)

if __name__ == '__main__':
    app.run(debug=True)


@app.route("/")
def attedance():
    attendance_plot = attendance_graph(251)['chart']
    context = {"attendance": attendance_plot, "team_ids": team_ids}

    return render_template('index.html', context=context)


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
