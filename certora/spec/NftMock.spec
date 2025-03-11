/*
 * Verification of NftMock
 */

methods {
    function totalSupply() external returns uint256 envfree;
}

invariant totalSupplyNonNegative()
    totalSupply() >= 0;