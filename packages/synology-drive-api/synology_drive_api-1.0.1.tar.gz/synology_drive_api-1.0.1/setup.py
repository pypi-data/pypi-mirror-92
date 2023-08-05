# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['synology_drive_api']

package_data = \
{'': ['*']}

install_requires = \
['optionaldict>=0.1.1,<0.2.0',
 'requests>=2.22.0,<3.0.0',
 'selenium>=3.141.0,<4.0.0',
 'simplejson>=3.17.0,<4.0.0']

setup_kwargs = {
    'name': 'synology-drive-api',
    'version': '1.0.1',
    'description': 'synology drive api python wrapper',
    'long_description': 'Inspired by  [synology-api](https://github.com/N4S4/synology-api). This repo is aimed at providing **Synology drive** api wrapper and related helper functions. It helps you manage your files/folders/labels in synology drive.  By means of Synology Office, you can edit spreadsheet on Drive and use this api wrapper read spreadsheet. It supports Python 3.7+.\n\n## Get login session\n\nYou can access drive by IP, drive domain or nas domain + drive path. \n\n> Synology Drive allows same user with multiple login session. if you need multiple login session and label functions, disable label cache.\n\n```python\nfrom synology_drive_api.drive import SynologyDrive\n\n# default http port is 5000, https is 5001. \nwith SynologyDrive(NAS_USER, NAS_PASS, NAS_IP) as synd:\n    pass \n# Use specified port\nwith SynologyDrive(NAS_USER, NAS_PASS, NAS_IP, NAS_PORT) as synd:\n    pass\n# use http instead of https. https: default is True.\nwith SynologyDrive(NAS_USER, NAS_PASS, NAS_IP, https=False) as synd:\n    pass\n# use domain name or name + path access drive\n# Enabled in Application Portal | Application | Drive | General | Enable customized alias\ndrive_path_demo = \'your_nas_domain/drive\'\n# Enabled in Application Portal | Application | Drive | General | Enable customized domain\ndrive_path_demo2 = \'your_drive_domain\'\nwith SynologyDrive(NAS_USER, NAS_PASS, drive_path_demo) as synd:\n    pass\n# disable label cache\nwith SynologyDrive(NAS_USER, NAS_PASS, drive_path_demo, enable_label_cache=False) as synd:\n    pass\n```\n\n## Manage labels\n\nSynology drive thinks labels need to belong to single user. **If you want share labels between users, you should have access to these user accounts.** Another solution is creating a *tool user*.\n\nSynology drive search function provide label union search rather than intersection search. **If you need label intersection search, combine them into one label.**\n\n### Get label info\n\n```python\n# get single label info\nsynd.get_labels(\'your_label_name\')\n# get all labels info\nsynd.get_labels()\n```\n\n### Create/delete label\n\nLabel name is unique in drive.\n\n```python\n# create a label, color name: gray/red/orange/yellow/green/blue/purple.\n# default color is gray, default position is end of labels. 0 is first position.\nret = synd.create_label(\'your_label_name\', color=\'orange\', pos=0)\n# delete label by name/id.\nret = synd.delete_label(\'your_label_name\')\nret = synd.delete_label(label_id=419)\n```\n\n### Add/delete path label\n\n```python\n# acition：add, delete\nsynd.manage_path_label(action, path, label)\n```\n\npath examples:\n\n```python\n1. \'/team-folders/test_drive/SCU285/test.xls\', \'/mydrive/test_sheet_file.osheet\'\n2. \'505415003021516807\'\n3. [\'505415003021516807\', \'505415003021516817\']\n4. ["id:505415003021516807", "id:525657984139799470", "id:525657984810888112"]\n5. [\'/team-folders/test_drive/SCU285/test.xls\', \'/team-folders/test_drive/SCU283/test2.xls\']\n```\n\nlabel examples:\n\n```python\n1. \'label_name\'\n2. [\'label_name_1\', \'lable_name_2\']\n3. [{"action": "add", "label_id": "15"}, {"action": "add", "label_id": "16"}]\n```\n\n### List labelled files\n\nFilter files or folders by single label. If you want to use label union search, use search functions (todo).\n\n```python\nsynd.list_labelled_file(label_name=\'your_label_name\')\n```\n\n## Manage File/Folder\n\n>Team folder start with `/team-folders/`, Private folder start with `/mydrive/`\n\n### List TeamFolder\n\nTeamfolder  is virtual parent folder of shared folders in Synology drive. When you login in Drive, you can see your authorized shared folder.\n\n```python\nsynd.get_teamfolder_info()\n# {sub_folder_name: folder_id, ...}\n```\n\n### List Folder\n\nList Folder or files info of a folder\n\n```python\nsynd.list_folder(\'/mydrive\')\n```\n\n### Get specific folder or file info\n\nGet folder or file info such as created time.\n\n```python\n# file_path or file_id "552146100935505098"\nsynd.get_file_or_folder_info(path_or_path_id)\n```\n\n### Create Folder\n\n```python\n# create folder in your private folder\nsynd.create_folder(folder_name)\n# create folder in dest folder\nsynd.create_folder(\'test\', \'team-folder/folder2/\')\n```\n\n### Upload file\n\nYou don\'t need create folder subfolder before uploading your file.\n\n```python\n# prepare your file\nfile = io.BytesIO(mail_attachment[\'file\'])\n# add a file name to file\nfile.name = strip_file_name(mail_attachment[\'name\'])\nret_upload = nas_client.upload_file(file, dest_folder_path=dest_folder_path)\n# upload to your private folder\nret_upload = nas_client.upload_file(file)\n```\n\n### Download file\n\n```python\nfile_name = \'test.pdf\'\nbio = synd.download_file(f\'/mydrive/{file_name}\')\nwith open(file_name, \'wb\') as f:\n    f.write(bio)\n```\n\n### Download Synology office file\n\n```python\nimport pandas as pd\n\n# download osheet as xlsx and read into pandas dataframe.\nbio = synd.download_synology_office_file(\'/mydrive/test.osheet\')\npd.read_excel(bio, sheet_name=None)\n\n# dowloand odoc as docx\nbio = synd.download_synology_office_file(\'/mydrive/test.odoc\')\nwith open(\'test.docx\', \'wb\') as f:\n    f.write(bio)\n```\n\n### Delete file or folder\n\nDelete file or folder is  an async task.\n\n```python\nsynd.delete_path(\'/mydrive/abc_folder\')\nsynd.delete_path(\'598184594644187768\')\n```\n\n### Rename file or folder\n\n```python\n# Rename file \'/mydrive/H3_AP201812091265503218_1.pdf\' to \'/mydrive/new.pdf\'\nsynd.rename_path(\'new.pdf\', \'/mydrive/H3_AP201812091265503218_1.pdf\')\n# Rename folder \'/mydrive/test_folder\' to \'/mydrive/abc_folder\'\nsynd.rename_path(\'abc_folder\', \'/mydrive/test_folder\')\n```\n',
    'author': 'zbjdonald',
    'author_email': 'zbjdonald@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zbjdonald/synology-drive-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
