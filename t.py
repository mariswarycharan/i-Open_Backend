import subprocess

# Function to run a git command
def run_git_command(cmd):
    try:
        # Run the command and wait for it to complete
        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Return the standard output from the command
        return result.stdout
    except subprocess.CalledProcessError as e:
        # If an error occurs, print the error message and return None
        print(f"An error occurred while running the command: {e.stderr}")
        return None

# Example usage of the function to run git verify-pack
output = run_git_command(['git', 'verify-pack', '-v', 'D:/i-Open/.git/objects/pack/pack-*.idx'])
if output:
    print(output)