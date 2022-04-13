import React, { useState } from "react";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";

import Box from "@mui/material/Box";

const commonStyles = {
  bgcolor: "background.paper",
  m: 1,
  // border: 1,
};

import PropTypes from "prop-types";

function Person({ personClass, onChangeHandler, personInfo }) {
  const [name, setName] = useState(personInfo.name);
  const [tel, setTel] = useState(personInfo.TEL);
  const [fax, setFax] = useState(personInfo.FAX);
  const [location, setLocation] = useState(personInfo.location);
  return (
    <Box
      variant="outlined"
      // sx={{ ...commonStyles, borderColor: "grey.500" }}
      sx={{ ...commonStyles }}
      style={{ margin: 10, padding: 10 }}
    >
      <Typography variant="subtitle2" gutterBottom component="div">
        {personClass}
      </Typography>
      <div>
        <TextField
          focused
          style={{ margin: 4 }}
          id="Outlined"
          label="Name"
          value={name}
          onChange={(event) => {
            setName(event.target.value);
            onChangeHandler({
              name: event.target.value,
              TEL: tel,
              FAX: fax,
              location: location,
            });
          }}
          variant="standard"
        />
        <TextField
          focused
          style={{ margin: 4 }}
          id="Outlined"
          label="TEL"
          value={tel}
          onChange={(event) => {
            setTel(event.target.value);
            onChangeHandler({
              name: name,
              TEL: event.target.value,
              FAX: fax,
              location: location,
            });
          }}
          variant="standard"
        />
        <TextField
          focused
          style={{ margin: 4 }}
          id="Outlined"
          label="FAX"
          value={fax}
          onChange={(event) => {
            setFax(event.target.value);
            onChangeHandler({
              name: name,
              TEL: tel,
              FAX: event.target.value,
              location: location,
            });
          }}
          variant="standard"
        />
        <TextField
          focused
          style={{ margin: 4 }}
          id="Outlined"
          label="Location"
          value={location}
          onChange={(event) => {
            setLocation(event.target.value);
            onChangeHandler({
              name: name,
              TEL: tel,
              FAX: fax,
              location: event.target.value,
            });
          }}
          variant="standard"
        />
      </div>
    </Box>
  );
}

Person.defaultProps = {
  personClass: "",
  onChangeHandler: () => {},
  personInfo: {},
};

// Typechecking props for the Breadcrumbs
Person.propTypes = {
  personClass: PropTypes.string.isRequired,
  onChangeHandler: PropTypes.func.isRequired,
  personInfo: PropTypes.object,
};

export default Person;
