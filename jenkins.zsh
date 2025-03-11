#!/bin/zsh

# Export Jenkins configuration as environment variables
export JENKINS_URL="http://localhost:8080"
export JENKINS_USERNAME="<username>"
export JENKINS_TOKEN="<token>"

# Optional: Create an alias for easier usage
alias jenkins-cli="cd ~/Work/jenkins-cli && asdf exec python jenkins_api.py"

# Example usage with alias:
# jenkins-cli list
# jenkins-cli info job-name
# jenkins-cli build job-name
