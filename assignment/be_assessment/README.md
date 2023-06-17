# Backend Assessment

You can pick either one of the assignment and finish that. Each have their own deadline, and we request you to submit it before that. 

## Assignment 1

## Task
Your task is to create a **_dockerized_** service, **claim_process**  to process claims. 

## Requirements
1. **claim_process** transforms a JSON payload representing a single claim input with multiple lines and stores it into a RDB.
   - An example input (in CSV format) - *claim_1234.csv* is provided. Note that the names are not consistent in capitalization.
2. **claim_process** generates a unique id per claim.
3. **claim_process** computes the *“net fee”* as a result per the formula below.
*“net fee” = “provider fees” + “member coinsurance” + “member copay” - “Allowed fees”* (note again that the names are not consistent in capitalization).
4. A downstream service, **payments**, will consume *“net fee”* computed by **claim_process**.


## Task Instructions
1. You have up to **8 hours** to complete your solution. Mail govind@32health.care a copy/link to your solution.
2. Feel free to make and reasonable assumptions, state them and proceed if anything is unclear.
3. Please use FastApi as your API framework. As noted earlier the solution must be dockerized.
4. Use sqlite as a db and ORM of your choice. Extra points if you use postgres as your db and SQLModel as your ORM and have a docker-compose solution that brings up a db and the web service in one command
5. Please add data validation for *“submitted procedure”* and *“Provider NPI”* columns. *“Submitted procedure”* always begins with the letter ‘D’ and *“Provider NPI”* is always a 10 digit number. The data validation should be flexible to allow for other validation rules as needed. All fields except *”quadrant”* are required.
6. Write pseudo code or comments in your code to indicate how **claim_process** will communicate with **payments**. There are multiple choices here but propose a reasonable solution based on:
   - What needs to be done if there is a failure in either service and steps need to be unwinded.
   - Multiple instances of either service are running concurrently to handle a large volume of claims.

## Evaluation Criteria
1. Clean, documented code and avoidance of anti-patterns
2. Functioning code
3. Presence of Test cases

--

## Assignment 2

## Task
Your task is to create a **_dockerized_** service, **payment_processor**  to process claims. 

## Requirements
1. **payment_processor** consumes a rabbitmq and processes single claim_fee JSON input and stores it into a RDB.
   - An example input (in CSV format) - *claim_fees_1234.csv* is provided. Note that the names are not consistent in capitalization.
2. **payment_processor** generates a unique numerical id per payment record, have this be atleast 16 digits, 1000900080007000
3. **payment_processor** computes the **total_payment** as a result per the formula below.
*“total_payment” = “net fee” + “processing fee” (note again that the names are not consistent in capitalization).
4. **payment_processor** creates a payment record
   - An example file (in CSV format) *payment.csv* has been provided
5. **payment_processor** creates a "payment record line" string value, you can use the example file to look at the format. Also you may have to look at members_1234.csv to find the necessary information
   - An example file has been provided for the format, *payment_record.md*, \t is a tab space
6. **payment_processor** adds this "payment record line" to a NACHA file whose filename will match the service date. For example if a claim_fee with a service date as *3/28/18*, you need to add this "payment record line" to a file named *payments_3_28_18.nacha*, you will have to create this file for every new service date you come across in the file.
7. **payment_processor** need to create an endpoint that allows the user to give a particular service date and then get all the payments that were created for that date. 
8. **payment_processor** has an endpoint that allows me to reverse a payment using the values *claim_id*, *member_id* and *service_date*, the processor has to remove this line from the nacha file

## Task Instructions
1. You have up to **2 days** to complete your solution. Mail govind@32health.care a copy/link to your solution.
2. Feel free to make and reasonable assumptions, state them and proceed if anything is unclear.
3. Please use FastApi as your API framework. As noted earlier the solution must be in a docker container.
4. Use sqlite as a db and ORM of your choice. (Not necessary, but Extra points if you use postgres as your db and SQLModel as your ORM 
5. Use rabbitmq or kafka as your message queue broker
5. Please have a docker-compose solution that brings up the db, kafka queue and the fastapi api in one command)
6. You may have to write a script that reads the input csv *claim_fees_1234.csv* and puts a JSON message into the rabbitmq, so that your **payment_processor* service can consume from the same queue and execute the above mentioned process. 
7. Write comments in your code to indicate how **payment_processor** will communicate with **payments**. There are multiple choices here but propose a reasonable solution based on:
   - What needs to be done if there is a failure in either service and steps need to be unwinded.
   - Multiple instances of either service are running concurrently to handle a large volume of claims.
   (Not necessary but extra points if you actually implement a rudimentary solution that create a payment record in a payments table, with error handling and other stuff built into it)

## Evaluation Criteria
1. Clean, documented code and avoidance of anti-patterns
2. Functioning code
3. Presence of Test cases
