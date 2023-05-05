# toast_auth

Implements the `ToastToken` class, which is used to authenticate with the Toast API.

`ToastToken` needs a token_location, either a path to a file or 's3', and will do the majority of the work for authenticating the Toast API.

The following environment variables are required:
From Toast:  
- TOAST_API_SERVER
- TOAST_CLIENT_ID
- TOAST_CLIENT_SECRET

For token JSON storage:
If stored locally:
- FILE_NAME

If stored in s3:
- BUCKET_NAME
- FILE_NAME

## Installation

```
pip install toast_auth
```

## Use

### Token stored in AWS s3
```
toast_token = ToastToken(token_location='s3')
```

### Token stored locally
```
toast_token = ToastToken(token_location='local')
```

### Authenticating with Toast API
Get orders: see documentation [here](https://doc.toasttab.com/openapi/orders/operation/ordersBulkGet/)
```
query = {
    "startDate": start,
    "endDate": end,
    "page": str(page),
    "pageSize": "100",
}
headers = {
    **toast_token,
    "Toast-Restaurant-External-ID": location_guid,
}

response = requests.get(orders_url, headers=headers, params=query).json()
```