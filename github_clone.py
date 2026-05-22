import os
import shutil
import stat
from git import Repo

def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def clone_repo(repo_url):
    clone_path = "cloned_repo"

    # Remove old repo safely
    if os.path.exists(clone_path):
        shutil.rmtree(clone_path, onexc=remove_readonly)

    # Clone fresh repo
    Repo.clone_from(repo_url, clone_path)

    return clone_path