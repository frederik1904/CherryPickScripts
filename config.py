import configparser


class Config():
    CONFIG: configparser.ConfigParser = configparser.ConfigParser()
    KEE_PASS: str = 'KeePass'
    def __init__(self):
        self.CONFIG.read('config.ini')

    def get_kee_pass_item(self, item: str) -> str:
        return self.CONFIG[self.KEE_PASS][item]
