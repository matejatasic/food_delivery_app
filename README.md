# Overview
This is a Bank management system console app with some basic customer functionalities written in C++. Sqlite was used as a database. At first it was planned to be written in C, but after considering the complexity of the application it was decided to be rewritten in C. Admin and teller part of the application were also planned to be built, but after estimating the complexity of adding those parts, it was decided to create only the basic customer functionalities, but those parts may be added in the future. In regards to that solid principles and repository pattern were implemented to some extent to make it easier to extend the current code.

# Basic functionalities
1. Account information
2. Money depositing
3. Money withdrawing
4. Transaction details

# Usage
1. Download the project
2. In the project folder run `make`
3. After that run the executable using the `./bank-management-system` command

**Note:** you will have to create the tables(using the SQL queries from the _bank-management-system.sql_ file) and populate the accounts table with the needed data for this app to work. The pin column in accounts table will have to be populated with the hash of a pin.

