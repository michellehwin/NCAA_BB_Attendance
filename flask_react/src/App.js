import TeamSelector from './components/TeamSelector';
import { useEffect, useState } from "react";
import embed from 'vega-embed';
import './App.css';
import Graph from './components/Graph';

// root app component, every component made should be put in here to be rendered
// jsx can only return one parent element
// can use <></> as parent element
function App() {

  const [teams, setTeams] = useState([{ "key": 251, "id": 251, "name": "Texas Longhorns" }]);

  const deleteGraph = (team) => {
    console.log("Deleting graph: " + team.name);
    setTeams(teams.filter(teamA => teamA.id !== team.id));
  };

  return (
    <div className="App">
      <header className="App-header">
      </header>
      <TeamSelector setTeams={setTeams} teams={teams} />
      {
        teams.map((team) => (
          <div className='teamContainer'>
            <Graph team={team} key={team.id + "W"} deleteGraph={deleteGraph} women={true} />
            <Graph team={team} key={team.id + "M"} deleteGraph={deleteGraph} women={false} />
            <button onClick={() => deleteGraph(team)} className='graphCloseButton'>X</button>
          </div>
        ))
      }
    </div>
  );
}

export default App;
