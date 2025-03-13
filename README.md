# Jenkins CLI Tool

Simple command-line interface for interacting with Jenkins server.

## Requirements

- Python 3.11.7 (specified in .tool-versions for asdf)

## Installation

1. Install Python using asdf:
```bash
asdf install
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install requirements:
```bash
pip install -r requirements.txt
```

## Configuration

### Method 1: Alias Configuration
You can use aliases for your frequently used jobs and their parameters. The configuration is stored in `~/.jenkins-cli.yaml`.

1. Generate default configuration:
```bash
./jenkins_api.py init-config
```

This will create a config file with an example alias:
```yaml
aliases:
  deploy-app:
    job_name: DEPLOY_my_application
    parameters:
      TASK: deploy
      GIT_SYMBOL: origin/master
    options:
      progress: true
```

Now you can use the alias instead of the full job name and parameters:
```bash
jenkins-cli build deploy-app  # This will use the configured job name and parameters
```

You can still override parameters from command line:
```bash
jenkins-cli build deploy-app --parameters '{"TASK": "restart"}'
```

### Method 2: Environment Variables
You can set your Jenkins configuration as environment variables:
```bash
export JENKINS_URL="your Jenkins URL"  # Optional, defaults to this URL 
export JENKINS_USERNAME="your-username"
export JENKINS_TOKEN="your-api-token"
```

### Method 2: ZSH Configuration
A convenience script `jenkins.zsh` is provided that sets up the environment variables and creates an alias:

1. Edit the credentials in `jenkins.zsh`:
```bash
vim jenkins.zsh  # Set your username and token
```

2. Source the file in your `.zshrc`:
```bash
echo "source $HOME/Desktop/jenkins-cli/jenkins.zsh" >> ~/.zshrc
source ~/.zshrc
```

3. Now you can use the `jenkins-cli` alias:
```bash
jenkins-cli list  # Lists all jobs
jenkins-cli info job-name  # Gets job info
jenkins-cli build job-name  # Triggers a build
```

## Usage

### Method 1: Using Command Line Arguments
```bash
# List all jobs
./jenkins_api.py --username your-username --token your-api-token list

# Get job info
./jenkins_api.py --username your-username --token your-api-token info job-name

# Build job
./jenkins_api.py --username your-username --token your-api-token build job-name
```

### Method 2: Using Environment Variables
```bash
# After setting JENKINS_USERNAME and JENKINS_TOKEN
./jenkins_api.py list
./jenkins_api.py info job-name
./jenkins_api.py build job-name
```

### Method 3: Using ZSH Alias
```bash
# After sourcing jenkins.zsh
jenkins-cli list
jenkins-cli info job-name
jenkins-cli build job-name
```

### Full Command Reference

#### List all Jenkins jobs
```bash
./jenkins_api.py --username your-username --token your-api-token list
```

### Get job information
```bash
./jenkins_api.py --username your-username --token your-api-token info job-name
```

### Trigger a job build
Without parameters:
```bash
./jenkins_api.py --username your-username --token your-api-token build job-name
```

With parameters:
```bash
./jenkins_api.py --username your-username --token your-api-token build job-name --parameters '{"param1": "value1"}'
```

With console output streaming:
```bash
./jenkins_api.py --username your-username --token your-api-token build job-name --stream
```

With build progress bar:
```bash
./jenkins_api.py --username your-username --token your-api-token build job-name --progress
```

With both console output and progress bar:
```bash
./jenkins_api.py --username your-username --token your-api-token build job-name --stream --progress
```

With parameters and monitoring:
```bash
./jenkins_api.py --username your-username --token your-api-token build job-name --parameters '{"param1": "value1"}' --stream --progress
```

## Examples

1. List all available jobs:
```bash
./jenkins_api.py --username john.doe --token 11aa22bb33cc list
```

2. Get information about specific job:
```bash
./jenkins_api.py --username john.doe --token 11aa22bb33cc info my-build-job
```

3. Trigger a parameterized build:
```bash
./jenkins_api.py --username john.doe --token 11aa22bb33cc build deployment-job --parameters '{"environment": "staging", "version": "1.2.3"}'
```

4. Trigger a build with progress monitoring:
```bash
./jenkins_api.py --username john.doe --token 11aa22bb33cc build my-build-job --progress
```

5. Trigger a build with console output streaming:
```bash
./jenkins_api.py --username john.doe --token 11aa22bb33cc build my-build-job --stream
```

