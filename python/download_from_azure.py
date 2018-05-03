import configparser
from azure.storage.file import FileService

configs = configparser.ConfigParser()
configs.read("C:/ws/filescripts/config.ini")

storage_key = configs.get("Azure", "storage-key")
share_name = configs.get("Azure", "share-name")
storage_name = configs.get("Azure", "storage-name")

remote_data_path = 'prod/WeeklyReports'
local_data_path = 'C:/data/ford/WeeklyReports/'

file_service = FileService(account_name=share_name, account_key=storage_key)
file_service.set_proxy(host='localhost',port='3128')

shares = list(file_service.list_directories_and_files(storage_name,remote_data_path))
file_list = list(map(lambda x:x.name,shares))

for fn in file_list:
    file_service.get_file_to_path(storage_name, remote_data_path, fn, local_data_path+fn)
# fn = 'MonthlyReport_June_2017.txt'
# file_service.get_file_to_path(storage_name, remote_data_path, fn, local_data_path+fn)
