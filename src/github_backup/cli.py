"""Command-line interface for GitHub backup tool."""

import os
import sys
import json
import click
from pathlib import Path
from typing import Optional, List

from .backup_manager import BackupManager
from . import __version__


@click.group()
@click.version_option(__version__)
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.pass_context
def cli(ctx, verbose):
    """GitHub Repository Backup Tool
    
    A tool for backing up GitHub repositories to Dropbox.
    """
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    
    if verbose:
        import logging
        logging.basicConfig(level=logging.INFO)


@cli.command()
@click.option('--github-token', envvar='GITHUB_TOKEN', 
              help='GitHub personal access token (or set GITHUB_TOKEN env var)')
@click.option('--dropbox-token', envvar='DROPBOX_ACCESS_TOKEN',
              help='Dropbox access token (or set DROPBOX_ACCESS_TOKEN env var)')
@click.option('--backup-folder', default='/Projects',
              help='Dropbox folder for backups (default: /Projects)')
@click.option('--username', help='GitHub username (default: authenticated user)')
@click.option('--exclude', multiple=True, help='Repository names to exclude (can be used multiple times)')
@click.option('--include-private/--no-private', default=True,
              help='Include private repositories (default: True)')
@click.option('--output', type=click.Path(), help='Output results to JSON file')
@click.pass_context
def backup_all(ctx, github_token, dropbox_token, backup_folder, username, exclude, include_private, output):
    """Backup all repositories for a user."""
    try:
        backup_manager = BackupManager(
            github_token=github_token,
            dropbox_token=dropbox_token,
            backup_folder=backup_folder
        )
        
        click.echo(f"Starting backup for user: {username or 'authenticated user'}")
        click.echo(f"Backup folder: {backup_folder}")
        
        if exclude:
            click.echo(f"Excluding repositories: {', '.join(exclude)}")
        
        results = backup_manager.backup_all_repositories(
            username=username,
            exclude_repos=list(exclude),
            include_private=include_private
        )
        
        # Display results
        click.echo("\n" + "="*50)
        click.echo("BACKUP RESULTS")
        click.echo("="*50)
        click.echo(f"Total repositories: {results['total_repos']}")
        click.echo(f"Successful backups: {results['successful_backups']}")
        click.echo(f"Failed backups: {results['failed_backups']}")
        click.echo(f"Skipped repositories: {results['skipped_repos']}")
        
        if results['failed_backups'] > 0:
            click.echo("\nFailed repositories:")
            for detail in results['backup_details']:
                if not detail['success']:
                    click.echo(f"  - {detail['repo_name']}")
        
        # Save results to file if requested
        if output:
            with open(output, 'w') as f:
                json.dump(results, f, indent=2)
            click.echo(f"\nResults saved to: {output}")
        
        # Exit with error code if any backups failed
        if results['failed_backups'] > 0:
            sys.exit(1)
            
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('repositories', nargs=-1, required=True)
@click.option('--github-token', envvar='GITHUB_TOKEN',
              help='GitHub personal access token (or set GITHUB_TOKEN env var)')
@click.option('--dropbox-token', envvar='DROPBOX_ACCESS_TOKEN',
              help='Dropbox access token (or set DROPBOX_ACCESS_TOKEN env var)')
@click.option('--backup-folder', default='/Projects',
              help='Dropbox folder for backups (default: /Projects)')
@click.option('--username', help='GitHub username (default: authenticated user)')
@click.option('--output', type=click.Path(), help='Output results to JSON file')
@click.pass_context
def backup_repos(ctx, repositories, github_token, dropbox_token, backup_folder, username, output):
    """Backup specific repositories by name."""
    try:
        backup_manager = BackupManager(
            github_token=github_token,
            dropbox_token=dropbox_token,
            backup_folder=backup_folder
        )
        
        click.echo(f"Starting backup for repositories: {', '.join(repositories)}")
        click.echo(f"Backup folder: {backup_folder}")
        
        results = backup_manager.backup_specific_repositories(
            repo_names=list(repositories),
            username=username
        )
        
        # Display results
        click.echo("\n" + "="*50)
        click.echo("BACKUP RESULTS")
        click.echo("="*50)
        click.echo(f"Requested repositories: {results['requested_repos']}")
        click.echo(f"Successful backups: {results['successful_backups']}")
        click.echo(f"Failed backups: {results['failed_backups']}")
        click.echo(f"Not found repositories: {results['not_found_repos']}")
        
        if results['failed_backups'] > 0:
            click.echo("\nFailed repositories:")
            for detail in results['backup_details']:
                if not detail['success']:
                    click.echo(f"  - {detail['repo_name']}: {detail.get('error', 'Unknown error')}")
        
        # Save results to file if requested
        if output:
            with open(output, 'w') as f:
                json.dump(results, f, indent=2)
            click.echo(f"\nResults saved to: {output}")
        
        # Exit with error code if any backups failed
        if results['failed_backups'] > 0 or results['not_found_repos'] > 0:
            sys.exit(1)
            
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--github-token', envvar='GITHUB_TOKEN',
              help='GitHub personal access token (or set GITHUB_TOKEN env var)')
@click.option('--username', help='GitHub username (default: authenticated user)')
def list_repos(github_token, username):
    """List all repositories for a user."""
    try:
        from .github_client import GitHubClient
        
        client = GitHubClient(github_token)
        repos = client.get_user_repositories(username)
        
        click.echo(f"Repositories for {username or 'authenticated user'}:")
        click.echo("="*50)
        
        for repo in repos:
            privacy = "private" if repo.private else "public"
            size_mb = repo.size / 1024 if repo.size > 0 else 0
            click.echo(f"{repo.name:<30} ({privacy:<7}) {size_mb:>6.1f} MB")
        
        click.echo(f"\nTotal: {len(repos)} repositories")
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == '__main__':
    main()
