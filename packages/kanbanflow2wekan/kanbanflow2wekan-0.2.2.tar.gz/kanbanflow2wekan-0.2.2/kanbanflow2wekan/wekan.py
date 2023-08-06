import requests

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
    self.user_id = r.json()['id']
    self.headers = {
      'Accept': 'application/json',
      'Authorization': 'Bearer {0}'.format(self.token)
    }

  def create_board(self, title):
    path = '/api/boards'
    url = self.base + path
    data = {
      'title': title,
      'owner': self.user_id
    }
    r = self.session.post(url, data=data, headers=self.headers)

    self.delete_swimlane(r.json()['_id'], r.json()['defaultSwimlaneId'])

    return r.json()['_id']

  def create_swimlane(self, board_id, title):
    path = '/api/boards/{0}/swimlanes'.format(board_id)
    url = self.base + path
    data = {
      'title': title,
    }
    r = self.session.post(url, data=data, headers=self.headers)
    return r.json()['_id']

  def delete_swimlane(self, board_id, swimlane_id):
    path = '/api/boards/{0}/swimlanes/{1}'.format(board_id, swimlane_id)
    url = self.base + path
    r = self.session.delete(url, headers=self.headers)

  def create_list(self, board_id, title):
    path = '/api/boards/{0}/lists'.format(board_id)
    url = self.base + path
    data = {
      'title': title,
    }
    r = self.session.post(url, data=data, headers=self.headers)

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

    return r.json()['_id']


  def create_checklist(self, board_id, card_id, title, items):
    path = '/api/boards/{0}/cards/{1}/checklists'.format(board_id, card_id)
    url = self.base + path
    data = {
      'title': title,
      'items': items
    }
    r = self.session.post(url, data=data, headers=self.headers)

    return r.json()['_id']

  def create_comment(self, board_id, card_id, author_id, comment):
    path = '/api/boards/{0}/cards/{1}/comments'.format(board_id, card_id)
    url = self.base + path
    data = {
      'authorId': author_id,
      'comment': comment
    }
    r = self.session.post(url, data=data, headers=self.headers)

    return r.json()['_id']

  def get_user_id(self, email):
    username = email.split('@')[0]
    path = '/api/users/'
    url = self.base + path
    r = self.session.get(url, headers=self.headers)

    users = r.json()

    user_id = self.user_id
    for user in users:
      if 'username' in user:
        if user['username'] == username:
          user_id = user['_id']
          break

    return user_id

