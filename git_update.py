import os

def git_update(commit , add='.' , path='.'):
    os.system(f'cp {add} {add}')
    os.system(f'cd {path}')
    os.system(f'git add {add}')
    os.system(f'git commit -m "{commit}"')
    os.system('git push origin master')
