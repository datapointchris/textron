# ===== USER INPUT ===== #

# Specify the repo to use for installation
repo=$"https://github.com/DataPointChris/reddit_nlp.git"

# ====================== #

# Install Python build dependencies
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
libncursesw5-dev xz-utils tk-dev liblzma-dev

# Clone repo
cd ~/
git clone $repo && echo "Successfully Cloned" || echo "Cloning FAIL"

# Get project name
project=$(basename "$repo" ".${repo##*.}")
echo "Project name:" $project

# Get Python version number from Pipfile
python_version=$(egrep -o "([0-9]{1,}\.)+[0-9]{1,}" reddit_nlp/Pipfile)
echo "Pipfile specifies Python" $python_version

# Download and build Python version that matches the Pipfile.lock
cd ~/
wget https://www.python.org/ftp/python/$python_version/Python-$python_version.tgz
tar xvf Python-$python_version.tgz
cd Python-$python_version
./configure 
# --enable-optimizations
make -j 8
sudo make altinstall

# Install pip
sudo apt-get install -y python3-pip

# Install Pipenv (upgrade only to get newest version that has faster locking)
sudo -H pip3 install --pre --upgrade pipenv

# Create virtual environment and install Python
cd ~/$project
pipenv --python $python_version

# Install project dependencies
# Make sure to use sync for deterministic build (NOT install)
yes y | pipenv sync
