pragma solidity >=0.4.22 <0.9.0;

contract ContractAuth {
    // enum type variable to store user gender
    // Actual user object which we will store
    // mapping(string => string) public authTable;
    mapping(uint256 => mapping(uint256 => uint256[2])) public authTable;

    // event signContract(uint256[2] contract_id, uint256[2] contract_auth);

    // user object
    //Internal function to conver genderType enum from string
    function getContractAuthKey(uint256[2] memory contract_id)
        public
        view
        returns (uint256[2] memory)
    {
        return authTable[contract_id[0]][contract_id[1]];
    }

    //Internal function to convert genderType enum to string
    function setContractAuthKey(
        uint256[2] memory contract_id,
        uint256[2] memory contract_auth
    ) public {
        authTable[contract_id[0]][contract_id[1]] = [
            contract_auth[0],
            contract_auth[1]
        ];
        // emit signContract(contract_id, contract_auth);
    }
}
