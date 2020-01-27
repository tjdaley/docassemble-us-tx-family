# docassemble-us-tx-family
US Texas Family Law Interviews and Forms

This is a new work with early signs of progress. Don't try to use it for anything yet.

## What Works

### 002.000 - User Profile

*docassemble.us_tx_family:data/questions/TX-002.000-User_Profile.yml*

The user profile interview is working. The first time a user invokes the interview, the user
will be prompted to enter information about the attorney and the law firm. Once the user
reviews and accepts the information, the information will be persisted using DARedis and a
summary screen will be shown.

On subsequent invocations of the interview, the saved user profile will be retrieved from
the persistent store. The user can then edit the information. Once the user is done editing
the information, the user continues the interview, the profile is saved, and a summary
screen is shown.

*Updated: 2020-01-26 by tjdaley*

## What's In Progress

### 003.001 - Case Setup

### 003.002 - Designation of Attorney in Charge / Entry of Appearance

### 009.001 - Guideline Child Support Trial Exhibit
