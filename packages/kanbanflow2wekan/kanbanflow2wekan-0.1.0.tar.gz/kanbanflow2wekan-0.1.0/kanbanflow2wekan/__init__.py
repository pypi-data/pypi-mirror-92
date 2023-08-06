__version__ = '0.1.0'

import os
import json
import requests


class Kanbanflow:
  def __init__(self, email, password):
    self.session = requests.Session()
    url = 'https://kanbanflow.com/login'
    data = {"email": email, "password": password, "rememberMe": "on"}
    r = self.session.post(url, data=data)

  def download_attachments(self, dump, path):
    for task in dump:
      if 'attachments' in task:
        for attachment in task['attachments']:
          link = attachment['link']
          name = attachment['name']

          if not os.path.exists(os.path.join(path, name)):
            with self.session.get(link, stream=True) as r:
              # r.raise_for_status()
              with open(os.path.join(path, name), 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                  f.write(chunk)
    return name

  def read_dumps(self, path):
    files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".json")]

    dumps = []
    for file in files:
      with open(file) as json_file:
        data = json.load(json_file)

        folder_path = file.split('.')[0]
        # folder_path = file
        if not os.path.exists(folder_path):
          os.makedirs(folder_path)
        # file é o path da pasta
        self.download_attachments(data, folder_path)

        dumps.append(data)

    return dumps


class Wekan:
  def __init__(self, api_url, username, password):
    path = '/users/login'
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Accept': '*/*'
    }
    data = {"username": username, "password": password}

    self.session = requests.Session()
    self.base = api_url

    url = self.base + path
    r = self.session.post(url, data=data, headers=headers)
    self.token = r.json()['token']
    self.id = r.json()['id']
    self.headers = {
      'Accept': 'application/json',
      'Authorization': 'Bearer {0}'.format(self.token)
    }

  def create_board(self, title):
    path = '/api/boards'
    url = self.base + path
    data = {
      'title': title,
      'owner': self.id
    }
    r = self.session.post(url, data=data, headers=self.headers)
    # print(r.json())

    self.delete_swimlane(r.json()['_id'], r.json()['defaultSwimlaneId'])

    return r.json()['_id']

  def create_swimlane(self, board_id, title):
    path = '/api/boards/{0}/swimlanes'.format(board_id)
    url = self.base + path
    data = {
      'title': title,
    }
    r = self.session.post(url, data=data, headers=self.headers)
    # print(r.status_code)
    # print(r.json())
    return r.json()['_id']

  def delete_swimlane(self, board_id, swimlane_id):
    path = '/api/boards/{0}/swimlanes/{1}'.format(board_id, swimlane_id)
    url = self.base + path
    r = self.session.delete(url, headers=self.headers)
    # print(r.status_code)
    # print(r.json())

  def create_list(self, board_id, title):
    path = '/api/boards/{0}/lists'.format(board_id)
    url = self.base + path
    data = {
      'title': title,
    }
    r = self.session.post(url, data=data, headers=self.headers)
    # print(r.status_code)
    # print(r.json())
    return r.json()['_id']

  def create_card(self, board_id, list_id, author_id, swimlane_id, title, description):
    path = '/api/boards/{0}/lists/{1}/cards'.format(board_id, list_id)
    url = self.base + path
    data = {
      'authorId': author_id,
      'title': title,
      'description': description,
      'swimlaneId': swimlane_id
    }
    r = self.session.post(url, data=data, headers=self.headers)
    # print(r.status_code)
    return r.json()['_id']


  def create_checklist(self, board_id, card_id, title, items):
    path = '/api/boards/{0}/cards/{1}/checklists'.format(board_id, card_id)
    url = self.base + path
    data = {
      'title': title,
      'items': items
    }
    r = self.session.post(url, data=data, headers=self.headers)
    # print(r.status_code)
    print(r.json())
    return r.json()['_id']

  def create_comment(self, board_id, card_id, author_id, comment):
    path = '/api/boards/{0}/cards/{1}/comments'.format(board_id, card_id)
    url = self.base + path
    data = {
      'authorId': author_id,
      'comment': comment
    }
    r = self.session.post(url, data=data, headers=self.headers)
    # print(r.status_code)
    print(r.json())
    return r.json()['_id']

  def get_user_id(self, email):
    username = email.split('@')[0]
    path = '/api/users/'
    url = self.base + path
    r = self.session.get(url, headers=self.headers)
    # print(r.status_code)
    users = r.json()

    user_id = self.id
    for user in users:
      if 'username' in user:
        if user['username'] == username:
          user_id = user['_id']
          break

    return user_id

