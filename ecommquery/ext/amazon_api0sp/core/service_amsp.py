import json
import pprint
import urllib
from base64 import b64encode

import urllib3

from ecommquery.core.service_management import ManagementService
from ecommquery.ext.amazon_api0sp.core import amsp_constants

class ServiceAmSP(ManagementService):

    def __init__(self, client_id, client_secret_key, verbose: bool, debug: bool, pretend: bool):
        _access_token = "Atzr|IwEBIGG6iI0f6XEQDA25oTf07GoKN8BKCB8ItT2dYsX2O47kjI4tGMvvBia5AGIlbZEbYCKrlIvhsBcYPy6a2isQNTE9n6vrdN2ZNIWKlIdrTwqS8j0rfAChH1h2jKqKnGEVEpSyogeRqxEUbpKBShMSvXPbUaYDzZ0Q5mRwx-FC-EHRv1DepAQYuJC_xSC_YUxWYJT9dUX210m_2SNQ-_rFDhiHG-byZSty3BSaQDlOIO5A0i3nG_Sji7QmWJ1y2r7Dei_spoOywTpp_OHgodguae4frWLyGZvtQnwvnz9S_WEwiSUbGB9VJFeLGMFSQdVHsY7NqAs0Mhx1ZYqif7bsFG_O"
        self._client_id = client_id
        self._client_secret_key = client_secret_key

        http = urllib3.PoolManager()
        grantless_scope = True

        # Prepare your credentials for Basic Auth (Base64 encoded)
        credentials = f"{client_id}:{client_secret_key}".encode("utf-8")
        encoded_credentials = b64encode(credentials).decode("utf-8")

        # Prepare the request data
        payload = {
            "grant_type": "refresh_token",
            "client_id": client_id,
            "client_secret": client_secret_key,
            "scope": "sellingpartnerapi::listings"
        }

        #if grantless_scope:
        #    payload.update({'grant_type': 'client_credentials', 'scope': grantless_scope})
        #else:
        #    payload.update({'grant_type': 'refresh_token', 'refresh_token': self.refresh_token})

        #data = urllib.parse.urlencode(payload)
        #data = urllib3.request.urlencode(payload)
        #headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        # Send the POST request to retrieve the access token
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {encoded_credentials}"
        }

        #pprint.pprint(data)

        #try:
        #    response = http.request('POST', amsp_constants.LWA_ENDPOINT, headers=headers, body=data)
        #    print("Status code:", response.status)
        #    json_response = json.loads(response.data)

        #except Exception as e:
        #    print(str(e))

        #pprint.pprint(json_response)

    def list(self):

        _refresh_token = "Atzr|IwEBIGG6iI0f6XEQDA25oTf07GoKN8BKCB8ItT2dYsX2O47kjI4tGMvvBia5AGIlbZEbYCKrlIvhsBcYPy6a2isQNTE9n6vrdN2ZNIWKlIdrTwqS8j0rfAChH1h2jKqKnGEVEpSyogeRqxEUbpKBShMSvXPbUaYDzZ0Q5mRwx-FC-EHRv1DepAQYuJC_xSC_YUxWYJT9dUX210m_2SNQ-_rFDhiHG-byZSty3BSaQDlOIO5A0i3nG_Sji7QmWJ1y2r7Dei_spoOywTpp_OHgodguae4frWLyGZvtQnwvnz9S_WEwiSUbGB9VJFeLGMFSQdVHsY7NqAs0Mhx1ZYqif7bsFG_O"

        payload = {
            "grant_type": "refresh_token",
            "client_id": self._client_id,
            "client_secret": self._client_secret_key,
            "refresh_token": _refresh_token
        }

        # Use the access token in your request headers
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        http = urllib3.PoolManager()
        # Making a GET request to Amazon SP API
        response = http.request(
            "POST",
            amsp_constants.LWA_ENDPOINT,
            headers = headers,
            body = urllib.parse.urlencode(payload)
        )

        # Handle the response
        if response.status == 200:
            token_data = json.loads(response.data.decode('utf-8'))
            access_token = token_data['access_token']
            print(f"Access Token: {access_token}")
        else:
            print(f"Failed to retrieve token. Status code: {response.status}")
            print(response.data.decode('utf-8'))

    # https://developer-docs.amazon.com/sp-api/docs/listings-items-api-v2021-08-01-reference#getlistingsitem
    # https://developer-docs.amazon.com/sp-api/docs/marketplace-ids
    # MarketPlaceId:
    def list2(self):
        access_token = "Atza|IwEBIBIJf1pVsoFV8w8H-AFj1IAkg57Cpl73lNOQ6ewc3ASvXrsGsSuN-N0VZUbh6MdiZmmkE3jMpI8Etmvv6g5ZctqGKJfmc-5KQY4rD-QyWvWmpFf4VsayzeJhM4P_RkTkqh6037jAtrLHQ4oh7kHbIbN8lltnAMZoAht9PPm6pqF5aTG4dHj7ItioYOPr1MkGKoLe00JlJLwPddGJ7-EIjZBModi3A5lDpQYygRV3c1To1w6NyC682vzhFaBgcw7n1VmFj7J6F0vuBz6Fq-ELFa5Db_YFq-GNUAKX_36Jmi3b7mSHRk3YEr0_OledWAUW80syIQ-Z4wnjHfokeFxF3LfW"
        # SP API endpoint for EU region
        listings_url = "https://sellingpartnerapi-eu.amazon.com/listings/2021-08-01/items"

        # Example query parameters
        marketplace_id = "A1C3SOZRARQ6R3"  # Germany, change as needed
        seller_sku = "3S-MIKQ-225M"

        # Construct the full API URL with query parameters
        api_url = f"{listings_url}?sellerId=Foodieshop24&marketplaceIds={marketplace_id}&sku={seller_sku}"

        # Use the access token in the Authorization header
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "x-amz-access-token": access_token,  # Required for making SP API calls
            "x-amz-target": "com.amazon.spapi.SellingPartnerAPI.Listings"  # Target header for Listings API
        }

        http = urllib3.PoolManager()
        # Send a GET request to list the products
        response = http.request(
            "GET",
            api_url,
            headers=headers
        )

        # Handle the response
        if response.status == 200:
            product_data = json.loads(response.data.decode('utf-8'))
            print(f"Product Listing Data: {json.dumps(product_data, indent=2)}")
        else:
            print(f"Failed to retrieve product data. Status code: {response.status}")
            print(response.data.decode('utf-8'))


