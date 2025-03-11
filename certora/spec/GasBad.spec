/*
 * Verification of GasBadNftMarketplace
 */

using GasBadNftMarketplace as gasBad;
using NftMarketplace as nftMarketplace;

methods {
    function getListing(address,uint256) external returns INftMarketplace.Listing envfree;
    function getProceeds(address) external returns uint256 envfree;
    function _.safeTransferFrom(address,address,uint256) external => DISPATCHER(true);
    function _.onERC721Received(address,address,uint256,bytes) external => DISPATCHER(true);
}

ghost mathint listingUpdatesCount {
    init_state axiom listingUpdatesCount == 0;
}
ghost mathint log4Count {
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

rule callingAnyFunctionShouldResultInEachContractHavingTheSameState(method f, method f2) {
    require(f.selector == f2.selector);
    env e;
    calldataarg args;
    address nftAddr;
    uint256 tokenId;
    address seller;

    require(gasBad.getProceeds(e, seller) == nftMarketplace.getProceeds(e, seller));
    require(gasBad.getListing(e, nftAddr, tokenId).price == nftMarketplace.getListing(e, nftAddr, tokenId).price);
    require(gasBad.getListing(e, nftAddr, tokenId).seller == nftMarketplace.getListing(e, nftAddr, tokenId).seller);

    gasBad.f(e, args);
    nftMarketplace.f2(e, args);

    assert(gasBad.getProceeds(e, seller) == nftMarketplace.getProceeds(e, seller));
    assert(gasBad.getListing(e, nftAddr, tokenId).price == nftMarketplace.getListing(e, nftAddr, tokenId).price);
    assert(gasBad.getListing(e, nftAddr, tokenId).seller == nftMarketplace.getListing(e, nftAddr, tokenId).seller);
}