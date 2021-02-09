# Radia

> Radia is the mascot of Inkling Performance Labs. As the lead researcher, her duty is to take care of the teams participating in Low Ink as well as to see growth in the teams and individuals taking part in the tournaments.

<!-- Banner -->

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
