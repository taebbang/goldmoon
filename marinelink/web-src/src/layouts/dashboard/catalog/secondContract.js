import MiniStatisticsCard from "examples/Cards/StatisticsCards/MiniStatisticsCard";
import ArchiveIcon from "@mui/icons-material/Archive";
import BuildByDevelopers from "layouts/dashboard/components/BuildByDevelopers";

/* eslint-disable react/prop-types */
function Card({ cardClickListner }) {
  return (
    <MiniStatisticsCard
      title={{ text: "2nd" }}
      count="SecondContract"
      icon={{ color: "info", component: <ArchiveIcon /> }}
      backgroundColor="#74BAFF"
      colorThema="dark"
      catalogClickListner={cardClickListner}
    />
  );
}

function Contract() {
  return <BuildByDevelopers />;
}

export { Card, Contract };
