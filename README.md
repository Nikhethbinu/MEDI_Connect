# MediConnect -- Hospital Appointment Booking System

MediConnect is a web-based hospital appointment management application
developed with **Python, Django, and MySQL**. It is designed to organize
interactions between patients, doctors, and administrators, with
separate modules for appointments and related healthcare information.

## Project Overview

The project uses Django's Model--View--Template (MVT) architecture,
Django ORM for database operations, and Django authentication for user
login. The codebase is divided into separate Django apps to keep
responsibilities organized.

## Main Modules

-   **Accounts** -- registration, login, logout, and authentication.
-   **Patients** -- patient-related information and profiles.
-   **Doctors** -- doctor profiles and availability.
-   **Appointments** -- appointment-related operations.
-   **Prescriptions** -- prescription-related information.
-   **Medical Records** -- patient medical-record information.
-   **Billing** -- billing-related information.

The exact functionality available to users depends on the views and
permissions implemented in each module.

## Technology Stack

  Area                          Technology
  ----------------------------- -----------------------
  Backend                       Python, Django
  Frontend                      HTML, CSS, JavaScript
  Database                      MySQL
  Python MySQL driver           PyMySQL
  Version control               Git and GitHub

## Architecture

MediConnect follows Django's MVT pattern:

1.  A user sends a request through the browser.
2.  Django URL configuration routes the request to a view.
3.  The view runs application logic and interacts with models when
    database access is needed.
4.  Django ORM communicates with MySQL.
5.  The view returns a response, commonly by rendering a template.

**Request flow:** Browser → URL → View → Model/Database → View →
Template → Browser

## Database

MySQL is used as the relational database. Django models define the data
structure, and Django ORM provides a Python interface for creating,
retrieving, updating, and deleting records. Database schema changes are
managed through Django migrations.


## Future Improvements

Possible enhancements include:

-   Email or SMS appointment notifications.
-   Online payment integration.
-   Appointment cancellation and rescheduling improvements.
-   Additional reporting and analytics.


## Author

**Nikheth Binu**

GitHub: https://github.com/Nikhethbinu

------------------------------------------------------------------------

For issues or suggestions, feel free to open an issue in the repository.
