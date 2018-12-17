# IRepoter [![Build Status](https://travis-ci.org/Amoswachira/IRepoterv2.svg?branch=develop)](https://travis-ci.org/Amoswachira/IRepoterv2) [![codecov](https://codecov.io/gh/Amoswachira/IRepoterv2/branch/develop/graph/badge.svg)](https://codecov.io/gh/Amoswachira/IRepoterv2) [![Maintainability](https://api.codeclimate.com/v1/badges/0eb0eb7c71f70e024eca/maintainability)](https://codeclimate.com/github/Amoswachira/IRepoterv2/maintainability)
Corruption is a huge bane to Africa’s development. African countries must develop novel and localised solutions that will curb this menace, hence the birth of iReporter. iReporter enables any/every citizen to bring any form of corruption to the notice of appropriate authorities and the general public. Users can also report on things that needs government intervention



### MAIN FEATURES
- user can Register and create an account
- users can login
- Users can create a red-flag record (An incident linked to corruption).
- Users can create intervention record (a call for a government agency to intervene e.g repair bad road sections, collapsed bridges, flooding e.t.c).
- Users can edit their red-flag or intervention records.
- Users can delete their red-flag or intervention records.
- Users can add geolocation (Lat Long Coordinates) to their red-flag or intervention records.
- Users can change the geolocation (Lat Long Coordinates) attached to their red-flag or intervention records.
- Admin can change the status of a record to either under investigation, rejected (in the event of a false claim) or resolved (in the event that the claim has been investigated and resolved).
- Users can add images to their red-flag or intervention records, to support their claims.
- Users can add videos to their red-flag or intervention records, to support their claims.
- The application should display a Google Map with Marker showing the red-flag or intervention location.

### Postman link
>https://documenter.getpostman.com/view/3870907/RzfmE6Wc
### Heroku Link
>https://irepoterv2final.herokuapp.com/

## Installation and Deployment.

### Clone the repo
 > git clone https://github.com/Amoswachira/IRepoterv2.git

### Setup environment

#### create a virtual environment and activate it asap
>cd IRepoterv2
>virtualenv env

### Activate your virtualenv:

on Windows, virtualenv creates a batch file
>cd env
>\env\Scripts\activate.bat

#### Install all the dependencies using the command
> pip install - r Requirements.txt

#### How to Run the App
> ```.env
> flask run


## Endpoints to test

| Method | Endpoint                                    | Description                                    |
| ------ | ------------------------------------------- | ---------------------------------------------- |
| POST   | /api/v2/interventions                           | Create intervention records                      |
| GET    | /api/v2/interventions                           |get all interventions                    |
| GET    | /api/v2/intervention/9             | Fetch a specific interventions              |
| PATCH  | /api/v2/interventions/8/location    | Edit the location of a specific record.        |
| PATCH  | /api/v2/interventions/8/comment     | Edit the comment of a specific record.         |
| DELETE | /api/v2/intervention/99             | Delete a specific red flag record.             |
| POST | api/v2/auth/signup             | Registration of new users             |
| POST | api/v2/auth/login             | login in users             |
| PATCH | /api/v2/interventions/9/status             | patch Intervention type status.             |
| PATCH | /api/v2/redflag/6/status            | patch redflag status-red             |

