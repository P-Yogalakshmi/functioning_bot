# import configparser
# from configparser_crypt import ConfigParserCrypt
# # import base64
# # from cryptography.fernet import Fernet

# config = configparser.ConfigParser()
# config['database'] = {
#     'user': 'ranjith',
#     'pwd': 'ranjith2022',
#     'port': '1521',
#     'service_name': 'RMSDEV',
#     'host': '192.168.161.200',
#     'dsn': '192.168.161.200/RMSDEV'
# }

# # configparser = configparser.ConfigParser()
# config_crypt = ConfigParserCrypt()
# config_crypt.generate_key()
# key = config_crypt.aes_key
# # print(key)
# # config['database'] = {}
# # print(key)
# with open('config.encrypted', 'wb') as config_file:
#     config_crypt.write_encrypted(config_file)
#------------------------------------------------------------------------------

import configparser
from configparser_crypt import ConfigParserCrypt
from cryptography.fernet import Fernet
from io import StringIO

# Create an instance of ConfigParserCrypt
config_crypt = ConfigParserCrypt()

# Generate a secret key for encryption and decryption
secret_key = Fernet.generate_key()

# Create a sample configuration
config = configparser.ConfigParser()
config['database'] = {
    'user': 'ranjith',
    'pwd': 'ranjith2022',
    'port': '1521',
    'service_name': 'RMSDEV',
    'host': '192.168.161.200',
    'dsn': '192.168.161.200/RMSDEV'
}

# Create a Fernet cipher using the secret key
cipher = Fernet(secret_key)

# Convert the configuration to a string
config_io = StringIO()
config.write(config_io)
config_string = config_io.getvalue()

# Encrypt the configuration string
encrypted_config = cipher.encrypt(config_string.encode()).decode()

with open('secret.key', 'wb') as key_file:
    key_file.write(secret_key)

# Save the encrypted configuration to a file
with open('encrypted_config.ini', 'w') as encrypted_file:
    encrypted_file.write(encrypted_config)
#----------------------------------------------------------------------------
# Load the encrypted configuration from the file
# with open('encrypted_config.ini', 'r') as encrypted_file:
#     encrypted_config = encrypted_file.read()

# # Decrypt the configuration string
# decrypted_config = cipher.decrypt(encrypted_config.encode()).decode()

# # Convert the decrypted configuration string back to a configparser object
# decrypted_config_parser = configparser.ConfigParser()
# decrypted_config_parser.read_string(decrypted_config)

# # Access the decrypted values
# user = decrypted_config_parser['database']['user']
# password = decrypted_config_parser['database']['pwd']
# port = decrypted_config_parser['database']['port']
# service_name = decrypted_config_parser['database']['service_name']
# host = decrypted_config_parser['database']['host']
# dsn = decrypted_config_parser['database']['dsn']

# # Print the decrypted values
# print(f"User: {user}")
# print(f"Password: {password}")
# print(f"Port: {port}")
# print(f"Service Name: {service_name}")
# print(f"Host: {host}")
# print(f"DSN: {dsn}")







