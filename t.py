from git import Repo, GitCommandError

def start_feature_branch(repo_path: str, feature_branch_name: str, main_branch: str = 'main') -> None:
    """
    Start a new feature branch from the main branch.
    
    Args:
        repo_path (str): The local path to the Git repository.
        feature_branch_name (str): The name of the feature branch to create.
        main_branch (str): The name of the main branch. Defaults to 'main'.
    
    Raises:
        GitCommandError: If an error occurs while running Git commands.
        Exception: For any other errors that may occur.
    """
    try:
        repo = Repo(repo_path)
        origin = repo.remote(name='origin')

        # Checkout the main branch and pull latest changes
        repo.git.checkout(main_branch)
        repo.git.pull('origin', main_branch)
        
        # Check if the feature branch exists and create it if necessary
        if feature_branch_name in repo.heads:
            print(f"Feature branch '{feature_branch_name}' already exists. Checking it out.")
            repo.git.checkout(feature_branch_name)
        else:
            print(f"Creating and checking out feature branch '{feature_branch_name}'...")
            repo.git.checkout('-b', feature_branch_name)
            origin.push('--set-upstream', origin.name, feature_branch_name)
        
        print(f"Switched to feature branch: '{feature_branch_name}'")
        
    except GitCommandError as gce:
        print(f"Git command failed: {gce}")
    except Exception as e:
        print(f"An error occurred: {e}")


def commit_to_feature_branch(repo_path: str, commit_message: str) -> None:
    """
    Commit changes to the feature branch.
    
    Args:
        repo_path (str): The local path to the Git repository.
        commit_message (str): The commit message to use.
    
    Raises:
        GitCommandError: If an error occurs while running Git commands.
        Exception: For any other errors that may occur.
    """
    try:
        repo = Repo(repo_path)

        if repo.is_dirty(untracked_files=True):
            repo.git.add(A=True)
            repo.index.commit(commit_message)
            print(f"Changes committed with message: '{commit_message}'")
        else:
            print("No changes to commit.")
    
    except GitCommandError as gce:
        print(f"Git command failed: {gce}")
    except Exception as e:
        print(f"An error occurred: {e}")


def finish_feature_branch(repo_path: str, feature_branch_name: str, main_branch: str = 'main') -> None:
    """
    Merge the feature branch into the main branch and push changes to the remote.
    
    Args:
        repo_path (str): The local path to the Git repository.
        feature_branch_name (str): The name of the feature branch to merge.
        main_branch (str): The name of the main branch. Defaults to 'main'.
    
    Raises:
        GitCommandError: If an error occurs while running Git commands.
        Exception: For any other errors that may occur.
    """
    try:
        repo = Repo(repo_path)
        origin = repo.remote(name='origin')

        # Checkout the main branch and pull latest changes
        repo.git.checkout(main_branch)
        repo.git.pull('origin', main_branch)

        # Merge the feature branch into the main branch
        print(f"Merging feature branch '{feature_branch_name}' into '{main_branch}'...")
        repo.git.merge(feature_branch_name)

        # Push the changes to the remote main branch
        origin.push(main_branch)
        print(f"Main branch '{main_branch}' updated and pushed to remote.")

        # Optionally delete the local feature branch after merging
        repo.git.branch('-d', feature_branch_name)
        print(f"Feature branch '{feature_branch_name}' deleted locally.")
    
    except GitCommandError as gce:
        print(f"Git command failed: {gce}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage:
repo_path = 'D:/i-Open_backend'
feature_branch_name = 'feature/new-awesome-feature'
commit_message = 'Add new awesome feature'

# Start a new feature branch
start_feature_branch(repo_path, feature_branch_name)

# Commit changes to the feature branch
commit_to_feature_branch(repo_path, commit_message)

# Assume testing is done at this point. Once testing is complete, merge the feature branch.
finish_feature_branch(repo_path, feature_branch_name)
