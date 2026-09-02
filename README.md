## Setup:
### Code install:
1. Click the green "<> Code" dropdown button and select "Download ZIP"

2. Then unzip the download and move the project into a location that you'll remember, preferably not in "Downloads".

### Google Project setup:
1. Make a project using this link: https://console.cloud.google.com/projectcreate \
    Specifying an organization is not necessary. Be sure to name the project something that makes sense.

2. Next use this link to enable the Google Calendar API: https://console.cloud.google.com/flows/enableapi?apiid=calendar-json.googleapis.com \
    If it asks you which project you want to enable the API for, just select the project you just made.

### Service account setup:
1. Once your project is setup, we need to create a service account to read and edit the Google Calendar. \
    You can use this link to get to the service accounts: https://console.cloud.google.com/iam-admin/serviceaccounts \
    The website should ask which project to manage service accounts for, so again, just click the one that you just made.

2. Click the blue text that says "+ Create service account".

3. Again, give the service account a name that makes sense.

4. Press the button that says "Create and continue"

5. When prompted to select a role, click on the dropdown and search for "Owner". \
    Do note that there is a search bar to more easily find different permission levels.

6. Then click the blue "Done" button. If the website says there was an error, just click the "Done" button again.

### Service account key setup:
1. After setting up the service account, it should bring you back to the area where we clicked "+ Create service account". \
    But this time, we want to look at the list that's appeared. \
    In the list, find the service account you just made (by the name of ID works), and click on the 3 dots in that row in the "Actions column"

2. Then click "Manage keys" in the dropdown that's appeared.

3. After that, open up the dropdown menu under the "Add key" button.

4. If you already have a key, press "Upload existing key" and skip to step 6 of this section, otherwise, press "Create new key".

5. If you're creating a new key, select the "JSON" option and then hit "Create". This should download a .json to your computer.

6. Take your key credential .json, rename it to "service_credentials.json", and then move it to the "credentials" folder in this project.

### Google Calendar setup - Classes:
1. This will be the calendar in your Google Calendar that shows when your classes are and sends notifications. \
    So, start by creating a new calendar and naming it something that makes sense. \
    Make sure the time zone of the calendar is correct. \
    You want to make a new calendar since the program can add and delete any number of events in this calendar. \
    So if you put the service account in your main calendar, it could inadvertently delete something you didn't mean to delete.

2. Go back to the service accounts list and copy the email of the service account that you're using for the schedule creation.

3. On the settings for the newly created calendar, go to "Add people and groups" under "Sharing with". \
    Then paste the service account email to add them, and make the permissions of the service account "Make changes and see all event details" using the dropdown menu.

4. Scroll down to "Event notifications" and click "+ Add notification". You can configure this to notify you of a class any number of minutes before a class.

5. Finally, go to the "Integrate calendar" section, which is the second from the bottom. \
    Copy the "Calendar ID" and paste it into the "CLASS_CALENDAR_ID" variable as a string in the constants.py file

### Google Calendar setup - Holidays:
1. This will be the calendar in your Google Calendar that shows when school holidays are. \
    So, start by creating a new calendar and naming it something that makes sense. \
    Make sure the time zone of the calendar is correct. \
    It's less necessary to make another calendar here, since the program will only be able to read from it. \
    But it does make your calendar a bit easier to read with more organization.

2. Go back to the service accounts list and copy the email of the service account that you're using for the schedule creation.

3. On the settings for the newly created calendar, go to "Add people and groups" under "Sharing with". \
    Then paste the service account email to add them, and make the permissions of the service account "See event details" using the dropdown menu.

4. Finally, go to the "Integrate calendar" section, which is the second from the bottom. \
    Copy the "Calendar ID" and paste it into the "VACATION_CALENDAR_ID" variable as a string in the constants.py file

### Python setup:
1. When making this project, I used Python 3.14.2, so do note that other versions could work or could break.

2. Once you have Python installed, pip install all the libraries needed for this project. \
    You can do this by running the "pip install -r requirements.txt" in the terminal.

## Use:
### Getting the .json class schedule (OPTIONAL):
1. Go to https://my.astranova.org/ \
    Make sure to log in with your Astra Nova email

2. Click the button that says "MY ____ ____ SCHEDULE"

3. Then click the hamburger icon to the left of the "X" icon. \
    The hamburger icon is an icon that's 3 horizontal lines stacked vertically

4. Next, click "Export JSON"

5. Move this downloaded .json file into the "official class jsons" folder in the project

### Getting the .ics holiday schedule (OPTIONAL):
1. Go to https://www.astranova.org/calendar

2. Scroll to the bottom of the colored calendar

3. There should be a faint camouflaged button that says "DOWNLOAD CALENDAR (.ICS)"

4. Click it to get the .ics file. The format .ics is a standard format for calendars like Google Calendar and others.

5. Go to your Google Calendar at https://calendar.google.com/

6. Press the plus button next to the text "Other calendars" and press "Import" in the dropdown menu

7. Select the .ics file you just downloaded in the prompt asking for a file. \
    Then select the holiday calendar you just made in the dropdown menu for which calendar to add the events to.

8. Click "Import"

9. Make sure that the events were imported properly. If not, try the importing process again.

### Using the program:
1. Run "py main.py" and start following the prompts. \
    This program will ask you what action you want, so when asked, you can select an option by typing the number next to the option or you can type out the whole option.
    
2. If you already have a .json file of a term and year, for example "fall_2026_2027.json", created from this program, skip to the next step. \
    If not, select the "Write to json" option and follow the prompts. \
    If you have a .json in the "offical class jsons" folder, you can use that for convenience, just make sure it's the most recent version.
    If you don't have a .json, either try to get it for an easier conversion, or you can manually input the class names, class start and end times, term start and end dates, and term name. \
    Try to avoid typing in the times manually if the transition for daylight savings is within a week to make sure that the time conversion is accurate. \
    Somes notes about manually entering values, for time, it must be in a 24-hour format, or a 12-hour format with AM/PM. \
    For dates, input it in the same format as the example given, where the month name is shortened to its first 3 letters. \
    For days, input them as just their first 3 letters, just like with the names of months.

3. To rename a class to a different name, select the "Change class names" option which changes the name of classes in the .json file. \
    This also changes the name that shows up in the calendar

4. To write the .json file to a Google calendar, select the "Write to calendar" action. \
    This uses the .json file from the "Write to json" step and writes it to your calendar

5. To delete all the classes from a term from a Google calendar, select the "Delete from calendar" option. \
    This is useful to try refreshing what's in the calendar for a term or if you made a mistake in the .json creation.

6. To stop the program, select the "Quit" option

### Final notes:
When it asks for the term (Fall/Winter/Spring) and the starting year, the program is figuring out which .json file to use and which holidays to account for. \
Just fill in the term name as well as the year that the school year started to write the right data for that given term and school year. \
As an example for the starting school year, if the school year is from August 2026 to June 2027, the starting year for that school year would be 2026.