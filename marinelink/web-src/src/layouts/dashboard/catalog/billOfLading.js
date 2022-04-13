import { useState } from "react";

import IconButton from "@mui/material/IconButton";
import SaveIcon from "@mui/icons-material/Save";
import Button from "@mui/material/Button";

import MiniStatisticsCard from "examples/Cards/StatisticsCards/MiniStatisticsCard";
import ArchiveIcon from "@mui/icons-material/Archive";
// import AddLinkIcon from "@mui/icons-material/AddLink";
import AssignmentTurnedInIcon from "@mui/icons-material/AssignmentTurnedIn";
import CardComponent from "@mui/material/Card";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import Person from "./component/person";
import PersonList from "./component/personList";

/* eslint-disable react/prop-types */
function Card({ cardClickListner }) {
  return (
    <MiniStatisticsCard
      title={{ text: "B/L" }}
      count="Bill of Lading"
      icon={{ color: "info", component: <ArchiveIcon /> }}
      backgroundColor="#74BAFF"
      colorThema="dark"
      catalogClickListner={cardClickListner}
    />
  );
}

const commonStyles = {
  bgcolor: "background.paper",
  m: 1,
  // border: 1,
};

function Contract({ contractId, propsContractInfo, saveClickListner, saveContractListner }) {
  const [contractInfo, setContractInfo] = useState(propsContractInfo);
  console.log(contractInfo);
  return (
    <CardComponent style={{ padding: 10, backgroundColor: "#F9F9F9" }}>
      <div style={{ padding: 10, justifyContent: "space-between", display: "flex" }}>
        <h2>선하증권 </h2>
        <div>
          <IconButton
            style={{ marginRight: 20 }}
            size="large"
            color="dark"
            component="span"
            onClick={() => {
              saveClickListner(contractId, "bill_of_lading", contractInfo);
            }}
          >
            <SaveIcon />
          </IconButton>
          {/* <IconButton
            style={{ marginRight: 20 }}
            size="large"
            color="dark"
            component="span"
            onClick={() => {
              console.log("click");
            }}
          >
            <AddLinkIcon />
          </IconButton> */}
        </div>
      </div>
      <Person
        personClass="Consignor"
        personInfo={contractInfo.consignor}
        onChangeHandler={(consignorInfo) => {
          setContractInfo((prevState) => {
            return {
              ...prevState,
              consignor: consignorInfo,
            };
          });
        }}
      />
      <Person
        personClass="Consignee"
        personInfo={contractInfo.consignee}
        onChangeHandler={(consigneeInfo) => {
          setContractInfo((prevState) => {
            return {
              ...prevState,
              consignee: consigneeInfo,
            };
          });
        }}
      />
      <PersonList
        personClass="Notify Party"
        propPersonInfoList={contractInfo.notify_party}
        onChangeHandler={(notifyPartInfoList) => {
          setContractInfo((prevState) => {
            prevState.notify_party = [...notifyPartInfoList];
            return {
              ...prevState,
            };
          });
        }}
      />
      <Box variant="outlined" sx={{ ...commonStyles }} style={{ margin: 10, padding: 10 }}>
        <Typography variant="subtitle2" gutterBottom component="div">
          Basic Information
        </Typography>
        <div>
          <TextField
            focused
            style={{ marginRight: 10, width: "47%" }}
            id="Outlined"
            label="Export Reference"
            value={contractInfo.export_references}
            onChange={(event) => {
              setContractInfo((prevState) => {
                return {
                  ...prevState,
                  export_references: event.target.value,
                };
              });
            }}
            variant="standard"
          />
          <TextField
            focused
            style={{ marginLeft: 10, width: "47%" }}
            id="Outlined"
            label="Forwaring Agent Reference"
            value={contractInfo.forwarding_agent_reference}
            onChange={(event) => {
              setContractInfo((prevState) => {
                return {
                  ...prevState,
                  forwarding_agent_reference: event.target.value,
                };
              });
            }}
            variant="standard"
          />
        </div>
        <div style={{ marginTop: 15 }}>
          <TextField
            focused
            style={{ marginRight: 10, width: "47%" }}
            id="Outlined"
            label="Point And Country Of Origin"
            value={contractInfo.point_and_country_of_origin}
            onChange={(event) => {
              setContractInfo((prevState) => {
                return {
                  ...prevState,
                  point_and_country_of_origin: event.target.value,
                };
              });
            }}
            variant="standard"
          />
          <TextField
            focused
            style={{ marginLeft: 10, width: "47%" }}
            id="Outlined"
            label="Domestic Routing / Export Instruction"
            value={contractInfo.domestic_routing__export_instructions}
            onChange={(event) => {
              setContractInfo((prevState) => {
                return {
                  ...prevState,
                  domestic_routing__export_instructions: event.target.value,
                };
              });
            }}
            variant="standard"
          />
        </div>
        <div style={{ marginTop: 15 }}>
          <TextField
            focused
            style={{ marginLeft: 0, width: "31%" }}
            id="Outlined"
            label="Pre Carriage BY"
            value={contractInfo.pre_carriage_by}
            onChange={(event) => {
              setContractInfo((prevState) => {
                return {
                  ...prevState,
                  pre_carriage_by: event.target.value,
                };
              });
            }}
            variant="standard"
          />
          <TextField
            focused
            style={{ marginLeft: "2%", marginRight: "2%", width: "31%" }}
            id="Outlined"
            label="Ocean Vessel"
            value={contractInfo.ocean_vessel}
            onChange={(event) => {
              setContractInfo((prevState) => {
                return {
                  ...prevState,
                  ocean_vessel: event.target.value,
                };
              });
            }}
            variant="standard"
          />
          <TextField
            focused
            style={{ margin: 0, width: "31%" }}
            id="Outlined"
            label="Port Of Discharge"
            value={contractInfo.port_of_discharge}
            onChange={(event) => {
              setContractInfo((prevState) => {
                return {
                  ...prevState,
                  port_of_discharge: event.target.value,
                };
              });
            }}
            variant="standard"
          />
        </div>
        <div style={{ marginTop: 15 }}>
          <TextField
            focused
            style={{ marginLeft: 0, width: "31%" }}
            id="Outlined"
            label="Place Of Receipt"
            value={contractInfo.place_of_receipt}
            onChange={(event) => {
              setContractInfo((prevState) => {
                return {
                  ...prevState,
                  place_of_receipt: event.target.value,
                };
              });
            }}
            variant="standard"
          />
          <TextField
            focused
            style={{ marginLeft: "2%", marginRight: "2%", width: "31%" }}
            id="Outlined"
            label="Place Of Receipt"
            value={contractInfo.place_of_receipt}
            onChange={(event) => {
              setContractInfo((prevState) => {
                return {
                  ...prevState,
                  place_of_receipt: event.target.value,
                };
              });
            }}
            variant="standard"
          />
          <TextField
            focused
            style={{ margin: 0, width: "31%" }}
            id="Outlined"
            label="Port Of Loading"
            value={contractInfo.port_of_loading}
            onChange={(event) => {
              setContractInfo((prevState) => {
                return {
                  ...prevState,
                  port_of_loading: event.target.value,
                };
              });
            }}
            variant="standard"
          />
        </div>
        <div style={{ marginTop: 15 }}>
          <TextField
            focused
            style={{ marginLeft: 0, width: "31%" }}
            id="Outlined"
            label="Onward Inland Routing"
            value={contractInfo.onward_inland_routing}
            onChange={(event) => {
              setContractInfo((prevState) => {
                return {
                  ...prevState,
                  onward_inland_routing: event.target.value,
                };
              });
            }}
            variant="standard"
          />
          <TextField
            focused
            style={{ marginLeft: "2%", marginRight: "2%", width: "31%" }}
            id="Outlined"
            label="For Transshipment To"
            value={contractInfo.for_transshipment_to}
            onChange={(event) => {
              setContractInfo((prevState) => {
                return {
                  ...prevState,
                  for_transshipment_to: event.target.value,
                };
              });
            }}
            variant="standard"
          />
          <TextField
            focused
            style={{ margin: 0, width: "31%" }}
            id="Outlined"
            label="Final Destination"
            value={contractInfo.final_destination}
            onChange={(event) => {
              setContractInfo((prevState) => {
                return {
                  ...prevState,
                  final_destination: event.target.value,
                };
              });
            }}
            variant="standard"
          />
        </div>
      </Box>
      <Box
        variant="outlined"
        // sx={{ ...commonStyles, borderColor: "grey.500" }}
        sx={{ ...commonStyles }}
        style={{ margin: 10, padding: 10 }}
      >
        <Typography variant="subtitle2" gutterBottom component="div">
          Particulars Furnished by Shipper
        </Typography>
        <TextField
          focused
          style={{ margin: 0, marginTop: 10, width: "95%" }}
          id="Outlined"
          label="Marks And Number"
          value={contractInfo.marks_n_number}
          onChange={(event) => {
            setContractInfo((prevState) => {
              return {
                ...prevState,
                marks_n_number: event.target.value,
              };
            });
          }}
          variant="standard"
          multiline={true}
        />
        <TextField
          focused
          style={{ margin: 0, marginTop: 10, width: "95%" }}
          id="Outlined"
          label="No Of Count / Pkgs"
          value={contractInfo.no_of_count_or_pkgs}
          onChange={(event) => {
            setContractInfo((prevState) => {
              return {
                ...prevState,
                no_of_count_or_pkgs: event.target.value,
              };
            });
          }}
          variant="standard"
          multiline={true}
        />
        <TextField
          focused
          style={{ margin: 0, marginTop: 10, width: "95%" }}
          id="Outlined"
          label="Description Of Pkgs / Goods"
          value={contractInfo.description_of_pkgs_or_goods}
          onChange={(event) => {
            setContractInfo((prevState) => {
              return {
                ...prevState,
                description_of_pkgs_or_goods: event.target.value,
              };
            });
          }}
          variant="standard"
          multiline={true}
        />
        <TextField
          focused
          style={{ margin: 0, marginTop: 10, width: "95%" }}
          id="Outlined"
          label="Gross Weight (Goods Weight)"
          value={contractInfo.goods_weight}
          onChange={(event) => {
            setContractInfo((prevState) => {
              return {
                ...prevState,
                goods_weight: event.target.value,
              };
            });
          }}
          variant="standard"
          multiline={true}
        />
        <TextField
          focused
          style={{ margin: 0, marginTop: 10, width: "95%" }}
          id="Outlined"
          label="Measurement"
          value={contractInfo.measurement}
          onChange={(event) => {
            setContractInfo((prevState) => {
              return {
                ...prevState,
                measurement: event.target.value,
              };
            });
          }}
          variant="standard"
          multiline={true}
        />
      </Box>
      <Box
        variant="outlined"
        // sx={{ ...commonStyles, borderColor: "grey.500" }}
        sx={{ ...commonStyles }}
        style={{ margin: 10, padding: 10 }}
      >
        <Typography variant="subtitle2" gutterBottom component="div">
          Revenue Information
        </Typography>
        <TextField
          focused
          style={{ margin: 0, marginTop: 10, width: "95%" }}
          id="Outlined"
          label="Freight and Charges Revenue Tons rate per "
          value={contractInfo.freight_and_charges_revenue_tons_rate_per}
          onChange={(event) => {
            setContractInfo((prevState) => {
              return {
                ...prevState,
                freight_and_charges_revenue_tons_rate_per: event.target.value,
              };
            });
          }}
          variant="standard"
          multiline={true}
        />
        <TextField
          focused
          style={{ margin: 0, marginTop: 10, width: "95%" }}
          id="Outlined"
          label="Prepaid"
          value={contractInfo.prepaid}
          onChange={(event) => {
            setContractInfo((prevState) => {
              return {
                ...prevState,
                prepaid: event.target.value,
              };
            });
          }}
          variant="standard"
          multiline={true}
        />
        <TextField
          focused
          style={{ margin: 0, marginTop: 10, width: "95%" }}
          id="Outlined"
          label="Collect"
          value={contractInfo.collect}
          onChange={(event) => {
            setContractInfo((prevState) => {
              return {
                ...prevState,
                collect: event.target.value,
              };
            });
          }}
          variant="standard"
          multiline={true}
        />
      </Box>
      <Box
        variant="outlined"
        sx={{ ...commonStyles, backgroundColor: "#ffebee" }}
        style={{
          marginLeft: "40%",
          marginRight: "40%",
          marginTop: 10,
          marginBotton: 10,
          padding: 10,
        }}
      >
        <Button
          style={{ width: "100%" }}
          size="large"
          startIcon={<AssignmentTurnedInIcon />}
          onClick={() => {
            saveContractListner(contractId, "bill_of_lading", contractInfo);
          }}
        >
          Contract
        </Button>
      </Box>
    </CardComponent>
  );
}

export { Card, Contract };
