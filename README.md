# LEADME

![Language](https://img.shields.io/badge/Language-Python%20-blue)
![Framework](https://img.shields.io/badge/Framework-Flask-lightblue)
![Language](https://img.shields.io/badge/Language-Js-yellow)
![Language](https://img.shields.io/badge/Language-CSS-purple)
![Language](https://img.shields.io/badge/Language-HTML-brown)
![License](https://img.shields.io/badge/License-MIT-green)

- **Author LinkedIn**: [Ortniel ADOUMASSE](https://www.linkedin.com/in/ortniel-adoumasse/).

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

is a web application designed to assist recent high school graduates in Benin in making informed decisions about their university program selections.

In Benin, after obtaining their Baccalaureate, students are required to apply for university programs through an online platform. Each student can select up to three programs of interest. Admission into these programs is then determined based on the student’s academic performance, including their grades and honors achieved in the Baccalaureate exams.

Each program has a limited number of fully funded scholarships and partially funded semi-scholarships. If a student is not selected for either scholarship option, they still have the opportunity to enroll in a program as a self-funded (paying) student.

Given the importance of this process, it is crucial to guide students effectively to minimize errors in their program choices and reduce the likelihood of subsequent dropouts. LeadMe aims to simplify this process by providing a structured and reliable platform to support students in making well-informed decisions about their educational futures.

## Features

- **Personalized Program Recommendations**:  
  Based on the student’s Baccalaureate grades and average scores in each available program, the platform provides a personalized overview of the programs where the student has the highest chances of being accepted.

- **Scholarship Information via Blog Extension**:  
  Through the platform’s integrated blog extension, students can access up-to-date information regarding both local and international scholarships available for their chosen programs, helping them find financial support opportunities.

- **Admin Dashboard for Content Management**:  
  An admin dashboard allows platform administrators to easily manage and update information about available programs, scholarships, and blog content, ensuring the platform remains current and accurate.

## Setup and Installation

### Prerequisites
Ensure you have the following installed on your machine:
- Python 3.x
- Redis installed on your machine
- PostgreSQL install on your machine and a empty database called `leadme`

### Installation Steps
1. Clone the repository:
    ```sh
    git clone https://github.com/adoumasseo/leadMe.git
    ```
2. Navigate to the project directory:
    ```sh
    cd leadMe
    ```
3. Create a virtual environment:
    ```sh
    python3 -m venv .venv
    ```
4. Activate the virtual environment:
    - On Linux/macOS:
        ```sh
        . .venv/bin/activate
        ```
    - On Windows:
        ```sh
        .venv\Scripts\activate
        ```
5. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```
6. Env variable and config
  - Use the .env.example on the project root to create a .env for the app (It's neccessary. If you need help with it just email me.) <br>
  - Make sure to have the `SECRET_KEY`, `DATABASE_URL`, `FLASK_APP` and `FLASK_ENV`.
  - The others Variables are for the email service. You can create your own using `google smtp` service. Or you can also email me if you want mine :) (But make sure to have them if you need to test the functionalities email related)

7. Migrations <br>
Make sure to be at the root of the project with your acticated env. Then run:
  - ```sh flask db upgrade```: to apply the migrations on the database

8. Seeders <br>
  Before seeding the database you might want to modify the seed code a litle bit if you want to acces the admin panel with your informations. <br>
  - Navigate to `app/database/seeds` and open the file `seed_users.py`.
  - You will find something like this in it 
  ```py
  from app.extensions import db
  from app.database.models.user import User
  from app.database.models.university import Universite
  from app.database.models.ecole import Ecole
  from app.database.models.matiere import Matiere
  from app.database.models.filiere import Filiere
  from app.database.models.post import Post
  from app.database.models.serie import Serie
  from app.database.models.associations import MatiereFiliere, Moyenne, Note, Coefficient
  from faker import Faker
  
  fake = Faker()
  
  def seed_users():
      """Function to seed the database with sample users."""
      serie = Serie.query.filter_by(nom='Serie C').first()
      if not serie:
          print("NOT Serie")
          return
      
      users = [
          User(
              prenom="ADMIN",
              nom="ADMIN",
              matricule=None,
              email=fake.email(),
              password=fake.password(),
              serie_id=serie.id_serie,
              role="admin"
          ),
          User(
              prenom="Ortniel",
              nom="ADOUMASSE",
              matricule=None,
              email="adoumasseo@gmail.com",
              password="admin@admin",
              serie_id=serie.id_serie,
              role="admin"
          )
      ]
      db.session.bulk_save_objects(users)
      db.session.commit()
      print("Seeded users table successfully!")
  
  ```
  - Add a new instance of User() to the users array with your informations. A valid and working email address is recommended.
  - Add the end you should have something like this for the array users.
  ```sh
  users = [
      User(
          prenom="ADMIN",
          nom="ADMIN",
          matricule=None,
          email=fake.email(),
          password=fake.password(),
          serie_id=serie.id_serie,
          role="admin"
      ),
      User(
          prenom="Ortniel",
          nom="ADOUMASSE",
          matricule=None,
          email="adoumasseo@gmail.com",
          password="admin@admin",
          serie_id=serie.id_serie,
          role="admin"
      )
      ,
      User(
          prenom="yourFistName",
          nom="yourLastName",
          matricule=None,
          email="yourEmail",
          password="admin@admin",
          serie_id=serie.id_serie,
          role="admin"
      )
  ]
  ```
  - Save the file and go back to the root of the project.
  
  - Then run ```sh flask seed_all```: to add some data to the database.
  
8. Start the development server:
    ```sh
    flask run
    ``` <br>
    and enjoy the app.

### File Directory Structure
```bash
.
├── app
│   ├── controllers
│   │   ├── auth
│   │   │   ├── __init__.py
│   │   │   └── routes.py
│   │   ├── computation
│   │   │   ├── __init__.py
│   │   │   └── routes.py
│   │   ├── dashboard
│   │   │   ├── __init__.py
│   │   │   └── routes.py
│   │   ├── ecole
│   │   │   ├── __init__.py
│   │   │   └── routes.py
│   │   ├── filiere
│   │   │   ├── __init__.py
│   │   │   └── routes.py
│   │   ├── __init__.py
│   │   ├── main
│   │   │   ├── __init__.py
│   │   │   └── routes.py
│   │   ├── matiere
│   │   │   ├── __init__.py
│   │   │   └── routes.py
│   │   ├── post
│   │   │   ├── __init__.py
│   │   │   └── routes.py
│   │   ├── serie
│   │   │   ├── __init__.py
│   │   │   └── routes.py
│   │   └── university
│   │       ├── __init__.py
│   │       └── routes.py
│   ├── database
│   │   ├── __init__.py
│   │   ├── migrations
│   │   │   ├── alembic.ini
│   │   │   ├── env.py
│   │   │   ├── README
│   │   │   ├── script.py.mako
│   │   │   └── versions
│   │   │       └── b71afcd74785_initial_migration.py
│   │   ├── models
│   │   │   ├── associations.py
│   │   │   ├── ecole.py
│   │   │   ├── filiere.py
│   │   │   ├── __init__.py
│   │   │   ├── matiere.py
│   │   │   ├── post.py
│   │   │   ├── serie.py
│   │   │   ├── university.py
│   │   │   └── user.py
│   │   └── seeds
│   │       ├── __init__.py
│   │       ├── seed_ecole.py
│   │       ├── seed_filiere.py
│   │       ├── seed_filiere_serie.py
│   │       ├── seed_matiere_series.py
│   │       ├── seed_matieres_filieres.py
│   │       ├── seed_university.py
│   │       └── seed_users.py
│   ├── extensions.py
│   ├── __init__.py
│   ├── middleware
│   │   └── auth.py
│   ├── static
│   │   ├── css
│   │   ├── fonts
│   │   ├── images
│   │   ├── js
│   │   ├── libs
│   │   ├── pdf
│   │   │   └── orientation_guide.pdf
│   │   └── uploads
│   ├── templates
│   │   ├── auth
│   │   │   └── form
│   │   │       ├── change_password.html
│   │   │       ├── login.html
│   │   │       ├── reset_password.html
│   │   │       ├── reset_password_request.html
│   │   │       └── verify_code.html
│   │   ├── computation
│   │   │   ├── filiere-details.html
│   │   │   ├── user-informations.html
│   │   │   ├── user-marks.html
│   │   │   └── user-result.html
│   │   ├── dashboard
│   │   │   ├── ecole
│   │   │   │   ├── create.html
│   │   │   │   ├── edit.html
│   │   │   │   └── index.html
│   │   │   ├── filiere
│   │   │   │   ├── create.html
│   │   │   │   ├── edit.html
│   │   │   │   └── index.html
│   │   │   ├── index.html
│   │   │   ├── matiere
│   │   │   │   ├── create.html
│   │   │   │   ├── edit.html
│   │   │   │   └── index.html
│   │   │   ├── post
│   │   │   │   ├── create.html
│   │   │   │   ├── edit.html
│   │   │   │   └── index.html
│   │   │   ├── serie
│   │   │   │   ├── create.html
│   │   │   │   ├── edit.html
│   │   │   │   └── index.html
│   │   │   └── university
│   │   │       ├── create.html
│   │   │       ├── edit.html
│   │   │       └── index.html
│   │   ├── email
│   │   │   └── reset_code.html
│   │   ├── landing_page.html
│   │   ├── layouts
│   │   │   ├── base.html
│   │   │   ├── dash_base.html
│   │   │   └── front_nav.html
│   │   ├── pdf
│   │   │   └── computation_result.html
│   │   └── posts.html
│   ├── tests
│   │   └── mail.py
│   └── utils
│       ├── auth.py
│       ├── code.py
│       ├── debug.py
│       └── mail.py
├── config.py
├── dir_tree.md
├── README.md
├── redis_config.py
└── requirements.txt

43 directories, 93 files

```



## Usage

- To Acces the dashbord after the seed you have to click `Administrator Area` At the top of the landing page
- Here are the credentials
  - email: ```adoumasseo@gmail.com``` (Mine incidentally)
  - password: ```admin@admin```
- For the rest you can just discover by yourself :).

## Contributing

We welcome contributions! To get started:

1. Fork the repository.
2. Create a new branch for your feature or bug fix:
    ```sh
    git checkout -b feature-name
    ```
3. Make your changes and commit them:
    ```sh
    git commit -m 'Description of feature or fix'
    ```
4. Push your branch to your forked repository:
    ```sh
    git push origin feature-name
    ```
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE.md](LICENSE.md) file for details.
