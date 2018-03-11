pragma solidity ^0.4.2;

/// @title Verification of Machine Learning Models
contract ModelVerification {

    bool verified;
    uint256 accuracy;
    uint256 accuracy_threshold = 90;

    // set y and pred state variables and evaluate verification criteria
    function verify(int[] y, int[] pred) public {
        uint numerator = 0;
        uint denominator = y.length;
        for (uint i = 0; i < y.length; i++) {
            if (y[i] == pred[i]) {
                numerator += 1.0;
            }
        }
        accuracy = numerator * 100 / denominator;
        verified = accuracy >= accuracy_threshold;
    }

    // get verification report variables
    function get_report() public returns (bool, uint256, uint256) {
        return (verified, accuracy, accuracy_threshold);
    }
}
