var ContractAuth = artifacts.require("ContractAuth");
module.exports = function (deployer) {
  deployer.deploy(ContractAuth, "contract");
  // Additional contracts can be deployed here
};
