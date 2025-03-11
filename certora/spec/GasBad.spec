/*
 * Verification of GasBadNftMarketplace
 */

persistent ghost mathint listingUpdatesCount {
    init_state axiom listingUpdatesCount == 0;
}
persistent ghost mathint log4Count {
    init_state axiom log4Count == 0;
}

hook Sstore s_listings[KEY address nftAddress][KEY uint256 tokenId].price uint256 price {
    listingUpdatesCount = listingUpdatesCount + 1;
}

hook LOG4(uint offset, uint length, bytes32 t1, bytes32 t2, bytes32 t3, bytes32 t4) {
    log4Count = log4Count + 1;
}

invariant anytimeMappingUpdatedEmitEvent()
    listingUpdatesCount <= log4Count;