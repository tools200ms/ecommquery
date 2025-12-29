import time
from pprint import pprint

from ecommquery.ext.allegro_api.core.requestor import Requestor
from ecommquery.ext.allegro_api.core.session import Session
from ecommquery.ext.allegro_api.lib.constants import PathTo


class Authenticator:
    _device_resp_filter = ("device_code", "user_code",
                    "verification_uri", "verification_uri_complete",
                    "expires_in", "interval")

    _token_resp_filter = ("access_token", "allegro_api", "expires_in",
                          "iss", "jti", "refresh_token", "scope", "token_type")

    def __init__(self,
                 device_code: str, user_code: str,
                 verification_uri: str, verification_uri_complete: str,
                 expires_in: str, interval: str):

        self.device_code = device_code
        self.user_code = user_code
        self.verification_uri = verification_uri
        self.verification_uri_complete = verification_uri_complete
        self.expires_in = int(expires_in)

        interval_value = int(interval)
        if not 1 <= interval_value <= 60:
            raise ValueError(f"Interval must be between 1 and 60 seconds, got {interval_value}")
        self.interval = interval_value

    def printMessage(self):
        print(f"""=======================================================
ACTION REQUIRED: In order to authorize application, please open the 
following URL in a browser:
    🔗 **URL:** {self.verification_uri_complete}
=======================================================""")

    def printDetails(self):
        print(f"""
Authentication Details:
- Device Code: {self.device_code}
- User Code: {self.user_code}
- Verification URI: {self.verification_uri}
- Complete URI: {self.verification_uri_complete}
- Expires in: {self.expires_in} seconds
- Polling interval: {self.interval} seconds
""")

    @classmethod
    def start_device_flow(cls, req: Requestor):
        '''
        First filter response values with filter (for the case if more fields would be returned)
        and then call constructor
        :return:
        '''

        # req.post(Requestor.DEVICE_URL, {"client_id": CLIENT_ID})
        # params = {
        #     "client_id": CLIENT_ID
        # }

        # resp = requests.post(
        #     DEVICE_URL,
        #     headers=headers,
        #     params=params
        # )

        resp = req.post(PathTo.DEVICE, {"client_id": req.client_id})
        resp.raise_for_status()
        resp_data = resp.json()
        result = {k: resp_data[k] for k in cls._device_resp_filter if k in resp_data}

        try:
            return cls(**result)
        except TypeError:
            raise ValueError(f"Error: Required fields missing in the response: {resp.json()}")
        except ValueError:
            raise ValueError(f"Error: Invalid response value: {resp.json()}")

    def poll_for_token(self, req: Requestor):
        """Step 2: Poll the Allegro token endpoint until the user grants access."""
        print(f"\n--- Waiting for User Authorization for {self.expires_in} seconds ---")

        time_begin = time.time()
        expiry_time = time_begin + self.expires_in

        while time.time() < expiry_time:
            # Wait for the specified interval before polling again
            time.sleep(self.interval)

            resp = req.post(PathTo.TOKEN,
                            {"grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                             "device_code": self.device_code})

            # Get response data
            resp_data = resp.json()

            if resp.status_code == 400:
                error_msg = resp_data.get('error_description', 'No error description provided')
                print(f"Error: Request failed with status code {resp.status_code}")
                print(f"Error message: {error_msg}")
                continue
            elif resp.status_code != 200:
                raise Exception(f"Unexpected response status code: {resp.status_code}")

            pprint(resp_data)
            result = {k: resp_data[k] for k in Authenticator._token_resp_filter if k in resp_data}
            result['req'] = req

            return Session(**result)

        print("Authorization timed out.")
        return None
