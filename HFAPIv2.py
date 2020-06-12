
####################
#
# Written by Lrrr
# Basic HFAPIv2 Python Wrapper
# Please fork and request merges!
#
####################

import random
import string
import requests
import json

class HF_API:
    "A python wrapper for the HackForums.net API v2"

    client_id = None
    secret_key = None
    access_token = None
    uid = None
    errors = None
    state = None

    base_url = "https://hackforums.net/api/v2"

    def __init__(self, state=None):
        self.state = self.change_state(state)

    def change_state(self, state):
        if state:
            self.set_state(state)
            return
        self.set_state(''.join(
                random.choices(
                    string.ascii_uppercase + string.digits,
                    k=12
                ))
        )

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_client_id(self, client_id):
        self.client_id = client_id

    def set_secret_key(self, secret_key):
        self.secret_key = secret_key

    def set_access_token(self, access_token):
        self.access_token = access_token

    def write_post(self, tid=None, body=None):
        if tid and body:
            return self.action("write",
                {"posts": {
                    "_tid": tid,
                    "_message": body
                }}
            )
        raise Exception("Required fields are missing")

    def app_vault_deposit(self, amount=None):
        if amount and amount >= 100:
            return self.action("write",
                { "bytes": {
                    "_deposit": amount
                }}
            )
        raise Exception("Amount must be >= 100")

    def app_vault_withdraw(self, amount=None):
        if amount and amount >= 100:
            return self.action("write",
                { "bytes": {
                    "_withdraw": tid
                }}
            )
        raise Exception("Amount must be >= 100")

    def donate_bytes(self, uid=None, amount=None, reason=None, pid=None):
        if uid and amount:
            return self.action("write",
                { "bytes": {
                    "_uid": uid,
                    "_amount": amount,
                    "_reason": reason,
                    "_pid": pid
                }}
            )
        raise Exception("Required fields are missing")

    def make_contract(self, uid=None, their_product=None, their_currency=None,
                    their_amount=None, your_product=None, your_currency=None,
                    your_amount=None, tid=None, muid=None, timeout=7,
                    position=None, terms=None, public=None, address=None
                ):

        positions = ["buying","selling","trading","exchanging","vouchcopy"]
        asks = {
            "bytes": {
                "_action": "new",
                "_uid": uid,
                "_theirproduct": their_product,
                "_theircurrency": their_currency,
                "_theiramount": their_amount,
                "_yourproduct": your_product,
                "_yourcurrency": your_currency,
                "_youramount": your_amount,
                "_tid": tid,
                "_muid": muid,
                "_timeout": timeout,
                "_terms": terms,
                "_address": address
            }
        }

        if public:
            asks.bytes["_public"] = "yes"
        if position in positions:
            asks.bytes["_position"] = position

        if uid and position and amount:
            return self.action("write", asks)

        return Exception("Missing required field[s]")


    def gen_auth_url(self,state=None):
        if self.client_id:
            _auth_url = [
                f"{self.base_url}/authorize?response_type=code",
                f"&client_id={self.client_id}&state={state}"
            ]
            return ''.join(_auth_url)
        raise Exception("client_id missing")

    def action(self,method,asks):
        if self.access_token and method in ('read','write') and asks:
            resp = requests.post(
                f"{self.base_url}/{method}",
                data = {'asks':json.dumps(asks)},
                headers = {"Authorization": f"Bearer {self.access_token}"}
            )
            # using the built-in requests.json() method will result in issues
            # converting the dictionary back into a json string.
            if resp:
                return json.loads(resp.text)
            raise Exception("Invalid action response")
        raise Exception("invalid access_token or action method")
