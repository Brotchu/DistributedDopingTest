# DistributedDopingTest

## Generic User cases

### Login

### Logout

### Token Validation

### Refresh Token

### update personal info


## Athlete User cases

### insert availabilities

### update availabilities


## ADO User cases

### get availabilities

``` json
// POST https://{BaseUrl}/ado/get-availabilities
// Request Body Example 
{
  "token": "<Token Here>",
  "timestamp": 123456,       // <Unix Timestamp>
  "payload": {
    "filters": [
      {
        "type": "email", // id
        "expect": "yuy4@tcd.ie"
      },
      {
       "type": "zone",
       "expect": [
         "Dublin",
         "GB" 
         // other zones
       ] 
      },
      {
        "type": "date",
        "from": 0,
        "to": -1 // all
      },
      {
        "type": "name",
        "pattern": "<regex here>"
      }
    ]
  }
}
```
