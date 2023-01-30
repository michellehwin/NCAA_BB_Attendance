import { useEffect, useState } from "react";
import Select from 'react-select';
import PropTypes from 'prop-types';

const TeamSelector = ({ teams, setTeams }) => {

  const [selectedTeam, setSelectedTeam] = useState(null);

  const [teamOptions, setTeamOptions] = useState(null);
  // fetch all team options and update dropdown
  useEffect(() => {
    fetch(process.env.REACT_APP_FLASK_URL + "ESPNTeams").then(response => {
      return response.json();
    }).then(data => {
      return setTeamOptions(data);
    });
  }, []);

  const getTeamOptions = teams => {
    let options = [];
    for (let team in teams) {
      const teamObj = {};
      const currTeamID = teams[team];
      teamObj.value = currTeamID;
      teamObj.label = team;
      options.push(teamObj);
    }
    return options;
  };

  const handleChange = (selectedOption) => {
    console.log(selectedOption);
    setSelectedTeam({ id: selectedOption.value, name: selectedOption.label });
  };
  const handleClick = (e) => {
    setTeams([...teams, selectedTeam]);
  };

  return (
    <div>
      <Select className="teamSelect" onChange={handleChange} options={getTeamOptions(teamOptions)} />
      <button onClick={handleClick}>Add Team</button>
    </div>
  );
};

TeamSelector.propTypes = {
  setTeams: PropTypes.func.isRequired
};

export default TeamSelector;