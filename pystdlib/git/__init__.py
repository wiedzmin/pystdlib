import os

from pygit2 import RemoteCallbacks, Tag, UserPass

from pystdlib.uishim import log_error
from pystdlib.passutils import read_entry_raw, extract_specific_line, \
    extract_by_regex, field_regex_mappings

MAIN_BRANCHES = ["master", "main"]


def is_git_repo(path=None):
    if not path:
        return False
    root = os.path.abspath(path) + "/.git"
    return os.path.exists(root) and os.path.isdir(root)


def get_active_branch(repo):
    head = None
    try:
        head = repo.references['HEAD'].resolve()
    except KeyError as e:
        return head
    return head.name


def is_main_branch_active(repo):
    return any([get_active_branch(repo).endswith(branch)
                for branch in MAIN_BRANCHES])


def is_main_branch_protected():
    return any([os.path.exists(allow_token) and os.path.isfile(allow_token)
                for allow_token in [os.path.abspath(os.getcwd()) + f"/.unseal_{branch}"
                                    for branch in MAIN_BRANCHES]])


def resolve_remote(repo, remote_name):
    remote = None
    try:
        remote = repo.remotes[remote_name]
    except KeyError:
        pass
    return remote


def get_diff_size(repo):
    active_branch = get_active_branch(repo)
    if not active_branch:
        log_info("probably empty repo")
        return 0
    diff = repo.diff()
    return diff.stats.insertions + diff.stats.deletions


def collect_tags(repo):
    result = []
    for refname in repo.listall_references():
        ref = repo.revparse_single(refname)
        if isinstance(ref, Tag):
            result.append(refname)
    return result


def build_auth_callbacks(repo, pass_path):
    if not pass_path:
        log_error("empty pass path")
        raise ValueError("empty pass path")

    entry_data = read_entry_raw(pass_path)
    password = extract_specific_line(entry_data, 0)
    username = extract_by_regex(entry_data, field_regex_mappings["login"])

    if not username:
        log_error("username not found")
        raise ValueError("username not found")
    if not password:
        log_error("password not found")
        raise ValueError("password not found")

    return RemoteCallbacks(credentials=UserPass(username, password))
