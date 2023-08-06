from typing import NoReturn
from github_parser_pkg.user_profile import user_profile_parser
from github_parser_pkg.user_repos import user_repos_parser

def user_profile_main(username):
    profile_url = "https://github.com/"+ username
    user_profile_results = user_profile_parser(profile_url,username)
    return user_profile_results

def repo_info_main(url):
    user_repos_results = user_repos_parser(url)
    return user_repos_results

