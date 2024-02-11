from Config import Config
from git import Repo, GitCommandError
import logging
import questionary
import datetime


class Git():
    # Variables
    __CONFIG: Config
    __REPO: Repo
    __TIME_ZONE = datetime.timezone.utc

    # Constants
    __C_REPO_PATH = 'path'
    __C_BRANCH_NAME = 'branch_name'
    __C_TIME_FORMAT = '"%Y_%m_%d_%H:%M"'

    def __init__(self, config: Config):
        self.__CONFIG = config
        self.__REPO = Repo(self.__CONFIG.get_git_item('path'))

        self.fetch()
        input('Press Enter when you have checked that you are ready to start cherry-picking e.g. all your current '
              'work has been commited')
        self.checkout(self.__CONFIG.get_git_item(self.__C_BRANCH_NAME))
        self.pull()
        self.checkout(
            f'{self.__CONFIG.get_git_item(self.__C_BRANCH_NAME)}_cherry_pick_{datetime.datetime.now(tz=self.__TIME_ZONE).strftime(self.__C_TIME_FORMAT)}')

    def fetch(self):
        logging.info('Fetching')
        for remote in self.__REPO.remotes:
            remote.fetch()
        logging.info('Fetched')

    def checkout(self, branch_name: str, new_branch: bool = False):
        if new_branch:
            logging.info(f'Checking out to new branch {branch_name}')
            self.__REPO.git.checkout('-b', branch_name)
        else:
            logging.info(f'Checking out to branch {branch_name}')
            self.__REPO.git.checkout(branch_name)

    def get_branch_names(self) -> [str]:
        return self.__REPO.branches

    def pull(self):
        logging.info('Pulling')
        self.__REPO.remotes.origin.pull()

    def cherry_pick(self, commit_hash: str) -> bool:
        """" This function does a cherry-pick of the given commit, if the commit has conflicts the function will
        pause and ask the user to handle the merge conflict, returns False if the CP was not aborted, else True"""

        result = False

        try:
            logging.info(f'Starting cherry pick {commit_hash}')
            self.__REPO.git.cherry_pick(commit_hash)
        except GitCommandError:
            logging.warning(f'Got an error while cherry picking {commit_hash}, assuming its a merge conflict')
            inp = questionary.select(
                f'Conflict encountered while cherry picking commit {commit_hash}, either fix the merge conflict manually or skip / abort the cherry pick',
                choices=[
                    'continue',
                    'abort',
                    'skip'
                ]
            ).ask()

            result = inp == 'abort'
            self.__REPO.git.cherry_pick(f'--{inp}')

        return result
