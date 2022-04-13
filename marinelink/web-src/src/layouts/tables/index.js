/**
=========================================================
* Soft UI Dashboard React - v2.0.0
=========================================================

* Product Page: https://www.creative-tim.com/product/soft-ui-dashboard-material-ui
* Copyright 2021 Creative Tim (https://www.creative-tim.com)

Coded by www.creative-tim.com

 =========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
*/

// @mui material components
import Card from "@mui/material/Card";

// Soft UI Dashboard React components
import SuiBox from "components/SuiBox";
import SuiTypography from "components/SuiTypography";
import SuiAvatar from "components/SuiAvatar";
import SuiBadge from "components/SuiBadge";

// Soft UI Dashboard React example components
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "examples/Navbars/DashboardNavbar";
import Snackbar from "@mui/material/Snackbar";
import MuiAlert from "@mui/material/Alert";
// import Footer from "examples/Footer";
import Table from "examples/Table";

// Custom styles for the Tables
import styles from "layouts/tables/styles";

import { useEffect, useState, forwardRef } from "react";
import { useHistory } from "react-router-dom";
import { useAuth } from "auth-context/auth.context";
import ContractApi from "api/contract";
import downBox from "assets/images/down_box.png";
import upBox from "assets/images/up_box.png";
import send from "assets/images/send.png";

import Modal from "@mui/material/Modal";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";
import { Button, Link } from "@mui/material";
import { API_SERVER } from "config/constant";
/* eslint-disable react/prop-types */

const ContractTypeIconMap = {
  100: downBox, // 선하증권 icon
  200: upBox,
  300: send,
};

const ContractTypeKeyMap = {
  100: "bill_of_lading", // 선하증권 icon
  200: "second",
  300: "third",
};

const ContractStatusKeyMap = {
  10: "created",
  20: "saved",
  30: "before-checked",
  40: "checked",
  50: "done",
};

const ContractStatusColorMap = {
  10: "warning",
  20: "secondary",
  30: "info",
  40: "primary",
  50: "success",
};

