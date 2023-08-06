Kanbanflow2Wekan
================

[![](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/download/releases/3.4.0/)  [![](https://img.shields.io/github/license/ResidentMario/missingno.svg)](https://github.com/mdiniz97/AnsibleAWX-Client/blob/master/README.md)


Donate to help keep this project maintained

<a href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=ZHX5884XX26MW&source=url" target="_blank">
    <img src="https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif" border="0" name="submit" title="PayPal - The safer, easier way to pay online!" alt="Donate with PayPal button" />
</a>

Summary
-------
This is a library to perform kanban migration from Kanbanflow to Wekan in an automated way.

Requirements
------------
* requests

Quick Start Guide
-----------------

### Install kanbanflow2wekan
	pip install kanbanflow2wekan

### Initialize kanbanflow2wekan


    import os
    from dotenv import load_dotenv
    from kanbanflow2wekan import k2w

    load_dotenv()

    print('kanbanflow2wekan | by: @mdiniz97\n\n')

    migration = k2w(
        os.getenv('WEKAN_URL'),
        os.getenv('WEKAN_USER'),
        os.getenv('WEKAN_PASSWORD'),
        os.path.join(os.getcwd(), 'kanbanflow'), # path to kanbanflow dump's folder
        os.getenv('KANBANFLOW_USER'),
        os.getenv('KANBANFLOW_PASSWORD'),
        kf_download_attachments=True,
    )

    migration.migrate()
