import axios from "./index";

class AuthApi {
  static Login = (data) => {
    data = {
      id: data.id,
      pwd: data.password,
    };
    return axios.post(`/api/login`, data);
  };

  static Register = (data) => {
    data = {
      id: data.id,
      pwd: data.pwd,
      email: data.email,
      phone: data.phone,
      name: data.name,
    };
    return axios.post(`/api/user`, data);
  };

  static Logout = (data) => {
    data = {
      id: data.id,
    };
    return axios.put(`/api/logout`, data);
  };
}

export default AuthApi;
