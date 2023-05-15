# Payment system (Pet-project)
![coverage-93%-green](https://github.com/Spectorisimo/WalletAPI/assets/99352497/8214cafc-345d-4f40-bf1e-e91e5799ae76)
# Description
I've developed an API for an electronic payment system (P2P transfers through users' electronic wallets) that allows users to make payments.
I used JWT tokens for user uthentication, which provides a high level of security and data privacy protection. This allows users to securely use the payment system while protecting their personal data and funds.
In addition, I used a clean architecture to break the code into separate layers and make it easier to read and maintain. This allows you to speed up the development process and ensure easy scalability of the project in the future.
Сelery was used to charge a monthly fee from each wallet.It starts 30 days after wallet creation.
# ER Model
![image](https://github.com/Spectorisimo/WalletAPI/assets/99352497/72b47895-0a6f-4cf6-a7f0-2d01a723b4ec)
# Features
- User registration.
- User authentication and authorization.
- Update information about user.
- Creation of wallets. You can create up to three wallets (One for each type of currency).
- Operations with wallets (deposit, withdrawal, transfer).When transferring funds between wallets with different types of currencies, funds are automatically transferred from the sender's currency to the recipient's currency, the exchange rate is taken from [here](https://www.exchangerate-api.com/).
- Automatic collection of fees from the wallet every month (200 KZT).If there aren't enough funds on the wallet to withdraw the commission, then this wallet will be blocked until the balance of the wallet is replenished with an amount sufficient to withdraw the commission.
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

# Installation
Clone the repository
```
git clone https://github.com/Spectorisimo/WalletAPI.git
```
Create the .env file for handling environment variables
```
SECRET_KEY=YOUR DJANGO SECRET KEY

EMAIL_HOST_USER=YOUR USERNAME FROM SMTP EMAIL
EMAIL_HOST_PASSWORD=YOUR PASSWORD FROM SMTP EMAIL

DB_NAME=YOUR DATABASE NAME
DB_USER=YOUR DATABASE USER
DB_PASSWORD=YOUR DATABASE PASSWORD
```
Run Docker
```
docker compose up
```
Сreate a super user
```
docker compose wallet-project exec python code/manage.py createsuperuser
```
Make migrations
```
docker compose wallet-project exec python code/manage.py makemigrations
docker compose wallet-project exec python code/manage.py migrate
```
