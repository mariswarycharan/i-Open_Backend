import subprocess
import sys
import os

def is_git_repository():
    """
    Checks if the current directory is a Git repository by running 'git rev-parse'.
    
    Returns:
        bool: True if the current directory is a Git repository, False otherwise.
    """
    try:
        subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def update_code():
    """
    Pulls the latest code from the main repository branch, if the current directory is a Git repository.
    
    Raises:
        subprocess.CalledProcessError: If the command fails.
    """
    if not is_git_repository():
        print("This directory is not a Git repository. Please ensure you are in the correct directory.")
        sys.exit(1)
    
    update_command = ["git", "pull", "origin", "main"]
    try:
        print("Updating code repository...")
        subprocess.run(update_command, check=True)
        print("Code repository updated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to update code repository. Error: {e}", file=sys.stderr)
        sys.exit(1)

def deploy_to_environment(env):
    """
    Deploys the code to the specified environment.
    
    Args:
        env (str): The target environment (e.g., development, staging, production).
    
    Raises:
        subprocess.CalledProcessError: If the deployment command fails.
    """
    deploy_command = ["deploy-script", "--env", env]  # Placeholder for the actual deployment command
    try:
        print(f"Deploying to {env} environment...")
        subprocess.run(deploy_command, check=True)
        print(f"Deployment to {env} environment completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to deploy to {env}. Error: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    """
    Main function to update code and deploy to multiple environments.
    """
    environments = ['development', 'staging', 'production']  # Predefined environments for deployment
    
    # Update code repository
    update_code()

    # Deploy to each environment sequentially
    for env in environments:
        deploy_to_environment(env)

if __name__ == "__main__":
    main()
