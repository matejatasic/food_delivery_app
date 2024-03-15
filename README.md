# Food Delivery App

## Introduction

This is the final project for CS50's Web programming with Python and Javascript. This is a Food Delivery App with the customer and driver part. Initially it was planned to also build the restaurant part, but due the time that it took that build these two parts, it was left as a posibility in the future. This kind of project was selected as a final project because none of the previous course projects is too similiar functionalities (except maybe Network to some extent, which also has the like functionality).

## Distinctiveness and Complexity

The app is not similiar to any of the previous projects, by idea or by complexity. It has much more functionalities, pages, views, models than the previous projects. It also used a lot more of the external packages than the previous projects to provide many of the functionalities.

Regarding the code structure and the technical part in general, there are a lot of things that set this project apart from other projects like:
- the **Service pattern** was implemented to increase readability and maintainability
- **mypy package** was used to enforce type safety
- **settings file** was converted into a module
- **tests** (both unit and integrational) were written, along with [factory boy](https://factoryboy.readthedocs.io/en/stable/) which was used for easier setup of tests and a solid coverage was achieved
- **SSL protocol** is enforced and some other security measures to inrease security of the application
- an integration with the Microsofts [Bing Maps Rest Services](https://learn.microsoft.com/en-us/bingmaps/rest-services/) was done to get the location data based on the address query
- an integration with [Stripe API](https://docs.stripe.com/api) was done to mock payment
- [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/) was used to monitor certain aspects of application and to help speed it up
- a **Vagrantfile** for a virtual machine with provision was written to help start the project easier
- application was optimized to certain extent using **caching** and optimizing database queries at certain places through the use **select_related** and **prefetch_related**

Apart from this the project is different from other projects based on the idea and generally the functionalities, which there are a lot of.

## Files and Directories

The structure of the files and directories is as follows:
- food_delivery_app
    - food_delivey_app - contains the settings, the urls, the logic for type checking and customization of backend
    - customer part
        - management/commands - files used for seeding data to make the demoing of the application easier
        - services - files containing services, which deal with the business logic
        - static - files for styling, Javascript files and initial images
        - templates - html files
        - templatetags - file containing custom template tags
        - tests - unit and integration tests
        - api.py - contains the API views which are called using **fetch** from the Javascript code
        - decorators.py - contains a decorator for adding additional functionality to views
        - dtos.py - containts DTO-s for transferring only the necessary data
        - exceptions.py - custome exceptions and errors
        - forms.py - form classes for easier control of form logic
        - models.py - a few main models and other models which are created to reduce redundancy in main models
        - types.py - custom types
        - urls.py - both template and api view urls
        - views.py - views that return templates
    - static - contains global styling
    - media - contains uploaded images
    - Makefile - contains command for running runserver_plus server
    - requirements.txt - contains the dependencies
    - setup.cfg - contains configuration for mypy package
    - setup.sh - contains shell commands for virtual machine provisioning
- .gitignore - contains files to ignore by git
- Vagrantfile - contains for automatic setup of a virtual machine

## Installation and running

### Step 1 - Install the needed software
Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads) and [Vagrant](https://www.vagrantup.com/downloads.html) to be able to bring up the virtual machine.

### Step 2 - Run Vagrant
To start vagrant, simply type in the command `vagrant up` in your terminal
(if you are running it for the first time type in `vagrant up --provision`).
To access the server, type `vagrant ssh`.

### Step 3 - Start the server
Access the virtual machine by typing in this command: `vagrant ssh`
After that move to the appropriate directory by typing in this command: `cd /vagrant/food_delivery_app`.
After type in `make run` to run the server.

### Step 4 - Accessing the application
To access the application in your browser, type in **food-delivery-app.test:8000** or **192.168.56.10:8000**. You will probably get a warning about invalid certificate, and that's ok, it is because the **mkcert** certificate authority is not trusted by your browser. Just click on proceed to the site button.

### Note:

To be able to access all of the functionalities of the app you will have to do some additional steps. You will have to aqcuire the [Bing Maps Api Key](https://learn.microsoft.com/en-us/bingmaps/getting-started/bing-maps-dev-center-help/getting-a-bing-maps-key) and add it to the **BING_MAPS_API_KEY** variable in the **.env**. You will also have to aqcuire the [Stripe Api Keys](https://docs.stripe.com/keys) and place them in the **STRIPE_API_PUBLIC_KEY** and **STRIPE_API_SECRET_KEY** .env variables respectively. You will also have to create the [Tax rate](https://docs.stripe.com/billing/taxes/tax-rates), copy its ID and paste it into the **TAX_RATE** .env variable. After that you will have all the functionalities.