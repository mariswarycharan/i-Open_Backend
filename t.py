from git import Repo, GitCommandError
import subprocess

def create_feature_branch(repo_path: str, feature_name: str) -> str:
    """
    Create a new feature branch from the main branch.

    Args:
        repo_path (str): Path to the local Git repository.
        feature_name (str): Name of the new feature branch.

    Returns:
        str: Name of the created feature branch, or None if an error occurred.
    """
    try:
        repo = Repo(repo_path)

        # Ensure we're on the main branch and it's up to date
        repo.git.checkout('main')
        repo.git.pull('origin', 'main')

        # Create and switch to the new feature branch
        new_branch = f"feature/{feature_name}"
        repo.git.checkout('-b', new_branch)
        print(f"Created and switched to new branch: {new_branch}")
        return new_branch
    except GitCommandError as e:
        print(f"Git command error while creating the feature branch: {e}")
        return None
    except Exception as e:
        print(f"An error occurred while creating the feature branch: {e}")
        return None


def commit_and_push(repo_path: str, commit_message: str, branch: str) -> bool:
    """
    Commit changes and push to the specified branch.

    Args:
        repo_path (str): Path to the local Git repository.
        commit_message (str): Commit message.
        branch (str): Branch to push to.

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        repo = Repo(repo_path)

        if repo.is_dirty(untracked_files=True):
            # Stage all changes
            repo.git.add(A=True)

            # Commit changes
            repo.index.commit(commit_message)

            # Push changes to the remote branch
            origin = repo.remote(name='origin')
            origin.push(branch)
            print(f"Changes pushed to {branch} branch successfully!")
            return True
        else:
            print("No changes to commit.")
            return False
    except GitCommandError as e:
        print(f"Git command error while committing or pushing: {e}")
        return False
    except Exception as e:
        print(f"An error occurred while committing and pushing: {e}")
        return False


def run_tests(repo_path: str) -> bool:
    """
    Run tests for the project using unittest.

    Args:
        repo_path (str): Path to the local Git repository.

    Returns:
        bool: True if all tests pass, False otherwise.
    """
    try:
        # Placeholder for actual test command; replace with your project's test runner
        result = subprocess.run(['python', '-m', 'unittest', 'discover', repo_path], 
                                capture_output=True, text=True)

        if result.returncode == 0:
            print("All tests passed successfully!")
            return True
        else:
            print("Tests failed. Please fix the issues before merging.")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"An error occurred while running tests: {e}")
        return False


def merge_feature_branch(repo_path: str, feature_branch: str, main_branch: str = 'main') -> bool:
    """
    Merge the feature branch into the main branch after successful testing.

    Args:
        repo_path (str): Path to the local Git repository.
        feature_branch (str): Name of the feature branch to merge.
        main_branch (str): Name of the main branch. Defaults to 'main'.

    Returns:
        bool: True if the merge was successful, False otherwise.
    """
    try:
        repo = Repo(repo_path)

        # Switch to the main branch and pull the latest changes
        repo.git.checkout(main_branch)
        repo.git.pull('origin', main_branch)

        # Merge the feature branch
        print(f"Merging feature branch '{feature_branch}' into '{main_branch}'...")
        repo.git.merge(feature_branch)

        # Push the merged changes to the remote repository
        origin = repo.remote(name='origin')
        origin.push(main_branch)
        print(f"Feature branch '{feature_branch}' successfully merged into '{main_branch}' and pushed to remote.")
        return True
    except GitCommandError as e:
        print(f"Git command error during merge: {e}")
        return False
    except Exception as e:
        print(f"An error occurred while merging the feature branch: {e}")
        return False


def task_branching_workflow(repo_path: str, feature_name: str, commit_message: str) -> bool:
    """
    Execute the full task branching workflow: create branch, commit changes, run tests, and merge if tests pass.

    Args:
        repo_path (str): Path to the local Git repository.
        feature_name (str): Name of the new feature.
        commit_message (str): Commit message for the changes.

    Returns:
        bool: True if the entire workflow completes successfully, False otherwise.
    """
    # Create the feature branch
    feature_branch = create_feature_branch(repo_path, feature_name)
    if not feature_branch:
        return False

    # Commit and push changes to the feature branch
    if not commit_and_push(repo_path, commit_message, feature_branch):
        return False

    # Run tests
    if not run_tests(repo_path):
        print("Tests failed. Feature branch not merged.")
        return False

    # Merge the feature branch into the main branch
    if merge_feature_branch(repo_path, feature_branch):
        print(f"Feature '{feature_name}' has been successfully developed, tested, and merged!")
        return True
    else:
        print(f"Failed to merge feature '{feature_name}'. Please resolve conflicts manually.")
        return False


# Example usage
if __name__ == "__main__":
    repo_path = 'D:/i-Open_backend'
    feature_name = 'new-awesome-feature'
    commit_message = 'Implemented new awesome feature'

    success = task_branching_workflow(repo_path, feature_name, commit_message)
    if success:
        print("Task branching workflow completed successfully!")
    else:
        print("Task branching workflow encountered issues. Please review and resolve manually.")