const Alert = forwardRef(function Alert(props, ref) {
  return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

function ContractType({ contract_type, contract_id }) {
  return (
    <SuiBox display="flex" alignItems="center" px={1} py={0.5}>
      <SuiBox mr={2}>
        <SuiAvatar
          src={ContractTypeIconMap[contract_type]}
          alt={name}
          size="sm"
          variant="rounded"
        />
      </SuiBox>
      <SuiBox display="flex" flexDirection="column">
        <SuiTypography variant="button" fontWeight="medium">
          {contract_id}
        </SuiTypography>
        {/* <SuiTypography variant="caption" textColor="secondary">
          {email}
        </SuiTypography> */}
      </SuiBox>
    </SuiBox>
  );
}

function PeopleInfo({ name, phone }) {
  return (
    <SuiBox display="flex" flexDirection="column">
      <SuiTypography variant="caption" fontWeight="medium" textColor="text">
        {name}
      </SuiTypography>
      <SuiTypography variant="caption" textColor="secondary">
        {phone}
      </SuiTypography>
    </SuiBox>
  );
}

function Tables() {
  const { user } = useAuth();
  const [tableRecords, setTableRecords] = useState([]);
  const [selectedConsignorInfo, setSelectedConsignorInfo] = useState({
    name: "",
    phone: "",
    sign: false,
  });
  const [selectedConsigneeInfo, setSelectedConsigneeInfo] = useState({
    name: "",
    phone: "",
    sign: false,
  });
  const [selectContractId, setSelectedContractId] = useState(-1);
  const [selectContractStatus, setSelectedContractStatus] = useState(ContractStatusKeyMap[10]);
  const [selectContractType, setSelectedContractType] = useState(ContractTypeKeyMap[100]);
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState("");
  const history = useHistory();
  const columnInfo = [
    { name: "contract_type", title: "Contract Type", align: "left" },
    { name: "consignor", title: "Consignor", align: "left" },
    { name: "consignee", title: "Consignee", align: "center" },
    { name: "status", title: "Status", align: "center" },
    { name: "create_date", title: "Create Date", align: "center" },
    { name: "contract_date", title: "Contract Date", align: "center" },
    { name: "action", title: "action", align: "center" },
  ];
  const getActionState = (keyword) => {
    switch (keyword) {
      case ContractStatusKeyMap[10]:
        return "Edit";
      case ContractStatusKeyMap[20]:
        return "Edit";
      case ContractStatusKeyMap[30]:
        return "State";
      case ContractStatusKeyMap[40]:
        return "State";
      case ContractStatusKeyMap[50]:
        return "Show";
      default:
        return "Edit";
    }
  };
  useEffect(() => {
    ContractApi.getContractList(user).then((response) => {
      const records = response.data.data.contract.map((contract) => {
        return {
          contract_type: <ContractType contract_type={contract.type} contract_id={contract.id} />,
          consignor: (
            <PeopleInfo name={contract.consignor_info.name} phone={contract.consignor_info.phone} />
          ),
          consignee: (
            <PeopleInfo name={contract.consignee_info.name} phone={contract.consignee_info.phone} />
          ),
          status: (
            <SuiBadge
              variant="gradient"
              badgeContent={ContractStatusKeyMap[contract.status]}
              color={ContractStatusColorMap[contract.status]}
              size="extra-small"
            />
          ),
          create_date: (
            <SuiTypography variant="caption" textColor="secondary" fontWeight="medium">
              {contract.create_date}
            </SuiTypography>
          ),
          contract_date: (
            <SuiTypography variant="caption" textColor="secondary" fontWeight="medium">
              {contract.contract_date ? contract.contract_date : ""}
            </SuiTypography>
          ),
          action: (
            <SuiTypography
              style={{ cursor: "pointer" }}
              variant="caption"
              textColor="secondary"
              fontWeight="medium"
              onClick={() => {
                switch (contract.status) {
                  case 10:
                    history.push("/dashboard", {
                      data: {
                        contractType: ContractTypeKeyMap[contract.type],
                        contractId: contract.id,
                      },
                    });
                    break;
                  case 20:
                    history.push("/dashboard", {
                      data: {
                        contractType: ContractTypeKeyMap[contract.type],
                        contractId: contract.id,
                      },
                    });
                    break;
                  case 30:
                  case 40:
                  case 50:
                    setSelectedConsignorInfo((prevState) => {
                      return {
                        ...prevState,
                        name: contract.consignor_info.name,
                        phone: contract.consignor_info.phone,
                      };
                    });
                    setSelectedConsigneeInfo((prevState) => {
                      return {
                        ...prevState,
                        name: contract.consignee_info.name,
                        phone: contract.consignee_info.phone,
                      };
                    });
                    setSelectedContractId(contract.id);
                    ContractApi.getContractSignStatus(user, contract.id).then((response) => {
                      setSelectedConsignorInfo((prevState) => {
                        return {
                          ...prevState,
                          sign: response.data.data.consignor,
                        };
                      });
                      setSelectedConsigneeInfo((prevState) => {
                        return {
                          ...prevState,
                          sign: response.data.data.consignee,
                        };
                      });
                      setSelectedContractStatus(response.data.data.status);
                      setSelectedContractType(response.data.data.type);
                    });
                    openModal();
                    break;
                  // case 50:
                  //   setSelectedConsignorInfo(index);
                  //   openModal();
                  //   break;
                }
              }}
            >
              {getActionState(ContractStatusKeyMap[contract.status])}
            </SuiTypography>
          ),
        };
      });
      setTableRecords(records);
    });
  }, [openSnackbar]);
  const classes = styles();
  // const { columns, rows } = authorsTableData;
  // const { columns: prCols, rows: prRows } = projectsTableData;
  const [isModalOpen, setIsModalOpen] = useState(false);
  const openModal = () => {
    setIsModalOpen(true);
  };
  const closeModal = () => {
    setIsModalOpen(false);
  };
  const handleClose = (event, reason) => {
    if (reason === "clickaway") {
      return;
    }
    setOpenSnackbar(false);
  };
  return (
    <DashboardLayout>
      <DashboardNavbar />
      <SuiBox py={3}>
        <SuiBox mb={3}>
          <Card>
            <SuiBox display="flex" justifyContent="space-between" alignItems="center" p={3}>
              <SuiTypography variant="h6">Contract List</SuiTypography>
            </SuiBox>
            <SuiBox customClass={classes.tables_table}>
              <Table columns={columnInfo} rows={tableRecords} />
            </SuiBox>
          </Card>
        </SuiBox>
      </SuiBox>
      <Modal
        open={isModalOpen}
        onClose={closeModal}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box
          sx={{
            position: "absolute",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            width: 600,
            bgcolor: "background.paper",
            boxShadow: 24,
            p: 4,
          }}
        >
          <Typography id="modal-modal-title" variant="h5" component="h2">
            Contract State
          </Typography>
          <Divider />
          <Box>
            <Typography id="modal-modal-title" variant="h6" component="h6">
              Consignor
            </Typography>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <Typography>
                {selectedConsignorInfo.name ? selectedConsignorInfo.name : ""}
              </Typography>
              <Typography>
                {selectedConsignorInfo.phone ? selectedConsignorInfo.phone.replaceAll("-", "") : ""}
              </Typography>
              <Button
                color={selectedConsignorInfo.sign ? "success" : "secondary"}
                onClick={() => {
                  if (!selectedConsignorInfo.sign) {
                    window.open(API_SERVER + "/api/contract/consignor/" + selectContractId);
                  }
                }}
              >
                {selectedConsignorInfo.sign ? "Signed" : "Unsigned"}
              </Button>
            </div>
          </Box>
          <Box>
            <Typography id="modal-modal-title" variant="h6" component="h6">
              Consignee
            </Typography>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <Typography>
                {selectedConsigneeInfo.name ? selectedConsignorInfo.name : ""}
              </Typography>
              <Typography>
                {selectedConsigneeInfo.phone ? selectedConsigneeInfo.phone.replaceAll("-", "") : ""}
              </Typography>
              <Button
                color={selectedConsigneeInfo.sign ? "success" : "secondary"}
                onClick={() => {
                  if (!selectedConsigneeInfo.sign) {
                    const contract_url = `${API_SERVER}/api/contract/consignee/${selectContractId}`;
                    navigator.clipboard.writeText(contract_url);
                    alert(
                      "URL이 복사되었습니다. Consignee에게 URL을 전달하여 계약을 진행시켜주세요."
                    );
                  }
                }}
              >
                {selectedConsigneeInfo.sign ? "Signed" : "Unsigned"}
              </Button>
            </div>
          </Box>
          <Divider />
          <Box>
            <Button
              onClick={() => {
                if (ContractStatusKeyMap[selectContractStatus] === "done") {
                  console.log("get pdf checksum code");
                } else {
                  history.push("/dashboard", {
                    data: {
                      contractType: ContractTypeKeyMap[selectContractType],
                      contractId: selectContractId,
                    },
                  });
                }
              }}
            >
              {ContractStatusKeyMap[selectContractStatus] === "done" ? "CODE" : "EDIT"}
            </Button>
            <Button
              onClick={() => {
                console.log("test");
                ContractApi.runContract(user, selectContractId)
                  .then((response) => {
                    response;
                  })
                  .catch((err) => console.log(err));
                setSnackbarMessage("In Progress Contract");
                setOpenSnackbar(true);
                closeModal();
              }}
              disabled={ContractStatusKeyMap[selectContractStatus] === "done"}
            >
              Contract
            </Button>
            <Link
              href={
                ContractStatusKeyMap[selectContractStatus] !== "done"
                  ? ""
                  : `${API_SERVER}/api/contract/pdf/${selectContractId}`
              }
              variant="body2"
              color={
                ContractStatusKeyMap[selectContractStatus] !== "done" ? "secondary" : "primary"
              }
            >
              {ContractStatusKeyMap[selectContractStatus] !== "done" ? "" : "Download"}
            </Link>
          </Box>
        </Box>
      </Modal>
      <Snackbar
        open={openSnackbar}
        autoHideDuration={3000}
        onClose={handleClose}
        message={snackbarMessage}
      >
        <Alert onClose={handleClose} severity="success" sx={{ width: "100%" }}>
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </DashboardLayout>
  );
}

export default Tables;
