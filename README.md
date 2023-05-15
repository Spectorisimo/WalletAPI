# Payment system (Pet-project)
![coverage-93%-green](https://github.com/Spectorisimo/WalletAPI/assets/99352497/8214cafc-345d-4f40-bf1e-e91e5799ae76)
# Description
I developed a RESTful API for a payment system, which implemented the ability to register a user, authenticate with JWT tokens, create electronic wallets with different types of currencies, transactions between user wallets, functionality in the form of charging a monthly commission with each user wallet.
# ER Model
![image](https://github.com/Spectorisimo/WalletAPI/assets/99352497/72b47895-0a6f-4cf6-a7f0-2d01a723b4ec)
# API

### /users/

#### GET
##### Responses

| Code | Description |
| ---- | ----------- |
| 200 |  |

### /users/create/

#### POST
##### Responses

| Code | Description |
| ---- | ----------- |
| 201 |  |

### /users/password/update/

#### POST
##### Responses

| Code | Description |
| ---- | ----------- |
| 201 |  |

### /users/password/verify/

#### PATCH
##### Responses

| Code | Description |
| ---- | ----------- |
| 200 |  |

### /users/token/create/

#### POST
##### Responses

| Code | Description |
| ---- | ----------- |
| 201 |  |

### /users/token/refresh/

#### POST
##### Description:

Takes a refresh type JSON web token and returns an access type JSON web
token if the refresh token is valid.

##### Responses

| Code | Description |
| ---- | ----------- |
| 201 |  |

### /users/update/

#### PATCH
##### Responses

| Code | Description |
| ---- | ----------- |
| 200 |  |

### /users/verify/

#### POST
##### Responses

| Code | Description |
| ---- | ----------- |
| 201 |  |

### /users/wallets/

#### GET
##### Responses

| Code | Description |
| ---- | ----------- |
| 200 |  |

### /users/wallets/create/

#### POST
##### Responses

| Code | Description |
| ---- | ----------- |
| 201 |  |

### /users/wallets/{id}/

#### GET
##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| id | path |  | Yes | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 |  |

### /users/wallets/{id}/deposit/

#### POST
##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| id | path |  | Yes | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 201 |  |

### /users/wallets/{id}/transactions/

#### GET
##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| id | path |  | Yes | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 |  |

### /users/wallets/{id}/transfer/

#### POST
##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| id | path |  | Yes | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 201 |  |

### /users/wallets/{id}/update/

#### PATCH
##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| id | path |  | Yes | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 |  |

### /users/wallets/{id}/withdraw/

#### POST
##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| id | path |  | Yes | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 201 |  |
