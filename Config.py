import configparser


class Config():
    CONFIG: configparser.ConfigParser = configparser.ConfigParser()
    C_KEE_PASS: str = 'KeePass'
    C_PY_GIT: str = 'PyGit'

    def __init__(self):
        self.CONFIG.read('config.ini')

    def get_kee_pass_item(self, item: str) -> str:
        return self.CONFIG[self.C_KEE_PASS][item]

    def get_git_item(self, item: str) -> str:
        return self.CONFIG[self.C_PY_GIT][item]
