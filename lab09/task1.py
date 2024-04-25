import netifaces

data = netifaces.ifaddresses('en0')[netifaces.AF_INET][0]
print('ip address =', data['addr'])
print('network mask =', data['netmask'])