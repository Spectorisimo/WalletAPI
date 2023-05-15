# Payment system (Pet-project)
![coverage-93%-green](https://github.com/Spectorisimo/WalletAPI/assets/99352497/8214cafc-345d-4f40-bf1e-e91e5799ae76)
# Description
I developed a RESTful API for a payment system, which implemented the ability to register a user, authenticate with JWT tokens, create electronic wallets with different types of currencies, transactions between user wallets, functionality in the form of charging a monthly commission with each user wallet.
# ER Model
![image](https://github.com/Spectorisimo/WalletAPI/assets/99352497/72b47895-0a6f-4cf6-a7f0-2d01a723b4ec)
# API

### /users/

#### GET
##### Description:

Get information about user

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Information about user |

### /users/create/

#### POST
##### Description:

Finishes the user creation process

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| data | body |  | Yes | [CreateUser](#CreateUser) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 201 | User successfully created | [CreateUser](#CreateUser) |

### /users/password/update/

#### POST
##### Description:

Finishes the user password update process

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| data | body |  | Yes | [UpdatePassword](#UpdatePassword) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 201 | Password has been successfully updated | [UpdatePassword](#UpdatePassword) |

### /users/password/verify/

#### PATCH
##### Description:

Starts the user password update process

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| data | body |  | Yes | [VerifyUser](#VerifyUser) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | Returns session id and sends verification code | [VerifyUser](#VerifyUser) |

### /users/token/create/

#### POST
##### Description:

Creates an access type JSON web token if user credentials are correct

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| data | body |  | Yes | [CreateToken](#CreateToken) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 201 |  | [CreateToken](#CreateToken) |

### /users/token/refresh/

#### POST
##### Description:

Takes a refresh type JSON web token and returns an access type JSON web
token if the refresh token is valid.

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| data | body |  | Yes | [TokenRefresh](#TokenRefresh) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 201 |  | [TokenRefresh](#TokenRefresh) |

### /users/update/

#### PATCH
##### Description:

Updates information about user

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| data | body |  | Yes | [UpdatePersonalInfo](#UpdatePersonalInfo) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 |  | [UpdatePersonalInfo](#UpdatePersonalInfo) |

### /users/verify/

#### POST
##### Description:

Start the user creation process

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| data | body |  | Yes | [VerifyUser](#VerifyUser) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 201 | Return session id and sends verification code | [VerifyUser](#VerifyUser) |

### /users/wallets/

#### GET
##### Description:

Returns  a list of the user's wallets

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 |  | [ [Wallet](#Wallet) ] |

### /users/wallets/create/

#### POST
##### Description:

Creates user's wallet

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| data | body |  | Yes | [CreateWallet](#CreateWallet) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 201 |  | [CreateWallet](#CreateWallet) |

### /users/wallets/{id}/

#### GET
##### Description:

Returns specific user's wallet

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| id | path |  | Yes | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 |  | [Wallet](#Wallet) |

### /users/wallets/{id}/deposit/

#### POST
##### Description:

Replenishes the balance of the wallet

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| id | path |  | Yes | string |
| data | body |  | Yes | [WalletDepositWithdraw](#WalletDepositWithdraw) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 201 |  | [WalletDepositWithdraw](#WalletDepositWithdraw) |

### /users/wallets/{id}/transactions/

#### GET
##### Description:

Returns a list of transactions for a particular wallet

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
##### Description:

Transfers funds between user wallets

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| id | path |  | Yes | string |
| data | body |  | Yes | [WalletTransfer](#WalletTransfer) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 201 |  | [WalletTransfer](#WalletTransfer) |

### /users/wallets/{id}/update/

#### PATCH
##### Description:

Updates information about user's wallet

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| id | path |  | Yes | string |
| data | body |  | Yes | [UpdateWallet](#UpdateWallet) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 |  | [UpdateWallet](#UpdateWallet) |

### /users/wallets/{id}/withdraw/

#### POST
##### Description:

Withdrawal of funds from the user's wallet

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| id | path |  | Yes | string |
| data | body |  | Yes | [WalletDepositWithdraw](#WalletDepositWithdraw) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 201 |  | [WalletDepositWithdraw](#WalletDepositWithdraw) |

### Models


#### CreateUser

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| email | string (email) |  | Yes |
| phone_number | string |  | Yes |
| password | string |  | Yes |

#### UpdatePassword

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| password | string |  | Yes |
| new_password | string |  | Yes |

#### VerifyUser

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| session_id | string (uuid) |  | Yes |
| code | string |  | Yes |

#### CreateToken

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| phone_number | string |  | Yes |
| password | string |  | Yes |

#### TokenRefresh

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| refresh | string |  | Yes |
| access | string |  | No |

#### UpdatePersonalInfo

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| profile_image | string (uri) |  | No |
| first_name | string |  | No |
| last_name | string |  | No |

#### Wallet

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| id | integer |  | No |
| wallet_number | string |  | No |
| name | string |  | No |
| amount | string (decimal) |  | No |
| amount_currency | string |  | No |
| is_active | boolean |  | No |
| created_at | dateTime |  | No |
| updated_at | dateTime |  | No |
| user | string (uuid) |  | Yes |

#### CreateWallet

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| name | string |  | No |
| amount_currency | string |  | No |

#### WalletDepositWithdraw

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| amount | string (decimal) |  | Yes |

#### WalletTransfer

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| wallet_number | string |  | Yes |
| amount | string (decimal) |  | Yes |

#### UpdateWallet

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| name | string |  | No |
