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
import { useState, useEffect, forwardRef } from "react";
import { useHistory } from "react-router-dom";
// @mui material components
import Card from "@mui/material/Card";
import Grid from "@mui/material/Grid";
// import Icon from "@mui/material/Icon";

// Soft UI Dashboard React components
import SuiBox from "components/SuiBox";
import SuiTypography from "components/SuiTypography";
import Snackbar from "@mui/material/Snackbar";
// Soft UI Dashboard React example components
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "examples/Navbars/DashboardNavbar";
import MuiAlert from "@mui/material/Alert";

// import Footer from "examples/Footer";
// import MiniStatisticsCard from "examples/Cards/StatisticsCards/MiniStatisticsCard";
// import ReportsBarChart from "examples/Charts/BarCharts/ReportsBarChart";
// import GradientLineChart from "examples/Charts/LineCharts/GradientLineChart";

// Soft UI Dashboard React base styles
// import typography from "assets/theme/base/typography";

// Dashboard layout components
// import BuildByDevelopers from "layouts/dashboard/components/BuildByDevelopers";
// import WorkWithTheRockets from "layouts/dashboard/components/WorkWithTheRockets";
// import Projects from "layouts/dashboard/components/Projects";
// import OrderOverview from "layouts/dashboard/components/OrderOverview";

// Data
// import reportsBarChartData from "layouts/dashboard/data/reportsBarChartData";
// import gradientLineChartData from "layouts/dashboard/data/gradientLineChartData";
import IconButton from "@mui/material/IconButton";
import ExpandLessIcon from "@mui/icons-material/ExpandLess";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
// import AccountBalanceIcon from "@mui/icons-material/AccountBalance";

import * as BL from "./catalog/billOfLading";
import * as Second from "./catalog/secondContract";
import ContractApi from "api/contract";
import { useAuth } from "auth-context/auth.context";

const contractCategoryMap = {
  bill_of_lading: 100,
};

