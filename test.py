import subprocess
import sys

def deploy_to_environment(environment):
    # Define the deployment steps for each environment
    deployment_steps = {
        'staging': ['git pull origin staging', 'pip install -r requirements.txt', 'restart staging server'],
        'production': ['git pull origin master', 'pip install -r requirements.txt', 'restart production server']
    }

    # Execute each deployment step
    for step in deployment_steps[environment]:
        try:
            # Running the deployment command
            subprocess.run(step, check=True, shell=True)
            print(f"Successfully completed step: {step}")
        except subprocess.CalledProcessError as e:
            # Log the error and exit if a step fails
            print(f"Failed to complete step: {step}", file=sys.stderr)
            print(e, file=sys.stderr)
            sys.exit(1)
    print(f"Deployment to {environment} completed successfully.")

# The environments we want to deploy to
environments = ['staging', 'production']

# Run the deployment
for env in environments:
    print(f"Starting deployment to {env}...")
    deploy_to_environment(env)