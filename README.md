# Radia

> Radia is the mascot of Inkling Performance Labs. As the lead researcher, her duty is to take care of the teams participating in Low Ink as well as to see growth in the teams and individuals taking part in the tournaments.

<!-- Banner -->

## Usage
This is for staff members, for non-staff members, type `!help`.

### Managing tournaments
#### Setting it up
1. First, make sure that the bot has the `ICAL` environment variable set up.
1. Create a calendar event, make sure it's on the calendar that the `ICAL` variable points to.
   - The name of the event will be used to reference the tournament.
   - The date of the event will be used to determine the order in the agenda.
1. Set the description of the event.
   ```
   battlefy: <the battlefy tournament id>
   role: <optionally, you can include a custom captain role id to use, defaults to the Captain role>
   ```
1. The bot will automatically refresh calendar data (along with other data) ever hour, but you can run `!refresh` or `!sync` to see your changes immediately.

#### Using commands
- You can run `!agenda` to get a look at all the scheduled tournaments. The command will also tell you the **index of each tournament**, this is important.
- You can run `!captain` to check the current status of captains. This command does NOT assign roles.

You can append the index of any tournament to these commands / subcommands to specify a specific tournament.
> `!agenda 1`
> `!captain 2`

#### Agenda management
- To get the upcoming tournament, you can run `!agenda next` or `!agenda 0`. This will be the default tournament used by the `!captain` command.
- To get the previous tournament, you can run `!agenda prev` or `!agenda -1`. This can be helpful when removing captains.

You can also use the aliases, `!cal`, or `!calendar` if you so wish.

##### Captain management
Running `!captain` will only check the status of captains, to assign roles, you have to explicitly state that you want roles assigned.

As said before, you can append the index of a tournament to use that tournament instead of the default.

- `!captain assign` Assigns the captain role for the next tournament. This command automatically send a status check after it is complete.
- `!captain remove` Removes the captain role for the next tournament. Be careful, if you're running this command after the tournament has ended, make sure to specify it to use the previous tournament with `!captain assign -1`.
- `!captain check` This is simply an alias for `!captain`.

### Final words
Thanks for reading, I hope this documentation section was helpful to you. If you have any questions, feel free to ask me [@LeptoFlare](https://github.com/LeptoFlare).

## Contributing
1. Fork the repository, do NOT create any branches on the source repository.
1. Make a new branch to submit your pull request from.
1. Submit a pull request to the `master` branch. Please make sure you select "Allow edits from contributors".

### Running locally
#### Prerequisites
1. Make sure you have Docker installed.
1. A Google API project for the bot.

#### Google setup
1. Enable the following API
   - [Google Sheets API](https://console.developers.google.com/apis/api/sheets.googleapis.com)
   - [Google Drive API](https://console.developers.google.com/apis/api/drive.googleapis.com)
1. Go to the [API & Services](https://console.developers.google.com/apis/credentials) and navigate to `credentials` tab
1. Click on `+ create credentials` and create a new `Service Accounts` fill in the necessary field.
   - When you get to **Role** give it `editor`.
1. Download the `credentials` files and rename it `google.json`
1. Share the Google Sheet with the `client_email` from the json file.
1. Copy the gsheet key from the url at `https://docs.google.com/spreadsheets/d/`**`{key}`**`/edit`, you will use this in the `.env`

#### Bot Setup
1. Create a `.env` in the repository root:

   ```py
   TOKEN = discord.bot.token
   GSHEET = gsheet_key
   ICAL = 43cm%40group.calendar.google.com/private-1b6d/basic.ics
   SENTRY = "System Environment"  # Optional
   DEBUG = 1  # Optional
   ```

   Please know that there are no `true` or `false` values in `.env` files. If you want to set a key to false, set it to `0`

1. Run `docker-compose up` in the repository root.
