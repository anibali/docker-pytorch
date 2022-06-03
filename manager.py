#!/usr/bin/env python3

import jinja2
import yaml
from pathlib import Path


DOCKER_REPOSITORY = 'anibali/pytorch'


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
      conda_env_path = dockerfile_dir.joinpath('environment.yml')
      with conda_env_path.open('w') as f:
        yaml.safe_dump(conda_env, f, sort_keys=False)

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
