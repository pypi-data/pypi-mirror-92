__version__ = '0.2.0'

from .kanbanflow import Kanbanflow
from .wekan import Wekan

class k2w:
  def __init__(
    self,
    wekan_url,
    wekan_user,
    wekan_password,
    kf_dump_path,
    kf_user=None,
    kf_password=None,
    kf_download_attachments=False,
  ):
    self.wekan_url = wekan_url
    self.wekan_user = wekan_user
    self.wekan_password = wekan_password
    self.kf_dump_path = kf_dump_path
    self.kf_user = kf_user
    self.kf_password = kf_password

    self.kf = Kanbanflow(
      kf_user,
      kf_password,
      kf_download_attachments,
    )

    self.dumps = self.kf.read_dumps(kf_dump_path)

    self.w = Wekan(
      wekan_url,
      wekan_user,
      wekan_password
    )

  def migrate(self):
    for dump_name in self.dumps:
      print('DUMP: ', dump_name)
      board_id = self.w.create_board(dump_name)

      swimlanes = {}
      lists = {}
      for task in self.dumps[dump_name]:
        print('\tTASK: ', task['name'])
        if task['swimlane'] not in swimlanes:
          swimlane_id = self.w.create_swimlane(board_id, task['swimlane'])
          swimlanes[task['swimlane']] = swimlane_id

        if task['column'] not in lists:
          list_id = self.w.create_list(board_id, task['column'])
          lists[task['column']] = list_id

        card_id = self.w.create_card(
          board_id,
          lists[task['column']],
          self.w.user_id,
          swimlanes[task['swimlane']],
          task['name'],
          task['description'],
        )

        if 'subTasks' in task:
          subtasks = [sub['name'] for sub in task['subTasks']]

          self.w.create_checklist(board_id, card_id, 'Subtasks', subtasks)

        if 'comments' in task:
          for comment in task['comments']:
            username = comment['author']['email']
            user_id = self.w.get_user_id(username)

            self.w.create_comment(board_id, card_id, user_id, comment['text'])



