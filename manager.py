#!/usr/bin/env python3

import hashlib
import os
from contextlib import contextmanager
from pathlib import Path

import jinja2
import yaml
from conda_lock import conda_lock

DOCKER_REPOSITORY = 'anibali/pytorch'


@contextmanager
def chdir(path):
  old_dir = os.getcwd()
  os.chdir(path)
  yield
  os.chdir(old_dir)


def main():
  # Directory for GitHub Actions workflow configuration files.
  workflow_dir = Path('.github', 'workflows')
  workflow_dir.mkdir(parents=True, exist_ok=True)

  # Delete existing build-and-push workflows.
  for old_workflow_path in workflow_dir.glob('publish_*.yml'):
    old_workflow_path.unlink()

  # Template file for Docker build and push workflows.
  workflow_template_path = Path('publish_workflow.yml.jinja2')
  workflow_template = jinja2.Template(workflow_template_path.read_text(encoding='utf-8'),
                                      keep_trailing_newline=True)

  # Read Docker image configurations.
  images = yaml.safe_load(Path('images.yml').read_text(encoding='utf-8'))

  for image_id, image_opts in images.items():
    if image_opts.get('deprecated', False):
      continue

    print(f'> Processing {image_id}...')

    tags = [image_id] + image_opts.get('extra_tags', [])
    conda_chans = image_opts['template'].get('conda_channels', None)
    conda_deps = image_opts['template'].get('conda_dependencies', None)
    template_path = Path(image_opts['template']['path'])
    template_vars = image_opts['template'].get('vars', {})

    template = jinja2.Template(template_path.read_text(encoding='utf-8'),
                               keep_trailing_newline=True)

    dockerfile_dir = Path('dockerfiles', image_id)
    dockerfile_dir.mkdir(parents=True, exist_ok=True)

    dockerfile_path = dockerfile_dir.joinpath('Dockerfile')
    dockerfile_content = template.render(**template_vars)
    dockerfile_path.write_text(dockerfile_content, encoding='utf-8')

    if conda_deps is not None:
      conda_env = {}
      conda_env['name'] = 'base'
      if conda_chans is not None:
        conda_env['channels'] = conda_chans
      conda_env['dependencies'] = conda_deps
      conda_env_path = dockerfile_dir.joinpath('environment.yml').absolute()
      conda_env_contents = yaml.safe_dump(conda_env, sort_keys=False)
      conda_env_path.write_text(conda_env_contents)

      if image_opts['template'].get('conda_lock', True):
        conda_lock_path = dockerfile_dir.joinpath('conda-linux-64.lock')

        env_hash = hashlib.sha256(conda_env_contents.encode('utf-8')).hexdigest()

        # Read the previously stored version of the hash, if present.
        old_env_hash = None
        digest_line_start = '# env_hash: '
        if conda_lock_path.is_file():
          for line in conda_lock_path.read_text().splitlines():
            if line.startswith(digest_line_start):
              old_env_hash = line[len(digest_line_start):]

        # Only generate a new lock file when environment.yml changes. To force creating a new lock
        # file, delete the old one.
        should_update_lock_file = env_hash != old_env_hash
        if should_update_lock_file:
          with chdir(dockerfile_dir):
            # This creates conda-linux-64.lock.
            conda_lock.run_lock([conda_env_path], conda_exe=None, platforms=['linux-64'],
                                kinds=['explicit'])

        conda_lock_lines = conda_lock_path.read_text().splitlines()

        if should_update_lock_file:
          # Insert our hash of environment.yml into conda-linux-64.lock.
          insert_index = 0
          for line in conda_lock_lines:
            if not line.startswith('#'):
              break
            insert_index += 1
          conda_lock_lines.insert(insert_index, digest_line_start + env_hash)

        # Comment out packages that we do not want to install.
        exclude_conda_packages = image_opts['template'].get('exclude_conda_packages', [])
        for i in range(len(conda_lock_lines)):
          line = conda_lock_lines[i]
          if not line.startswith('#'):
            for package in exclude_conda_packages:
              if package in line:
                conda_lock_lines[i] = '# ' + line
                break

        conda_lock_path.write_text('\n'.join(conda_lock_lines))

    # Save workflow for automated builds using GitHub Actions.
    workflow_path = workflow_dir.joinpath(f'publish_{image_id}.yml')
    workflow_content = workflow_template.render(
      image_id=image_id,
      repository=DOCKER_REPOSITORY,
      tags=tags,
      dockerfile_dir=str(dockerfile_dir),
      workflow_file=str(workflow_path),
    )
    workflow_path.write_text(workflow_content, encoding='utf-8')


if __name__ == '__main__':
  main()
