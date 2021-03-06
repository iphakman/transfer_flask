# transfer_flask

### Create transactions

#### Endpoint            Methods    Rule
#### ------------------  ---------  ---------------------------
#### create_transaction  GET, POST  /transaction/<int:id>
#### index               GET        /
#### login               GET, POST  /login
#### logout              GET        /logout
#### show_transaction    GET        /users/<int:id>/transaction
#### user_form           GET, POST  /users
#### users               GET        /users/<int:id>/
#### renew_currencies    GET, POST  /currencies_add
#### get_currencies      GET        /currencies

### We can add users/transactions
### Data stored into postgres db

## create_transaction
#### /transaction/<id>  - id refers to userid.
### Will add transaction: 
#### id: Userid sender
#### email: receiver of transaction
#### amount: amount for the transaction
#### currency: amount's currency

## index
#### /      - index page, will list full user lists.

## login
#### /login     - login to the page.
### Will validate user/password, create_transaction, show_transaction, user_form requires login

## logout
#### /logout    - logout

## show_transaction
#### /users/<int:id>/transaction    - id refers to userid

## user_form
#### /users
### Will add user:
#### name: user name
#### last_name: user last name
#### email: email's user, used as receiver in transactions
#### phone_number: user's phone number
#### msdi: number identifier
#### password: user password

## users
#### /users/<int:id>/transaction    - id refers to userid
### Will list transactions of the user(id)

## get_currencies
#### /currencies
### Will list all currencies available on the database

## renew_currencies
#### /currencies_add
### Will update the rate for each currencies, from google.com (get_currency_date)

## DB MODELS
### users
####  id | name  | last_name | password |        email         |     msdi      | is_admin | phone_number 
### transaction
####  id | user_id | amount |     destination      | currency 

### user_balance
####  id | user_id |  amount  | currency |       last_modified        | transaction_id 

### convertion
####  id | state | currency | symbol | iso_code | fractional_unit | variance 

