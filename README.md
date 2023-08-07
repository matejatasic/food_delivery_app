# Overview
This is a Bank management system console app with some basic customer functionalities written in C++. At first it was planned to be written in C, but after considering the complexity of the application it was decided to be rewritten in C. Admin and teller part of the application were also planned to be built, but after estimating the complexity of adding those parts, it was decided to create only the basic customer functionalities, but those parts may be added in the future. In regards to that solid principles and repository pattern were implemented to some extent to make it easier to extend the current code.

# Basic functionalities
1. Account information
2. Money depositing
3. Money withdrawing
4. Transaction details

# Project structure
The main file is in the root folder and is named bank-management-system. Apart from the main file is the sql file with the queries for creating tables. Next to it is the sqlite database file that is used to store the data. In the root folder the Make file is also present which make it easier to compile the code. In the errors folder the header file for errors is present. These errors are used in repositories and services to customise the error messages. In the repositories folder the repositories for accounts and transactions are present to make the contact with the database easier. In the services folder the services classes are present which contain the business logic and which are used in the main file. In the models folder the model classes are present which are used for easier organising of data that is retrieved in the repositories from the database and make it easier to reuse that data. It was first planned for this project to be built using the Clean Architecture to the planned complexity(more customer functionalities and admin and teller part) but was left half finished because the idea of a full blown application was possibly left for the future.

# Usage
1. Download the project
2. In the project folder run `make`
3. After that run the executable using the `./bank-management-system` command

**Note:** you will have to create the tables(using the SQL queries from the _bank-management-system.sql_ file) and populate the accounts table with the needed data for this app to work. The pin column in accounts table will have to be populated with the hash of a pin.

## About CS50
CS50 is a openware course from Havard University and taught by David J. Malan

Introduction to the intellectual enterprises of computer science and the art of programming. This course teaches students how to think algorithmically and solve problems efficiently. Topics include abstraction, algorithms, data structures, encapsulation, resource management, security, and software engineering. Languages include C, Python, and SQL plus students’ choice of: HTML, CSS, and JavaScript (for web development).

- Where do I get CS50 course?
https://cs50.harvard.edu/x/2020/