from git import Repo

def start_feature_branch(repo_path, feature_branch_name, base_branch='main'):
    try:
        repo = Repo(repo_path)
        origin = repo.remote(name='origin')
        
        # Check if the branch exists and switch to it, or create a new one
        if feature_branch_name in repo.branches:
            branch = repo.branches[feature_branch_name]
            repo.git.checkout(branch)
        else:
            repo.git.checkout(base_branch)
            repo.git.pull('origin', base_branch)
            repo.git.checkout('-b', feature_branch_name)
            origin.push('--set-upstream', feature_branch_name)

        print(f"Switched to branch: {feature_branch_name}")
    except Exception as e:
        print(f"An error occurred: {e}")

def commit_to_feature_branch(repo_path, commit_message):
    try:
        repo = Repo(repo_path)
        if repo.is_dirty(untracked_files=True):
            repo.git.add(A=True)
            repo.index.commit(commit_message)
            print("Changes committed to feature branch.")
        else:
            print("No changes to commit.")
    except Exception as e:
        print(f"An error occurred: {e}")

def merge_feature_to_main(repo_path, feature_branch_name):
    try:
        repo = Repo(repo_path)
        origin = repo.remote(name='origin')
        
        # Switch to the main branch and merge the feature branch into it
        repo.git.checkout('main')
        repo.git.pull('origin', 'main')
        repo.git.merge(feature_branch_name)
        
        # Push changes to the remote repository
        origin.push()
        print(f"Feature branch '{feature_branch_name}' merged into 'main' and pushed to remote.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
repo_path = 'D:/i-Open_backend'
feature_branch_name = 'feature/new-awesome'
commit_message = 'Add new awesome feature'

start_feature_branch(repo_path, feature_branch_name)
# Make your changes in the code here
commit_to_feature_branch(repo_path, commit_message)
# Test your changes here, and if everything is ok:
merge_feature_to_main(repo_path, feature_branch_name)