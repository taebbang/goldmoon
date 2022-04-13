import React, { useState } from "react";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";

import Box from "@mui/material/Box";

import IconButton from "@mui/material/IconButton";
import AddIcon from "@mui/icons-material/Add";
import RemoveIcon from "@mui/icons-material/Remove";

const commonStyles = {
  bgcolor: "background.paper",
  m: 1,
  // border: 1,
};

import PropTypes from "prop-types";

function Person({ index, personInfo, onChangeHandler }) {
  const [name, setName] = useState(personInfo.name ? personInfo.name : "");
  const [tel, setTel] = useState(personInfo.TEL ? personInfo.TEL : "");
  const [fax, setFax] = useState(personInfo.FAX ? personInfo.FAX : "");
  const [location, setLocation] = useState(personInfo.location ? personInfo.location : "");
  return (
    <div>
      <TextField
        focused
        style={{ margin: 4 }}
        id="Outlined"
        label="Name"
        value={name}
        onChange={(event) => {
          setName(event.target.value);
          onChangeHandler(index, {
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
          onChangeHandler(index, {
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
          onChangeHandler(index, {
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
          onChangeHandler(index, {
            name: name,
            TEL: tel,
            FAX: fax,
            location: event.target.value,
          });
        }}
        variant="standard"
      />
    </div>
  );
}

Person.defaultProps = {
  index: -1,
  personInfo: {},
  onChangeHandler: () => {},
};

// Typechecking props for the Breadcrumbs
Person.propTypes = {
  index: PropTypes.number.isRequired,
  personInfo: PropTypes.object,
  onChangeHandler: PropTypes.func,
};

function PersonList({ personClass, onChangeHandler, propPersonInfoList }) {
  const [personInfoList, setPersonInfoList] = useState(propPersonInfoList);
  const defaultPersonInfo = {
    name: "Hong Gil Dong",
    TEL: "010-0000-0000",
    FAX: "010-0000-0000",
    location: "SEOUL, KOREA",
  };
  const [personList, setPersonList] = useState(
    personInfoList.map((personInfo, index) => {
      return (
        <Person
          key={index}
          index={index}
          personInfo={personInfo}
          onChangeHandler={(index, personInfo) => {
            setPersonInfoList((prevState) => {
              prevState[index] = { ...personInfo };
              onChangeHandler(prevState);
              return [...prevState];
            });
          }}
        />
      );
    })
  );

  return (
    <Box
      variant="outlined"
      // sx={{ ...commonStyles, borderColor: "grey.500" }}
      sx={{ ...commonStyles }}
      style={{ margin: 10, padding: 10 }}
    >
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <Typography variant="subtitle2" gutterBottom component="div">
          {personClass}
        </Typography>
        <div>
          <IconButton
            style={{ marginRight: 20 }}
            size="large"
            color="dark"
            component="span"
            onClick={() => {
              setPersonInfoList((prevState) => {
                prevState.push(defaultPersonInfo);
                onChangeHandler(prevState);
                return [...prevState];
              });
              setPersonList((prevState) => {
                prevState.push(
                  <Person
                    key={personList.length}
                    index={personList.length}
                    personInfo={personInfoList[personList.length]}
                    onChangeHandler={(index, personInfo) => {
                      setPersonInfoList((prevState) => {
                        prevState[index] = { ...personInfo };
                        onChangeHandler(prevState);
                        return [...prevState];
                      });
                    }}
                  />
                );
                return [...prevState];
              });
            }}
          >
            <AddIcon />
          </IconButton>
          <IconButton
            style={{ marginRight: 20 }}
            size="large"
            color="dark"
            component="span"
            onClick={() => {
              setPersonInfoList((prevState) => {
                prevState.pop();
                onChangeHandler(prevState);
                return [...prevState];
              });
              setPersonList((prevState) => {
                prevState.pop();
                return [...prevState];
              });
            }}
          >
            <RemoveIcon />
          </IconButton>
        </div>
      </div>
      <div>{personList}</div>
    </Box>
  );
}

PersonList.defaultProps = {
  personClass: "",
  onChangeHandler: () => {},
  propPersonInfoList: [],
};

// Typechecking props for the Breadcrumbs
PersonList.propTypes = {
  personClass: PropTypes.string.isRequired,
  onChangeHandler: PropTypes.func.isRequired,
  propPersonInfoList: PropTypes.array,
};

export default PersonList;
