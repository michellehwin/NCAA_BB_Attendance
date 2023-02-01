import React from 'react';
import { useEffect, useState } from "react";
import embed from 'vega-embed';

const Graph = ({ team, deleteGraph, women }) => {


    const [graph, setGraph] = useState(null);
    useEffect(() => {
        console.log(team.id);
        let url = `NCAA_WBB_Attendance_Graph?team_id=${team.id}&team_name=${team.name}`;
        women ? url += "&women=true" : url += "&women=false";
        fetch(process.env.REACT_APP_FLASK_URL + url)
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
            let graphID = "#graph" + team.id + (women ? "W" : "M");
            embed(graphID, spec, embedOpt)
                .catch(error => showError(el, error));
        }
    }, [graph, team]);


    return (
        <div className='graphContainer'>
            <div id={"graph" + team.id + (women ? "W" : "M")}>{graph ? "" : "Loading..."}</div>
            {
                graph &&
                (<p>Average Home Attendance: {graph && (Math.round(graph.avg_home_attendance)).toLocaleString("en-US")}</p>)
            }
        </div>
    );
};

export default Graph;