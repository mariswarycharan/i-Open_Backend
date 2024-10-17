from git import Repo
import subprocess

def create_feature_branch(repo_path, feature_name):
    """
    Create a new feature branch from the main branch.
    
    Args:
    repo_path (str): Path to the local Git repository
    feature_name (str): Name of the new feature branch
    
    Returns:
    str: Name of the created feature branch
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
    except Exception as e:
        print(f"An error occurred while creating the feature branch: {e}")
        return None

def commit_and_push(repo_path, commit_message, branch):
    """
    Commit changes and push to the specified branch.
    
    Args:
    repo_path (str): Path to the local Git repository
    commit_message (str): Commit message
    branch (str): Branch to push to
    
    Returns:
    bool: True if successful, False otherwise
    """
    try:
        repo = Repo(repo_path)
        if repo.is_dirty(untracked_files=True):
            repo.git.add(A=True)
            repo.index.commit(commit_message)
            origin = repo.remote(name='origin')
            origin.push(branch)
            print(f"Changes pushed to {branch} branch successfully!")
            return True
        else:
            print("No changes to commit.")
            return False
    except Exception as e:
        print(f"An error occurred while committing and pushing: {e}")
        return False

def run_tests(repo_path):
    """
    Run tests for the project.
    
    Args:
    repo_path (str): Path to the local Git repository
    
    Returns:
    bool: True if tests pass, False otherwise
    """
    try:
        # This is a placeholder for running tests. Replace with your actual test command.
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

def merge_feature_branch(repo_path, feature_branch):
    """
    Merge the feature branch into the main branch after successful testing.
    
    Args:
    repo_path (str): Path to the local Git repository
    feature_branch (str): Name of the feature branch to merge
    
    Returns:
    bool: True if merge was successful, False otherwise
    """
    try:
        repo = Repo(repo_path)
        
        # Switch to main branch and update it
        repo.git.checkout('main')
        repo.git.pull('origin', 'main')
        
        # Merge the feature branch
        repo.git.merge(feature_branch)
        
        # Push the merged changes to remote main branch
        origin = repo.remote(name='origin')
        origin.push('main')
        
        print(f"Feature branch {feature_branch} merged into main successfully!")
        return True
    except Exception as e:
        print(f"An error occurred while merging the feature branch: {e}")
        return False

def task_branching_workflow(repo_path, feature_name, commit_message):
    """
    Execute the full task branching workflow: create branch, commit changes,
    run tests, and merge if tests pass.
    
    Args:
    repo_path (str): Path to the local Git repository
    feature_name (str): Name of the new feature
    commit_message (str): Commit message for the changes
    
    Returns:
    bool: True if the entire workflow completed successfully, False otherwise
    """
    # Create feature branch
    feature_branch = create_feature_branch(repo_path, feature_name)
    if not feature_branch:
        return False
    
    # Commit and push changes
    if not commit_and_push(repo_path, commit_message, feature_branch):
        return False
    
    # Run tests
    if not run_tests(repo_path):
        print("Tests failed. Feature branch not merged.")
        return False
    
    # Merge feature branch
    if merge_feature_branch(repo_path, feature_branch):
        print(f"Feature '{feature_name}' has been successfully developed, tested, and merged!")
        return True
    else:
        print(f"Failed to merge feature '{feature_name}'. Please resolve conflicts manually.")
        return False

# Example usage
if __name__ == "__main__":
    repo_path = 'D:/i-Open_backend'
    feature_name = "new_awesome_feature_test"
    commit_message = "Implemented new awesome feature"
    
    success = task_branching_workflow(repo_path, feature_name, commit_message)
    if success:
        print("Task branching workflow completed successfully!")
    else:
        print("Task branching workflow encountered issues. Please review and resolve manually.")