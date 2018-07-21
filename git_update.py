import os

def git_update(commit , add='.'):
    os.system(f'git add {add}')
    os.system(f'git commit -m "{commit}"')
    os.system('git push origin master')
