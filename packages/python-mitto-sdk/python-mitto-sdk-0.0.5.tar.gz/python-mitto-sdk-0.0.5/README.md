# python-mitto-sdk
Python Mitto SDK

## Overview:

Python library to interact with Mitto's API.

## Installation:
```python
pip install python-mitto-sdk
```

## Usage:
```python
# What's my Mitto version?
from mitto_sdk import Mitto

BASE_URL = "https://{mitto_url}"
API_KEY = ""

mitto = Mitto(
        base_url=BASE_URL,
        api_key=API_KEY
    )

about = mitto.get_about()
version = about["version"]
print(version)
```
