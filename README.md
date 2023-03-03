#  Polygon NFT Market Tracker

#### This is a hackathon Project for ETH Denver 2023 - Prototype up at 45.33.31.186:8000

#### This application allows the user to analyze pricing/volumes for Polygon NFT sales on OpenSea

Every Endpoint has a Simple HTML form which acts as a sort of "endpoint explorer"

Explore the dataset and API at 45.33.31.186:8000

# API

### /get_transactions
  - Returns a list of every Polygon NFT which sold and the sale price, along with some transaction metadata
  - Example GET: Get a list of every NFT tonydeals.eth ever bought on Polygon
  - http://45.33.31.186:8000/get_transactions?contract_address=&token_id=&start_dt=&end_dt=&buyer=0xbc6518d2463e52ce89d5e37f55438e953fa12211&seller=&coin_standard=all&response_type=json
  
  ![Screenshot from 2023-03-03 08-19-32](https://user-images.githubusercontent.com/63479105/222758125-55bbb082-8ca5-4e2c-aee9-ec78a12e44f9.png)


### /get_volume
  - Retuns Polygon NFT aggregate sales statistics for the time-window provided by the user
  - Example GET: Get Sales Summary Between Midnight 2/24 and Midnight 2/25
  - http://45.33.31.186:8000/get_volume?contract_address=&token_id=&start_dt=2023-02-24&end_dt=2023-02-25&buyer=&seller=&coin_standard=all&response_type=json
  
  ![Screenshot from 2023-03-03 08-23-32](https://user-images.githubusercontent.com/63479105/222758967-67a3e031-f110-4b9e-834d-e8da28f62aaf.png)


### /get_daily_sales_volume
  - Retuns Polygon NFT aggregate sales statistics for the time-window provided by the user, grouped by DAY
  - Example GET: Get daily sales stats on the smart contract that rugged me earlier this week
  - http://45.33.31.186:8000/get_daily_sales_volume?contract_address=0x19fbb5e802b58e5fd1b6de259a2f044b478550a4&token_id=&start_dt=&end_dt=2023-02-27&buyer=&seller=&coin_standard=all&response_type=json
  
  ![Screenshot from 2023-03-03 08-27-06](https://user-images.githubusercontent.com/63479105/222759757-bc69ba19-7cf8-4e95-8bbb-351ff8b17b38.png)

  
### /get_weekly_sales_volume
  - Retuns Polygon NFT aggregate sales statistics for the time-window provided by the user, grouped by WEEK
  - Example GET: Get weekly sales summaries for the last few weeks
  - http://45.33.31.186:8000/get_weekly_sales_volume?start_dt=2023-02-20
  
  ![Screenshot from 2023-03-03 08-34-09](https://user-images.githubusercontent.com/63479105/222761414-424affaa-ccf5-4b38-a77f-34c6448e607e.png)


### /get_monthly_sales_volume
  - Retuns Polygon NFT aggregate sales statistics for the time-window provided by the user, grouped by MONTH
  - Example GET: Get monthly sales stats on the Trump NFTS
  - http://45.33.31.186:8000/get_monthly_sales_volume?contract_address=0x24a11e702cd90f034ea44faf1e180c0c654ac5d9&token_id=&start_dt=&end_dt=&buyer=&seller=&coin_standard=all&response_type=json
  
  ![Screenshot from 2023-03-03 08-37-39](https://user-images.githubusercontent.com/63479105/222762189-03b0ebc7-497c-4bfc-b987-e3b2d8dd97f3.png)

  
  
# Parameters For ALL API Endpoints

###  - ?contract_address={SMART_CONTRACT_ADDRESS}
    - String / Address
    - Example: 45.33.31.186:8000/get_transactions?contract_address=0x19fbb5e802b58e5fd1b6de259a2f044b478550a4
###  - ?token_id={NFT_TOKEN_ID}
    - Int
    - Best paired with contract address otherwise you're pulling a random ID from a million contracts
    - Example: 45.33.31.186:8000/get_transactions?contract_address=0x19fbb5e802b58e5fd1b6de259a2f044b478550a4&token_id=747
###  - ?buyer={BUYER_ADDRESS}
    - String / Address
    - Example: 45.33.31.186:8000/get_transactions?buyer=0xbc6518d2463e52ce89d5e37f55438e953fa12211
###  - ?seller={SELLER_ADDRESS}
    - String / Address
    - Example: 45.33.31.186:8000/get_transactions?seller=0x3ebaf00176a77a9ede760dc43f798a9ad2a87c8a
###  - ?start_dt={START_DATE}
    - Date / Date-String
    - Example: 45.33.31.186:8000/get_transactions?start_dt=2023-02-14
###  - ?end_dt={END_DATE}
    - Date / Date-String
    - Example: 45.33.31.186:8000/get_transactions?end_dt=2023-03-14
###  - ?coin_standard={COIN_STANDARD}
    - Choices: ["all", "721", "1155"]
    - Example: 45.33.31.186:8000/get_transactions?coin_standard=1155
###  - ?response_type={RESPONSE_TYPE}
    - Choices: ["json", "html"]
    - Defaults to "json"
 
  
# Frontend Samples

![Screenshot from 2023-03-03 08-49-33](https://user-images.githubusercontent.com/63479105/222765309-5d0fc5fe-677d-4b62-aa77-ef248119cc17.png)


![Screenshot from 2023-03-03 08-46-15](https://user-images.githubusercontent.com/63479105/222765072-28388c7e-08ca-4889-836a-297cb95136cc.png)


