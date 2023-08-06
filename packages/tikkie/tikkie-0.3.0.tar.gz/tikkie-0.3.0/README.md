Python Tikkie API
=================

An unofficial Python library for communicating with the Tikkie API, made with ❤️ by [New10](https://new10.com/)

Installing
----------

```
pip install tikkie
```

Example
-------

```python
from decimal import Decimal

from tikkie import configure, get_platforms, get_users, create_payment_request

private_key = open('private_rsa.pem', 'rb').read().decode()
configure(api_key='secret', private_key=private_key, platform_token='my-platform-token', sandbox=False)

platform = get_platforms()[0]
user = get_users()[0]

rq = create_payment_request(
    user_token=user.user_token,
    bank_account_token=user.bank_accounts[0].bank_account_token,
    amount=Decimal(0.01),
    currency="EUR",
    description="Test cesar",
    external_id="123456",
    platform_token=platform.platform_token,
)
```
