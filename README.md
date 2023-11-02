# MiPedicenter App

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Technology](#technology)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [User Roles](#user-roles)
- [Authors](#authors)
- [License](#license)

## Introduction

MiPedicenter is a streamlined appointment management and point-of-sale application tailored for podiatry clinics. Built with Python and Flask, and backed by a MySQL database, it offers a suite of interactive tools for scheduling appointments, managing patient and podiatrist data, and handling product sales and inventory.

## Features

- **Interactive Calendar:** Schedule and manage appointments efficiently.
- **Patient and Podiatrist Management:** Assign appointments to patients and podiatrists.
- **Product Sales and Inventory Tracking:** Handle transactions and track stock levels.
- **Supplier Records:** Maintain a database of suppliers and manage orders.
- **Multi-Role Support:** Differentiated access for Admin, Podiatrist, and Receptionist roles.

## Technology

- [Python](https://www.python.org/) - The programming language used.
- [Flask](https://flask.palletsprojects.com/) - The web framework utilized.
- [MySQL](https://www.mysql.com/) - Database for storing all application data.

## Getting Started

These instructions will help you set up a copy of MiPedicenter on your local machine.

### Prerequisites

You need to have Python and MySQL installed on your system. You also need to install Flask if it's not already installed.

```
pip install Flask
```

### Installation

Clone the repository to your local machine:

```
git clone https://github.com/JuanArano17/MiPedicenter.git
```

Navigate to the project directory and install the required packages:

```
cd MiPedicenter
pip install -r requirements.txt
```

Set up the MySQL database by running the provided scripts.

Start the Flask application:

```
flask run
```

## Usage

After installation, you can start using MiPedicenter to:

- Schedule new appointments.
- Assign appointments to available podiatrists.
- Manage product sales and inventory.
- Record transactions with suppliers.

## User Roles

- **Admin:** Responsible for account creation and overall management.
- **Podiatrist:** Can confirm or cancel scheduled appointments.
- **Receptionist:** Manages appointments, sales, and stock entries.

## Authors

- **Juan Pablo Arano** - *Designer, Programmer & Tester* - [Juan Pablo Arano](https://github.com/JuanArano17)
- **Sofia Alejandra Prieto** - *Designer & Tester* - [Sofia Aleandra Prieto](https://github.com/sofipp)
  
See also the list of [contributors](https://github.com/JuanArano17/MiPedicenter/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
