Follow this tutorial to create a project: https://developers.google.com/workspace/calendar/api/quickstart/python \
After that, go to IAM & Admin -> Service Accounts and make a service account with Owner permissions. Then create a new key for the service account. \
Upload the service account key credentials as "service_credentials.json". \
Add the service account's email as an editor and manager of the Google Calendar you want to be writing to.

Edit the constants.py file and make the variable "CLASS_CALENDAR_ID" the Google Calendar ID of the Google Calendar you want to edit.

And if you have another Google Calendar of the days off, add the service account to that calendar and make the permissions be able to read it. \
You can allow the service account to make changes if you want, but it's not necessary. \
Then edit the variable "VACATION_CALENDAR_ID" to make it the Google Calendar ID of the Calendar with the days off listed.

To use the code:
1. Run "py main.py" and start following the prompts
2. If you already have a .json file of a term and year created from this program, skip to the next step. If not, select the "Write to json" option and continue
3. To write the .json file to a Google calendar, select the "Write to calendar" action. This uses the .json file from before and write it to your calendar
4. To delete all the classes from a term from a Google calendar, select the "Delete from calendar" option. This is useful to try refreshing what's in the calendar for a term
5. To stop the program, select the "Quit" option

When it asks for the term (Fall/Winter/Spring) and the starting year, the program is figuring out which .json file to use and which holidays to account for. \
Just fill in the term name as well as the starting year to write the right data for that given term and school year. \
By starting year, the program is asking for the year that the school year started.