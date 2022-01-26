# -*- coding: utf-8 -*-
# encoding: utf-8
from __future__ import print_function

import os.path
import webbrowser
import pyperclip
import time
import codecs

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']


def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v2', credentials=creds)
        previous_question = "Назвіть індустріальні об'єкти, які були побудовані у другій половині 50-х років - на " \
                            "початку 60-х років. "
        while True:
            site_code_file = codecs.open('../site_code.html', 'r', 'utf-8')
            string_file = site_code_file.read()
            REQUIRED_CLASS = "student-session-question-title"
            found_index = string_file.find(REQUIRED_CLASS)
            last_index = 0
            for i in range(len(string_file)):
                if string_file[found_index + len(REQUIRED_CLASS) + 3 + i] == '<':
                    last_index = i + 1
                    break
            site_code_file.close()

            question = string_file[(found_index + len(REQUIRED_CLASS) + 2):(found_index + len(REQUIRED_CLASS) + 2
                                                                            + last_index)]
            if question != previous_question:
                previous_question = question
                pyperclip.copy(question)
                time.sleep(2)
                query = "https://www.google.com/"
                webbrowser.open(query)
                with open('all_questions_illia.txt', 'a') as all_question_file:
                    all_question_file.write(question + '\n')
                all_question_file.close()

                file_id = '1sqjrxQE7PruFH0qp7j8tzWUH6arJylkg'
                new_description = 'descript'
                new_mime_type = 'text/plain'
                new_filename = 'all_questions_illia.txt'
                new_revision = False
                file = service.files().get(fileId=file_id).execute()

                file['title'] = new_filename
                file['description'] = new_description
                file['mimeType'] = new_mime_type

                media_body = MediaFileUpload(
                    new_filename, mimetype=new_mime_type, resumable=True)

                updated_file = service.files().update(
                    fileId=file_id,
                    body=file,
                    newRevision=new_revision,
                    media_body=media_body).execute()

    except HttpError as error:
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()
