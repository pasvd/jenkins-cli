#!/bin/zsh

# Export Jenkins configuration as environment variables
export JENKINS_URL="http://localhost:8080"
export JENKINS_USERNAME="<username>"
export JENKINS_TOKEN="<token>"

# Create a function for handling the jenkins-cli commands
jenkins-cli() {
    local original_dir=$PWD
    cd ~/Work/jenkins-cli
    asdf exec python jenkins_api.py "$@"
    cd "$original_dir"
}

# Example usage with alias:
# jenkins-cli list
# jenkins-cli info job-name
# jenkins-cli build job-name
