#!/usr/bin/env python3

import jenkins
import argparse
import sys
import json
import os
from typing import Optional, Dict, Any
from config_handler import ConfigHandler

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

    def build_job(self, job_name: str, parameters: Optional[dict] = None, stream: bool = False, progress: bool = False) -> None:
        """Trigger a build for a specific job and optionally stream its progress."""
        try:
            queue_item = None
            if parameters:
                queue_item = self.server.build_job(job_name, parameters=parameters)
            else:
                queue_item = self.server.build_job(job_name)
            
            print(f"Successfully triggered build for job: {job_name}")
            
            if stream or progress:
                print("Waiting for build to start...")
                build_number = None
                while build_number is None:
                    job_info = self.server.get_job_info(job_name)
                    if job_info['lastBuild']['number'] > job_info.get('lastCompletedBuild', {}).get('number', 0):
                        build_number = job_info['lastBuild']['number']
                    
                print(f"Build #{build_number} started")
                
                while True:
                    build_info = self.server.get_build_info(job_name, build_number)
                    if not build_info.get('building', False):
                        result = build_info.get('result', 'UNKNOWN')
                        print(f"\nBuild finished with result: {result}")
                        break
                        
                    if progress:
                        build_info = self.server.get_build_info(job_name, build_number)
                        status = build_info.get('displayName', '') or f'Build #{build_number}'
                        
                        # Get build stages if available (for pipeline jobs)
                        try:
                            stages = self.server.get_build_stages(job_name, build_number)
                            if stages:
                                completed_stages = sum(1 for stage in stages if stage.get('status') == 'SUCCESS')
                                total_stages = len(stages)
                                current_stage = next((stage['name'] for stage in stages if stage.get('status') == 'IN_PROGRESS'), None)
                                progress_value = int((completed_stages / total_stages) * 100)
                                status_text = f"{status} - {current_stage}" if current_stage else status
                                print(f"\rProgress: [{('=' * (progress_value // 2)).ljust(50)}] {progress_value}% - {status_text}", end='')
                            else:
                                # Fallback for non-pipeline jobs
                                timestamp = build_info.get('timestamp', 0)
                                current_time = int(time.time() * 1000)  # Convert to milliseconds
                                estimated_duration = build_info.get('estimatedDuration', 0)
                                
                                if estimated_duration > 0:
                                    elapsed = current_time - timestamp
                                    progress_value = min(95, int((elapsed / estimated_duration) * 100))  # Cap at 95% until complete
                                    print(f"\rProgress: [{('=' * (progress_value // 2)).ljust(50)}] {progress_value}% - {status}", end='')
                                else:
                                    print(f"\rProgress: Running... - {status}", end='')
                        except:
                            # If stages API fails, show simpler progress
                            print(f"\rProgress: Running... - {status}", end='')
                    
                    if stream:
                        console_output = self.server.get_build_console_output(job_name, build_number)
                        print(console_output)
                    
                    import time
                    time.sleep(2)  # Poll every 2 seconds
                    
        except Exception as e:
            print(f"Error with build: {str(e)}")

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
    build_parser.add_argument('job_name', help='Name of the job or alias to build')
    build_parser.add_argument('--parameters', help='JSON string of build parameters')
    build_parser.add_argument('--stream', action='store_true', help='Stream console output')
    build_parser.add_argument('--progress', action='store_true', help='Show build progress bar')

    # Init config command
    subparsers.add_parser('init-config', help='Generate default configuration file')

    args = parser.parse_args()

    username = args.username or os.environ.get('JENKINS_USERNAME')
    token = args.token or os.environ.get('JENKINS_TOKEN')
    jenkins_url = os.environ.get('JENKINS_URL', 'http://localhost:8080')

    if not username or not token:
        print("Error: Jenkins username and token must be provided either as arguments or environment variables")
        sys.exit(1)

    jenkins_cli = JenkinsCLI(jenkins_url, username, token)

    config_handler = ConfigHandler()

    if args.command == 'list':
        jenkins_cli.list_jobs()
    elif args.command == 'info':
        jenkins_cli.get_job_info(args.job_name)
    elif args.command == 'build':
        # Check if job_name is an alias
        alias_config = config_handler.get_job_config(args.job_name)
        if alias_config:
            job_name = alias_config['job_name']
            parameters = alias_config.get('parameters', {})
            if args.parameters:
                # Merge with user provided parameters
                parameters.update(json.loads(args.parameters))
            
            options = alias_config.get('options', {})
            stream = args.stream or options.get('stream', False)
            progress = args.progress or options.get('progress', False)
        else:
            job_name = args.job_name
            parameters = json.loads(args.parameters) if args.parameters else None
            stream = args.stream
            progress = args.progress
        
        jenkins_cli.build_job(job_name, parameters, stream, progress)
    elif args.command == 'init-config':
        config_handler.generate_default_config()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
