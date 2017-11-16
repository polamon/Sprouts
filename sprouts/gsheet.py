# -*- coding: utf-8 -*-

from __future__ import print_function
import argparse
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'sprouts'

def get_credentials():
    """
    Gets user credentials from storage or obtain new credentials.
    """
    home_dir = os.path.expanduser('~')
    credentials_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credentials_dir):
        os.makedirs(credentials_dir)
    credentials_path = os.path.join(credentials_dir, 'sprouts.json')

    store = Storage(credentials_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        flags = tools.argparser.parse_args(args=[])
        credentials = tools.run_flow(flow, store, flags)
    return credentials

def write_to_gsheet(gsheet_id, schema, values):
    """
    Write posts to Google Sheets.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http = http,
                              discoveryServiceUrl = discoveryUrl,
                              cache_discovery = False)

    # 1. write first row(schema)
    rangeName = 'A1:' + chr(ord('A') + len(schema) - 1)
    body = {'values': [schema]}
    service.spreadsheets().values().update(
        spreadsheetId = gsheet_id,
        range = rangeName,
        valueInputOption = 'USER_ENTERED',
        body = body).execute()

    rangeName = 'A2:' + chr(ord('A') + len(schema) - 1)
    body = {'values': values}
    service.spreadsheets().values().update(
        spreadsheetId = gsheet_id,
        range = rangeName,
        valueInputOption = 'USER_ENTERED',
        body = body).execute()
