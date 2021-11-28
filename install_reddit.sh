# ===== USER INPUT ===== #

# Specify the repo to use for installation
repo=$"https://github.com/DataPointChris/reddit_nlp.git"

# ====================== #

# Prerequesites for Pyenv 
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git python3-pip

# Install Pyenv
curl https://pyenv.run | bash

# Add Pyenv to the path
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc

source ~/.bashrc

# Install Pipenv (upgrade only to get newest version that has faster locking)
sudo -H pip3 install --pre --upgrade pipenv

# Clone repo
cd ~/
git clone $repo && echo "Successfully Cloned" || echo "Cloning FAIL"

# Get project name
project=$(basename "$repo" ".${repo##*.}")
echo "Project name:" $project

cd $project
yes y | pipenv sync