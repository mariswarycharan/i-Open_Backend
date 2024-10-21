import subprocess
import sys

# Define deployment environments
environments = ['development', 'staging', 'production']

def deploy_to_environment(env):
    """Deploys the latest code to the specified environment."""
    # Replace this command with your actual deployment commands
    deploy_command = f"deploy-script --env {env}"
    try:
        print(f"Deploying to {env}...")
        subprocess.run(deploy_command.split(), check=True)
        print(f"Successfully deployed to {env}!")
    except subprocess.CalledProcessError as e:
        print(f"Failed to deploy to {env}. Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Update code repository (e.g., git pull)
    # Replace with actual update command
    update_command = "git pull origin main"
    try:
        print("Updating code repository...")
        subprocess.run(update_command.split(), check=True)
    except subprocess.CalledProcessError as e:
        print("Failed to update code repository. Error: {e}")
        sys.exit(1)
    
    # Deploy to each environment
    for env in environments:
        deploy_to_environment(env)