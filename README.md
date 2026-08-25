Follow this tutorial to create a project: https://developers.google.com/workspace/calendar/api/quickstart/python \
After that, go to IAM & Admin -> Service Accounts and make a service account with Owner permissions. Then create a new key for the service account \
Upload the service account key credentials as "service_credentials.json" \
Add the service account's email as an editor and manager of the Google Calendar you want to be writing to \
Edit the constants.py file and make the variable "CALENDAR_ID" the Google Calendar ID of the Google Calendar you want to edit

To use the code:
1. If you already have a .json file of a term and year created from this program, skip to the next step. If not, run "py write_class_data.py" and follow the prompts
2. To write the .json file to a Google calendar, run "py write_to_calendar.py". This .json accounts for holidays as well
3. To delete all the classes from a term from a Google calendar, run "py delete_from_calendar.py". This is useful to try refreshing what's in the calendar for a term