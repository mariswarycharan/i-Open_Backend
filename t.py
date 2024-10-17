from git import Repo

def push_code_to_repo(repo_path, commit_message, feature_branch, main_branch='main'):
    try:
        repo = Repo(repo_path)
        if repo.is_dirty(untracked_files=True):
            repo.git.add(A=True)
            repo.index.commit(commit_message)
            origin = repo.remote(name='origin')
            
            # Check out the feature branch, or create it if it doesn't exist
            if feature_branch not in repo.heads:
                print(f"Creating new branch: {feature_branch}")
                repo.git.checkout('HEAD', b=feature_branch)
            else:
                print(f"Checking out existing branch: {feature_branch}")
                repo.git.checkout(feature_branch)
            
            # Push the feature branch to the remote repository
            origin.push(feature_branch)
            print(f"Feature branch '{feature_branch}' pushed successfully!")
            
            # Checkout the main branch and merge the feature branch into it
            repo.git.checkout(main_branch)
            print(f"Merging '{feature_branch}' into '{main_branch}'...")
            repo.git.merge(feature_branch)
            print(f"'{feature_branch}' successfully merged into '{main_branch}'")
            
            # Push the updated main branch to the remote repository
            origin.push(main_branch)
            print(f"Main branch '{main_branch}' updated successfully!")
        else:
            print("No changes to commit.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Usage example
repo_path = 'D:/i-Open_backend'
commit_message = 'Add new feature XYZ'
feature_branch = 'feature/xyz'
push_code_to_repo(repo_path, commit_message, feature_branch)