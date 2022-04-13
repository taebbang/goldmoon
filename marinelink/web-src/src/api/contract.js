import axios from "./index";

class ContractApi {
  static getUsableList = (user_info) => {
    let config = {
      headers: { ...axios.defaults.headers, Authorization: "Bearer " + user_info.token },
    };
    return axios.get(`/api/contract/usable`, config);
  };
  static getContractList = (user_info) => {
    let config = {
      headers: { ...axios.defaults.headers, Authorization: "Bearer " + user_info.token },
    };
    return axios.get(`/api/contract`, config);
  };

  static getDefaultContract = (user_info, contract_type) => {
    let config = {
      headers: { ...axios.defaults.headers, Authorization: "Bearer " + user_info.token },
    };
    return axios.get(`/api/contract/info/default/${contract_type}`, config);
  };

  static getContractInfo = (user_info, contract_id) => {
    let config = {
      headers: { ...axios.defaults.headers, Authorization: "Bearer " + user_info.token },
    };
    return axios.get(`/api/contract/info/${contract_id}`, config);
  };

  static getContractSignStatus = (user_info, contract_id) => {
    let config = {
      headers: { ...axios.defaults.headers, Authorization: "Bearer " + user_info.token },
    };
    return axios.get(`/api/contract/sign/${contract_id}`, config);
  };

  static postContract = (user_info, contract_id, contract_type, contract_info) => {
    console.log(user_info, contract_id, contract_type, contract_info);
    let config = {
      headers: { ...axios.defaults.headers, Authorization: "Bearer " + user_info.token },
    };
    let data = {
      type: contract_type,
      id: contract_id,
      info: contract_info,
    };
    return axios.post(`/api/contract/info`, data, config);
  };

  static postContractDone = (user_info, contract_id, contract_type, contract_info) => {
    let config = {
      headers: { ...axios.defaults.headers, Authorization: "Bearer " + user_info.token },
    };
    let data = {
      type: contract_type,
      id: contract_id,
      info: contract_info,
    };
    return axios.post(`/api/contract/info/done`, data, config);
  };

  static runContract = (user_info, contract_id) => {
    let config = {
      headers: { ...axios.defaults.headers, Authorization: "Bearer " + user_info.token },
    };
    let data = {
      contract_id: contract_id,
    };
    console.log(data);
    console.log(user_info);
    return axios.post(`/api/contract`, data, config);
  };
}

export default ContractApi;
