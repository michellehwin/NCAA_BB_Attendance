import React from 'react';
import { useEffect, useState } from "react";
import embed from 'vega-embed';

const Graph = ({ team, deleteGraph }) => {

    const [graph, setGraph] = useState(null);
    useEffect(() => {
        console.log(team.id);
        fetch(process.env.REACT_APP_FLASK_URL + `NCAA_WBB_Attendance_Graph?team_id=${team.id}&team_name=${team.name}`)
            .then(response => response.json())
            .then(data => {
                return setGraph(data);
            });
        console.log("fetch graph done");
        console.log(JSON.stringify(graph));
    }, [team]);


    useEffect(() => {
        console.log("render graph starting");
        if (graph) {
            var spec = graph.attendance_graph;
            spec['$schema'] = "https://vega.github.io/schema/vega-lite/v5.json";
            var embedOpt = { "mode": "vega-lite" };

            function showError(el, error) {
                el.innerHTML = ('<div class="error" style="color:red;">'
                    + '<p>JavaScript Error: ' + error.message + '</p>'
                    + "<p>This usually means there's a typo in your chart specification. "
                    + "See the javascript console for the full traceback.</p>"
                    + '</div>');
                throw error;
            }
            const el = document.getElementById('attendance');
            embed("#graph" + team.id, spec, embedOpt)
                .catch(error => showError(el, error));
        }
    }, [graph, team]);

    return (
        <div className='graphContainer'>
            <div id={"graph" + team.id}>{graph ? "" : "Loading..."}</div>
            <button onClick={() => deleteGraph(team)} className='graphCloseButton'>X</button>
            <p>Average Home Attendance: {graph && Math.round(graph.avg_home_attendance * 10) / 10}</p>
        </div>
    );
};

export default Graph;