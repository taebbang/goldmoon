// export const API_SERVER = "http://localhost:4242";
const regex = /http[s]{0,1}:\/\//;
export const API_SERVER =
  "http://" + window.location.host.replace(regex, "").split(":")[0] + ":3002";
