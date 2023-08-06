# mattermost-utils  [![Pipeline status](https://gitlab.tech.orange/dtrs-security/devops/mattermost-utils/badges/master/pipeline.svg)](https://gitlab.tech.orange/dtrs-security/devops/mattermost-utils/commits/master) [![Coverage report](https://gitlab.tech.orange/dtrs-security/devops/mattermost-utils/badges/master/coverage.svg)](https://gitlab.tech.orange/dtrs-security/devops/mattermost-utils/commits/master)

### Requirements

- pip package manager
- python version 3.8

### Deployment on Linux
- Clone project on your local machine
```
git clone https://gitlab.tech.orange/dtrs-security/devops/mattermost-utils.git
```
## Usage

#### Build
Make sure you have the latest versions of setuptools and wheel installed:
```
python3 -m pip install --user --upgrade setuptools wheel
```
Now run this command from the same directory where setup.py is located:
```
python setup.py sdist bdist_wheel
```
This command should output a lot of text and once completed should generate two files in the dist directory:
```
dist/
  mattermost_post_utils-0.0.1-py3-none-any.whl
  mattermost_post_utils-0.0.1.tar.gz
```

#### Uploading the distribution archives

The first thing you’ll need to do is register an account on [PyPI](https://pypi.org/)

Now you’ll create a PyPI [API token](https://pypi.org/help/#apitoken) so you will be able to securely upload your project.
Go to https://test.pypi.org/manage/account/#api-tokens and create a new [API token](https://pypi.org/help/#apitoken); 
don’t limit its scope to a particular project, since you are creating a new project.

###### Don’t close the page until you have copied and saved the token — you won’t see that token again.

Now that you are registered, you can use twine to upload the distribution packages. You’ll need to install Twine:
```
python3 -m pip install --user --upgrade twine
```
Once installed, run Twine to upload all of the archives under dist:
```
python3 -m twine upload dist/*
```
You will be prompted for a username and password. For the username, use __token__. For the password, use the token value, including the pypi- prefix.

After the command completes, you should see output similar to this:
```
Uploading distributions to https://pypi.org/legacy/
Enter your username: __token__
Enter your password: <your_token>
Uploading example_pkg_YOUR_USERNAME_HERE-0.0.1-py3-none-any.whl
100%|█████████████████████| 4.65k/4.65k [00:01<00:00, 2.88kB/s]
Uploading example_pkg_YOUR_USERNAME_HERE-0.0.1.tar.gz
100%|█████████████████████| 4.25k/4.25k [00:01<00:00, 3.05kB/s]
```
Once uploaded your package should be viewable on TestPyPI, 
for example, https://pypi.org/project/example-pkg-YOUR-USERNAME-HERE

#### Installing your newly uploaded package

You can use pip to install your package and verify that it works.

```
python3 -m pip install --no-deps example-pkg-YOUR-USERNAME-HERE
```
