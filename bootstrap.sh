# Install build tools
yum update -y
yum groupinstall -y "Development tools"
yum install -y zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel

# Install Python3.4
wget https://www.python.org/ftp/python/3.4.0/Python-3.4.0.tar.xz
tar xf Python-3.4.0.tar.xz
cd Python-3.4.0
./configure --prefix=/usr --enable-shared LDFLAGS="-Wl,-rpath /usr/lib"
make && make altinstall

# Install MongoDB
echo "[mongodb]
name=MongoDB Repository
baseurl=http://downloads-distro.mongodb.org/repo/redhat/os/x86_64/
gpgcheck=0
enabled=1" >> /etc/yum.repos.d/mongodb.repo
yum -y install mongodb-org
service mongod start
chkconfig mongod on

# Install virtualenv and necessary dependencies
cd /vagrant
python3.4 setup.py install

yum install libxslt-devel libxml2-devel -y