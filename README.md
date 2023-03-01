# Seaport Volumes on Polygon 

This is a hackathon Project for ETH Denver 2023

This application lets the user read sales volumes for NFTs on the Polygon Network's Seaport. 

The user can query NFT sales volumes by many parameters:
  - block_number / range of block_numbers
  - buyer
  - seller
  - contract_address
  - (contract_address + token_id)
  - range of dates
  - range of datetimes
  
The application works for ERC721 Tokens and ERC1155 Tokens. 

The api can serve aggregate numbers on sales totals, or it can serve a list of the underlying transactions. 


This is a web2 app for blockchain analytics - It consists of 
1) A Relational Database of Blockchain Data
2) An API to let you read that data
3) Simple HTML pages which let you call that API