const Alert = forwardRef(function Alert(props, ref) {
  return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

/* eslint-disable react/prop-types */
function Dashboard() {
  // const { size } = typography;
  // const { chart, items } = reportsBarChartData;
  const { user } = useAuth();
  const { setUser } = useAuth();
  const [usableCategoryList, setUsableCategoryList] = useState([]);
  const [isCategoryShow, setIsCategoryShow] = useState(true);
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState("");
  const [contractBody, setContractBody] = useState(undefined);
  const history = useHistory();
  useEffect(() => {
    ContractApi.getUsableList(user).then((response) => {
      if (response.data.success) {
        setUsableCategoryList(createCategoryListComponent(response.data.data.options));
      } else {
        setUser(undefined);
        return history.push("/authentication/sign-in");
      }
    });
  }, []);

  useEffect(() => {
    if (history.location.state) {
      if (history.location.state.data.contractType === "bill_of_lading") {
        const contractId = history.location.state.data.contractId;
        setIsCategoryShow(false);
        ContractApi.getContractInfo(user, contractId).then((response) => {
          // setContractId(response.data.data.contract_id);
          // setContractInfo(response.data.data.contract_info);
          setContractBody(
            <BL.Contract
              contractId={response.data.data.contract_id}
              propsContractInfo={response.data.data.contract_info}
              saveClickListner={(contractId, contractType, contractInfo) => {
                ContractApi.postContract(user, contractId, contractType, contractInfo)
                  .then()
                  .catch((e) => console.log(e));
                setSnackbarMessage("Save Bill Of Lading Contract Infomation");
                setOpenSnackbar(true);
              }}
              saveContractListner={(contractId, contractType, contractInfo) => {
                ContractApi.postContractDone(user, contractId, contractType, contractInfo)
                  .then()
                  .catch((e) => console.log(e));
                setSnackbarMessage("Finish Writing Bill Of Lading Contract Infomation");
                setOpenSnackbar(true);
                history.push("/tables");
              }}
            />
          );
        });
      }
    }
  }, []);

  const handleClose = (event, reason) => {
    if (reason === "clickaway") {
      return;
    }
    setOpenSnackbar(false);
  };

  function createCategoryListComponent(options) {
    const keyList = Object.keys(options);
    const componentList = keyList.map((key) => {
      if (contractCategoryMap[key] === 100) {
        return (
          <Grid item xs={12} sm={6} xl={3}>
            <BL.Card
              cardClickListner={() => {
                const contractType = "bill_of_lading";
                setIsCategoryShow(false);
                ContractApi.getDefaultContract(user, contractType).then((response) => {
                  // setContractId(response.data.data.contract_id);
                  response.data.data.contract_info.consignor.name = response.data.data.name;
                  response.data.data.contract_info.consignor.TEL = response.data.data.phone;
                  // setContractInfo(response.data.data.contract_info);
                  setContractBody(
                    <BL.Contract
                      contractId={response.data.data.contract_id}
                      propsContractInfo={response.data.data.contract_info}
                      saveClickListner={(contractId, contractType, contractInfo) => {
                        ContractApi.postContract(user, contractId, contractType, contractInfo)
                          .then()
                          .catch((e) => console.log(e));
                        setSnackbarMessage("Save Bill Of Lading Contract Infomation");
                        setOpenSnackbar(true);
                      }}
                      saveContractListner={(contractId, contractType, contractInfo) => {
                        ContractApi.postContract(user, contractId, contractType, contractInfo)
                          .then()
                          .catch((e) => console.log(e));
                        setSnackbarMessage("Save Bill Of Lading Contract Infomation");
                        setOpenSnackbar(true);
                      }}
                    />
                  );
                });
              }}
            />
          </Grid>
        );
      }
    });
    componentList.push(
      <Grid item xs={12} sm={6} xl={3}>
        <Second.Card
          cardClickListner={() => {
            setIsCategoryShow(false);
            setContractBody(<Second.Contract />);
          }}
        />
      </Grid>
    );
    return (
      <Grid container spacing={3}>
        {componentList}
      </Grid>
    );
  }

  return (
    <DashboardLayout>
      <DashboardNavbar />
      <SuiBox py={3}>
        <SuiBox mb={3}>
          <Card style={{ padding: 10, paddingBottom: 20 }}>
            <div style={{ justifyContent: "space-between", display: "flex" }}>
              <SuiTypography fontWeight="medium" style={{ padding: 10 }}>
                Catalog
              </SuiTypography>
              <IconButton
                style={{ marginRight: 20 }}
                size="large"
                color="dark"
                aria-label="minimize category"
                component="span"
                onClick={() => {
                  setIsCategoryShow(!isCategoryShow);
                }}
              >
                {isCategoryShow ? <ExpandLessIcon /> : <ExpandMoreIcon />}
              </IconButton>
            </div>
            {isCategoryShow ? usableCategoryList : undefined}
          </Card>
        </SuiBox>
        <SuiBox mb={3}>
          <Grid container spacing={3}>
            <Grid item xs={12} lg={12}>
              {contractBody}
            </Grid>
            {/* <Grid item xs={12} lg={5}>
              <WorkWithTheRockets />
            </Grid> */}
          </Grid>
        </SuiBox>
        {/* <SuiBox mb={3}>
          <Grid container spacing={3}>
            <Grid item xs={12} lg={5}>
              <ReportsBarChart
                title="active users"
                description={
                  <>
                    (<strong>+23%</strong>) than last week
                  </>
                }
                chart={chart}
                items={items}
              />
            </Grid>
            <Grid item xs={12} lg={7}>
              <GradientLineChart
                title="Sales Overview"
                description={
                  <SuiBox display="flex" alignItems="center">
                    <SuiBox fontSize={size.lg} color="success" mb={0.3} mr={0.5} lineHeight={0}>
                      <Icon className="font-bold">arrow_upward</Icon>
                    </SuiBox>
                    <SuiTypography variant="button" textColor="text" fontWeight="medium">
                      4% more{" "}
                      <SuiTypography variant="button" textColor="text" fontWeight="regular">
                        in 2021
                      </SuiTypography>
                    </SuiTypography>
                  </SuiBox>
                }
                height="20.25rem"
                chart={gradientLineChartData}
              />
            </Grid>
          </Grid>
        </SuiBox>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6} lg={8}>
            <Projects />
          </Grid>
          <Grid item xs={12} md={6} lg={4}>
            <OrderOverview />
          </Grid>
        </Grid> */}
      </SuiBox>

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
      {/* <Footer /> */}
    </DashboardLayout>
  );
}

export default Dashboard;
