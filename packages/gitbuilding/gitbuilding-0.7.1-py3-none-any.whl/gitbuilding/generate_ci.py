import os
import sys
import pathlib

RECOMMENDED_PYTHON_VERSION = "3.7"


def generate_ci():
    """
    Outputs CI files
    """
    print("This will generate the necessary files to publish your documentation as a"
        "website on Gitlab, Github or Netlify.\n")

    ans = input(PROMPT)

    try:
        ans = int(ans)
        if ans > 3 or ans < 1:
            raise ValueError()
    except ValueError:
        print(f'Answer "{ans}" is not understood.')
        sys.exit(1)

    if ans == 1:
        path = ".gitlab-ci.yml"
        if os.path.exists(path):
            print(f"Error: {path} already exists. Not overwriting it.")
            sys.exit(1)
        else:
            write_file(path, GITLAB_CI_YAML_CONTENTS)

    elif ans == 2:
        folder = ".github/workflows/"
        path = os.path.join(folder, "gitbuilding.yml")
        if os.path.exists(path):
            print(f"Error: {path} already exists. Not overwriting it.")
            sys.exit(1)
        else:
            # equivalent to mkdir -p, tries to make the folder but doesn't
            # error if it's already there
            pathlib.Path(folder).mkdir(parents=True, exist_ok=True)

            write_file(path, GITHUB_ACTION_YAML_CONTENTS)

    elif ans == 3:
        path_txt = "runtime.txt"
        path_toml = "netlify.toml"
        if os.path.exists(path_txt):
            print(f"{path_txt} already exists. Not overwriting it.")
        else:
            write_file(path_txt, RECOMMENDED_PYTHON_VERSION + "\n")
        if os.path.exists(path_toml):
            print(f"Error: {path_toml} already exists. Not overwriting it.")
            sys.exit(1)
        else:
            write_file(path_toml, NETLIFY_TOML_CONTENTS)


def write_file(path, contents):
    with open(path, "w") as file_obj:
        file_obj.write(contents)
    print(f"Generated {path}")


PROMPT = '''Which hosting service do you want to use?

1. Gitlab Pages
2. Github Pages
3. Netlify

Enter a number: '''


GITLAB_CI_YAML_CONTENTS =  '''
image: "python:''' + RECOMMENDED_PYTHON_VERSION + '''"
before_script:
  - python --version
  - pip install gitbuilding

pages:
  stage: deploy
  script:
  - gitbuilding build-html
  - mv _site public
  artifacts:
    paths:
    - public
  only:
  - master
'''

GITHUB_ACTION_YAML_CONTENTS = '''
name: Deploy Gitbuilding Project to Github Pages

on: [push]

jobs:
  build_and_deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install Python 3
        uses: actions/setup-python@v1
        with:
          python-version:''' + RECOMMENDED_PYTHON_VERSION + '''
      - name: Build
        run: |
          pip install gitbuilding
          gitbuilding build-html
      - name: Deploy
        uses: JamesIves/github-pages-deploy-action@3.6.1
        with:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          BRANCH: gh-pages
          FOLDER: _site/
          # Automatically remove deleted files from the deploy branch
          CLEAN: true
'''

NETLIFY_TOML_CONTENTS = '''
[build]
  command = "pip3 install gitbuilding && gitbuilding build-html"
  publish = "_site/"
'''
