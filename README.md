### TradfriAPI
## A API to control IKEA Trådfri on LAN or WAN

Prerequisites: 
Install libcoap using
```
sudo apt-get install build-essential autoconf automake libtool
git clone --recursive https://github.com/obgm/libcoap.git
cd libcoap
git checkout dtls
git submodule update --init --recursive
./autogen.sh
./configure --disable-documentation --disable-shared
make
sudo make install
```
Install tqdm with the following commands:
```
sudo apt-get install python-pip
sudo pip install tqdm
```

Clone this project:
```
git clone https://github.com/AcollaMolla/TradfriAPI
```

Create configuration file:
```
nano tradfri.cfg
```
The tradfri.cfg must contain the following:
```
[tradfri]
hubip = [TRADFRI HUB IP ADDRESS]
userid = [ARBITRARY USERNAME]
apikey = [GENERATED KEY]
[cookie]
cookiename = [NAME OF COOKIE]
cookievalue = [COOKIE VALUE]
```
# Run the server: #
```
python server.py
```
