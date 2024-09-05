# MakersBnB Project

## Overview

The MakersBnB project was a collaborative assignment undertaken as part of the Software Engineering course at Makers. This project involved a team of six, including myself, working together over the span of one week to develop a fully functional booking platform. The project aimed to simulate a real-world software development environment, where team collaboration, technical skills, and time management were crucial.

## Project Description

This repository contains the codebase for the MakersBnB application, developed using Python with the Flask framework. The project encompasses several key components:

- **Wireframe and Design**: Created to outline the user interface and user experience of the application.
- **Database Schema**: Designed to support the functionalities of the booking platform, including user management and reservation handling.
- **Application Code**: Developed using Flask for the backend, with Python as the primary programming language.
- **Frontend**: HTML and CSS were used to build the user interface.
- **Testing**: Unit and integration tests were implemented to ensure the reliability and functionality of the application.

## Team Collaboration

The project was a team effort, and collaboration was key to its success. We utilized GitHub for version control and managed our development process by forking the seed repository, cloning it to our local machines, and contributing to the codebase. Each team member played a specific role, contributing to various aspects of the project, from coding to testing.

## Key Learnings

- **Team Dynamics**: Gained experience in working effectively within a team, managing responsibilities, and coordinating efforts to achieve a common goal.
- **Full-Stack Development**: Developed skills in both frontend and backend development, integrating various technologies to build a cohesive application.
- **Project Management**: Learned to manage time efficiently and prioritize tasks to meet project deadlines.

## Challenges

- **Coordination and Communication**: Ensuring effective communication and coordination among team members was a challenge, but we overcame this by regular meetings and updates.
- **Integration**: Integrating different components of the project required careful planning and testing to ensure all parts worked seamlessly together.

This repository showcases the collaborative effort and technical skills applied to develop a comprehensive booking platform. It reflects our ability to work as a team, tackle complex problems, and deliver a functional application within a tight timeframe.


## Setup

```shell
# Install dependencies and set up the virtual environment
; pipenv install

# Activate the virtual environment
; pipenv shell

# Install the virtual browser we will use for testing
; playwright install
# If you have problems with the above, contact your coach

# Create a test and development database
; createdb YOUR_PROJECT_NAME
; createdb YOUR_PROJECT_NAME_TEST

# Open lib/database_connection.py and change the database names
; open lib/database_connection.py

# Run the tests (with extra logging)
; pytest -sv

# Run the app
; python app.py

# Now visit http://localhost:5000/index in your browser
```
