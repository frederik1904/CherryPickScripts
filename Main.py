from Config import Config
from KeePass import KeePass

config = Config()
kp = KeePass(config)

kp.get_toolkit_information()
