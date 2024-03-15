sudo apt update

sudo apt -y install python3-pip
sudo pip3 install --upgrade pip

# install postgresql
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt -y install postgresql libpq-dev

# setup database
DATABASE="food_delivery_db"
USER="vagrant"
PASSWORD="vagrant"

sudo systemctl start postgresql.service
sudo su postgres -c "psql -c \"CREATE ROLE $USER SUPERUSER LOGIN PASSWORD '$PASSWORD'\" "
sudo su postgres -c "createdb $DATABASE"

# write database credentials to .env
sudo su vagrant
cd /vagrant/food_delivery_app
echo -e "\nDB_NAME=$DATABASE\nDB_USER=$USER\nDB_PASSWORD=$PASSWORD" >> .env

# write site domain and redis to .env
SITE_DOMAIN_NAME="https://192.168.56.10:8000"
REDIS_LOCATION="redis://127.0.0.1:6379/"

echo -e "\nSITE_DOMAIN=\"$SITE_DOMAIN_NAME\"\nREDIS_LOCATION=$REDIS_LOCATION" >> .env

# install redis and start it
sudo apt -y install redis-server
sudo systemctl restart redis-server

# install mkcert
sudo apt -y install libnss3-tools
curl -JLO "https://dl.filippo.io/mkcert/latest?for=linux/amd64"
chmod +x mkcert-v*-linux-amd64
sudo cp mkcert-v*-linux-amd64 /usr/local/bin/mkcert

# add SSL certificates
mkcert -cert-file cert.pem -key-file key.pem localhost 127.0.0.1

# pip installs
pip3 install django
pip3 install --upgrade pip
pip3 install -r /vagrant/food_delivery_app/requirements.txt

# run migrations
make migrate

# seed the data
make seed
