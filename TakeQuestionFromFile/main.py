# with open('../token_immediate_sender.txt') as token_file:
#     TOKEN = token_file.read()
#
# token_file.close()

# with open('../site_code.html') as site_code_file:
#     string_file = site_code_file.read()
#     REQUIRED_CLASS = "student-session-question-title"
#     found_index = string_file.find(REQUIRED_CLASS)
#     last_index = 0
#     for i in range(len(string_file)):
#         if string_file[found_index + len(REQUIRED_CLASS) + 3 + i] == '<':
#             last_index = i + 1
#             break
#     site_code_file.close()
#
# question = string_file[(found_index + len(REQUIRED_CLASS) + 2):(found_index + len(REQUIRED_CLASS) + 2 + last_index)]
# print(question)

# -*- coding: utf-8 -*-
# encoding: utf-8
from __future__ import print_function

import io
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

# If modifying these scopes, delete the file token.json.
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v2', credentials=creds)

        # Call the Drive v3 API
        # results = service.files().list(
        #     pageSize=10, fields="nextPageToken, files(id, name)").execute()
        # items = results.get('files', [])
        #
        # if not items:
        #     print('No files found.')
        #     return
        # print('Files:')
        # for item in items:
        #     print(u'{0} ({1})'.format(item['name'], item['id']))

        previous_question = "Назвіть індустріальні об'єкти, які були побудовані у другій половині 50-х років - на " \
                            "початку 60-х років. "
        while True:
            # with open('../site_code.html') as site_code_file:
            #     string_file = site_code_file.read()
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
                new_title = 'hello.txt'
                new_description = 'descript'
                new_mime_type = 'text/plain'
                new_filename = 'all_questions_illia.txt'
                new_revision = False
                file = service.files().get(fileId=file_id).execute()

                # File's new metadata.
                file['title'] = new_filename
                file['description'] = new_description
                file['mimeType'] = new_mime_type

                # File's new content.
                media_body = MediaFileUpload(
                    new_filename, mimetype=new_mime_type, resumable=True)

                # Send the request to the API.
                updated_file = service.files().update(
                    fileId=file_id,
                    body=file,
                    newRevision=new_revision,
                    media_body=media_body).execute()

                # with open('../previous_questions_illia.txt', 'r') as previous_questions_file:
                #     previous_file_id = previous_questions_file.read()
                #     service.files().delete(fileId=previous_file_id).execute()
                #
                # previous_questions_file.close()

                # file_metadata = {'name': 'all_questions_illia.txt'}
                # media = MediaFileUpload('all_questions_illia.txt', mimetype='text/plain')
                # file = service.files().create(body=file_metadata,
                #                               media_body=media,
                #                               fields='id').execute()
                # print('File ID: %s' % file.get('id'))



                # media_body = MediaFileUpload('all_questions_illia.txt', mimetype='text/plain', resumable=True)
                # body = {
                #     'title': 'all_questions_illia.txt',
                #     'description': "desc",
                #     'mimeType': 'text/plain'
                # }
                # file = service.files().insert(
                #     body=body,
                #     media_body=media_body).execute()




                # with open('../previous_questions_illia.txt', 'w') as previous_questions_file:
                #     previous_questions_file.write(file.get('id'))
                #
                # previous_questions_file.close()
                # with open('../previous_questions_illia.txt', 'r') as previous_questions_file:
                #     previous_file_id = previous_questions_file.read()
                #     service.files().delete(fileId=previous_file_id).execute()
                #
                # previous_questions_file.close()



# rubbish
                # with open('../previous_id_file_drive_illia.txt', 'r') as previous_questions_file:
                #     previous_file_id = previous_questions_file.read()
                #     service.files().delete(fileId=previous_file_id).execute()
                #
                # previous_questions_file.close()

                # file_metadata = {'name': 'previous_questions_illia.txt'}
                # media = MediaFileUpload('../previous_questions_illia.txt', mimetype='text/plain')
                # file = service.files().create(body=file_metadata,
                #                               media_body=media,
                #                               fields='id').execute()
                # print('File ID: %s' % file.get('id'))
                # with open('../previous_id_file_drive_illia.txt', 'w') as previous_id:
                #     previous_id.write(file.get('id'))
                #
                # previous_id.close()






                # name = 'previous_questions_illia.txt'
                # current_questions_id = '1IokPRppnJh5cxaSl2UP-12CVe7-l168F'
                # got_by_id = service.files().get(fileId=current_questions_id).execute()
                # file['title'] = name
                # file['description'] = 'description'
                # file['mimeType'] = 'text/plain'
                #
                # media_body = MediaFileUpload(
                #     'previous_questions_illia.txt', mimetype='text/plain', resumable=True)
                # print("hello")
                # updated_file = service.files().update(
                #     fileId=current_questions_id,
                #     body=file,
                #     newRevision=False,  # it should replace data. True - appends
                #     media_body=media_body).execute()

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()
