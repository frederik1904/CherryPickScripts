from pykeepass import PyKeePass
from getpass import getpass
from config import Config


class KeePass:
    # Variables
    __CONFIG: Config = Config()
    __PATH: str
    __PASSWORD: str
    __KEE_PASS_GROUP_NAME: str

    # Constants
    __C_PATH = 'path'
    __C_GROUP_NAME = 'group_name'
    __C_TITLE_TFS = 'TFS'
    __C_TITLE_TOOLKIT = 'Toolkit'

    def __init__(self):
        self.__PASSWORD = getpass('Type password for keepass:')

        self.__PATH = self.__CONFIG.get_kee_pass_item(self.__C_PATH)
        self.__KEE_PASS_GROUP_NAME = self.__CONFIG.get_kee_pass_item(self.__C_GROUP_NAME)

        self.__KP = PyKeePass(self.__PATH, self.__PASSWORD)

    def get_tfs_information(self):
        return self.get_by_title(self.__C_TITLE_TFS)

    def get_toolkit_information(self):
        return self.get_by_title(self.__C_TITLE_TOOLKIT)

    def get_by_title(self, title: str):
        return self.__KP.find_entries_by_title(title=title, first=True)

    def get_cph_group(self):
        return self.__KP.find_groups(name=self.__KEE_PASS_GROUP_NAME, first=True)

