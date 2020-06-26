"""
This package deals with connecting and parsing data from
Google Sheets.
"""
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from .response import Responses, Replies
from typing import Optional

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']


class SheetConnector:
    def __init__(self, secret_json: str, sheet_name: str):
        """
        Constructor
        :param secret_json: str
            Where the JSON file with credentials is
        :param sheet_name: str
            Name of the sheet to connect to
        """
        self.__creds = ServiceAccountCredentials.from_json_keyfile_name(secret_json, scope)
        self.__client = gspread.authorize(self.__creds)
        self._sheet = self.__client.open(sheet_name)

    def get_responses(self, worksheet: str) -> Responses:
        """
        Get the responses available from a worksheet
        :param worksheet: str
            Worksheet to get responses from
        :return: Responses
            Returns a Responses Object with the responses
        """
        worksheet = self._sheet.worksheet(worksheet)
        worksheetData = worksheet.get_all_records()
        repliesList = []
        optionsList = []
        optionDict = {}
        listCount = 0  # Counts how many items we placed in the list
        for lines in worksheetData:  # For each line in worksheet
            # Check if prefix has text is not empty
            if lines["prefix0"]:
                optionsList.append(lines["prefix0"])  # Add to list of options
            else:
                pass  # Pass over line if the prefix0 is blank

            if lines["Response"]:  # If the response isn't blank
                repliesList.append(Replies(lines["Response"], lines["ImageLink"]))  # Place reply in repliesList
                for i in range(5):  # for 5 times
                    i = "prefix{}".format(i)  # create key
                    if lines[i]:  # If key's value isn't empty
                        optionDict[lines[i].title()] = listCount  # Add it to the list of prefixes
                    else:
                        break
                listCount = listCount + 1
        return Responses(optionsList, optionDict, repliesList)

    def get_settings(self, worksheet: str) -> Optional[dict]:
        """
        Get the settings for servers
        :param worksheet: str
            Worksheet to get settings from
        :return: dict
            Dict containing the settings
        """
        worksheet = self._sheet.worksheet(worksheet)
        worksheetData = worksheet.get_all_records()
        returnDict = {}
        for lines in worksheetData:
            tempHolding = {}
            if lines["ServerID"]:
                tempHolding["CaptainRoleID"] = str(lines["CaptainRoleID"])
                tempHolding["BattlefyFieldID"] = lines["BattlefyFieldID"]
                tempHolding["BotChannelID"] = str(lines["BotChannelID"])
                tempHolding["BattlefyTournamentID"] = lines["BattlefyTournamentID"]
                tempHolding["DefaultRoleID"] = lines["DefaultRoleID"]
                tempHolding["BattlefyFCID"] = lines["BattlefyFCID"]
                if lines["AutoAssignCaptainRole"] == "TRUE":
                    tempHolding["AutoAssignCaptainRole"] = True
                else:
                    tempHolding["AutoAssignCaptainRole"] = False
            returnDict[str(lines["ServerID"])] = tempHolding
        return returnDict

    def get_self_assign_roles(self, worksheet: str) -> Optional[dict]:
        """
        Get the assignable roles per server and their IDs
        Get the settings for servers
        :param worksheet: str
            Worksheet to get settings from
        :return: dict
            Dict containing the roles
        """
        worksheet = self._sheet.worksheet(worksheet)
        worksheetData = worksheet.get_all_records()
        returnDict = {}
        for lines in worksheetData:
            tempList = []
            for x in range(16):
                x = "Role{}".format(x)  # create key
                if lines[x]:
                    tempList.append(lines[x].title())
                else:
                    pass
            returnDict[lines["ServerID"]] = tempList
        return returnDict




