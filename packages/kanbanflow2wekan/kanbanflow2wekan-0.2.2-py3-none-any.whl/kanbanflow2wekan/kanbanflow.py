import os
import json
import requests

class Kanbanflow:
  def __init__(self, email=None, password=None, kf_download_attachments=False):
    self.kf_download_attachments = kf_download_attachments
    if kf_download_attachments and email and password:
      self.session = requests.Session()
      url = 'https://kanbanflow.com/login'
      data = {"email": email, "password": password, "rememberMe": "on"}
      r = self.session.post(url, data=data)
      r.raise_for_status()

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

    dumps = {}
    for file in files:
      with open(file) as json_file:
        data = json.load(json_file)

        folder_path = file.split('.')[0]
        dump_name = folder_path.split('/')[-1]

        if not os.path.exists(folder_path):
          os.makedirs(folder_path)

        if self.kf_download_attachments:
          self.download_attachments(data, folder_path)

        dumps[dump_name] = data

    return dumps