#!/usr/bin/env python3

import jenkins
import argparse
import sys
import json
import os
from typing import Optional

class JenkinsCLI:
    def __init__(self, url: str, username: str, password: str):
        """Initialize Jenkins connection."""
        try:
            self.server = jenkins.Jenkins(url, username=username, password=password)
            self.server.get_whoami()  # Test connection
        except Exception as e:
            print(f"Error connecting to Jenkins: {str(e)}")
            sys.exit(1)

    def list_jobs(self) -> None:
        """List all jobs in Jenkins."""
        try:
            jobs = self.server.get_all_jobs()
            print("\nAvailable Jenkins Jobs:")
            print("-" * 50)
            for job in jobs:
                print(f"Name: {job['name']}")
                print(f"URL: {job['url']}")
                print(f"Color (Status): {job['color']}")
                print("-" * 50)
        except Exception as e:
            print(f"Error listing jobs: {str(e)}")

    def get_job_info(self, job_name: str) -> None:
        """Get detailed information about a specific job."""
        try:
            job_info = self.server.get_job_info(job_name)
            print(f"\nJob Details for {job_name}:")
            print("-" * 50)
            print(f"Description: {job_info.get('description', 'N/A')}")
            print(f"URL: {job_info.get('url', 'N/A')}")
            print(f"Buildable: {job_info.get('buildable', False)}")
            print(f"Last Build: {job_info.get('lastBuild', {}).get('number', 'N/A')}")
            print(f"In Queue: {job_info.get('inQueue', False)}")
            print("-" * 50)
        except Exception as e:
            print(f"Error getting job info: {str(e)}")

    def build_job(self, job_name: str, parameters: Optional[dict] = None) -> None:
        """Trigger a build for a specific job."""
        try:
            if parameters:
                self.server.build_job(job_name, parameters=parameters)
            else:
                self.server.build_job(job_name)
            print(f"Successfully triggered build for job: {job_name}")
        except Exception as e:
            print(f"Error triggering build: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Jenkins CLI Tool for Jenkins')
    parser.add_argument('--username', help='Jenkins username (or set JENKINS_USERNAME env variable)')
    parser.add_argument('--token', help='Jenkins API token (or set JENKINS_TOKEN env variable)')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # List jobs command
    subparsers.add_parser('list', help='List all Jenkins jobs')
    
    # Job info command
    info_parser = subparsers.add_parser('info', help='Get job information')
    info_parser.add_argument('job_name', help='Name of the job')
    
    # Build job command
    build_parser = subparsers.add_parser('build', help='Trigger a job build')
    build_parser.add_argument('job_name', help='Name of the job to build')
    build_parser.add_argument('--parameters', help='JSON string of build parameters')

    args = parser.parse_args()

    username = args.username or os.environ.get('JENKINS_USERNAME')
    token = args.token or os.environ.get('JENKINS_TOKEN')
    jenkins_url = os.environ.get('JENKINS_URL', 'http://localhost:8080')

    if not username or not token:
        print("Error: Jenkins username and token must be provided either as arguments or environment variables")
        sys.exit(1)

    jenkins_cli = JenkinsCLI(jenkins_url, username, token)

    if args.command == 'list':
        jenkins_cli.list_jobs()
    elif args.command == 'info':
        jenkins_cli.get_job_info(args.job_name)
    elif args.command == 'build':
        parameters = json.loads(args.parameters) if args.parameters else None
        jenkins_cli.build_job(args.job_name, parameters)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
