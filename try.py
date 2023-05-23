import configparser
import os, oracledb, getpass, argparse, sys
import time
# from aio_pika import logger
# from typing import Self
# from flask import request
from rasa_sdk import Tracker
from configparser_crypt import ConfigParserCrypt
from cryptography.fernet import Fernet
import requests,json
import logging
from typing import Any, Text, Dict, List


# class jsonConversion:
#     def __init__(self):
#         self.connection=None

# #         config = configparser.ConfigParser()
# #         configFile = 'oracle.ini'
# #         config.read(configFile)
# #         try:
# #             #get the db connection details from config file
# #             user = config.get('database','user')
# #             pwd = config.get('database','pwd')
# #             port = config.get('database','port')
# #             sn = config.get('database','service_name')
# #             dsn = config.get('database','dsn')
# #             self.connection = oracledb.connect(user=user, password=pwd, dsn=dsn)
# #             #print(user, pwd, dsn);
# #         except oracledb.DatabaseError as e:
# #             raise
# #         except Exception as e:
# #             raise
#         with open('encrypted_config.ini', 'r') as encrypted_file:
#             encrypted_config = encrypted_file.read()

#         # Generate a secret key for decryption
#         secret_key = Fernet.generate_key()

#         # Create a Fernet cipher using the secret key
#         cipher = Fernet(secret_key)

#         # Decrypt the configuration string
#         decrypted_config = cipher.decrypt(encrypted_config.encode()).decode()

#         # Convert the decrypted configuration string back to a configparser object
#         decrypted_config_parser = configparser.ConfigParser()
#         decrypted_config_parser.read_string(decrypted_config)

#         try:
#             # Get the db connection details from the decrypted configuration
#             user = decrypted_config_parser.get('database', 'user')
#             pwd = decrypted_config_parser.get('database', 'pwd')
#             port = decrypted_config_parser.get('database', 'port')
#             sn = decrypted_config_parser.get('database', 'service_name')
#             dsn = decrypted_config_parser.get('database', 'dsn')
#             self.connection = oracledb.connect(user=user, password=pwd, dsn=dsn)
#         except oracledb.DatabaseError as e:
#             raise
#         except Exception as e:
#             raise

#     def CheckConn(self):
#         cur=None
#         try:
#             cur = self.connection.cursor()
#             cur.execute("""
#             select 'Connection Succeded' from dual
#             """)
#             output = {}
#             for text in cur:
#                 output['Connect Status'] = text[0]
#             return output

#         except Exception as e:
#             raise
#         finally:
#             if cur is None:
#                 cur.close()

#     # def order_details_prev_api(self):
#     #     # prev_item=tracker.get_slot('item')
#     #     prev_item=input('enter item no:')


#     #     url = 'http://192.168.161.85:8000/order'
#     #     # 'http://192.168.161.85:8000/order' -- to previous item order details
#     #     headers = {'Content-Type': 'application/json'}
#     #     data = {"item": prev_item}
#     #     response = requests.post(url, headers=headers, json=data)
        
#     #     json_data = json.loads(response.json())
#     #     dict=json.dumps(json_data)
#     #     # print(json_data)
#     #     # print(type(dict))
#     #     if json_data is None:
#     #         return("Sorry, the item number you provided has no order in approved status. Can you provide the correct item number?")
#     #     # else:
#     #     output = ''
#     #     # dictionary=json_data[0]
#     #     for dictionary in json_data:
#     #             # dictionary=json_data[0]
#     #         # if isinstance(dictionary, dict):
#     #             order_no = dictionary['ORDER_NO']
#     #             item = dictionary['ITEM']
#     #             supplier = dictionary['SUPPLIER']
#     #             location = dictionary['LOCATION']
#     #             loc_type = dictionary['LOC_TYPE']
#     #             department=dictionary['DEPT']
#     #             item_desc=dictionary['ITEM_DESC']
                
#     #             # quantity_ordered = dictionary['QTY_ORDERED']
#     #             # quantity_received = dictionary['QTY_RECEIVED']
#     #             output += f"order no:{order_no}\nitem:{item}\nsupplier:{supplier}\nlocation:{location}\nloc_type:{loc_type}\ndepartment:{department}\nitem_description:{item_desc}\n\n"
                
        
#     #     return output
#     def order_details_prev_api(self):
#         # prev_item = tracker.get_slot('item')
#         prev_item=input('enter item no:')

#         url = 'http://192.168.161.85:8000/order'
#         headers = {'Content-Type': 'application/json'}
#         data = {"item": prev_item}
#         response = requests.post(url, headers=headers, json=data)

#         # if response.status_code != 200:
#         #     return "wrong_item_number"

#         try:
#             json_data = json.loads(response.json())
#         except json.JSONDecodeError:
#             return "wrong_item_number"

#         if not json_data or not isinstance(json_data, list):
#             return "wrong_item_number"

#         output = ''
#         for dictionary in json_data:
#             order_no = dictionary.get('ORDER_NO')
#             item = dictionary.get('ITEM')
#             supplier = dictionary.get('SUPPLIER')
#             location = dictionary.get('LOCATION')
#             loc_type = dictionary.get('LOC_TYPE')
#             department = dictionary.get('DEPT')
#             item_desc = dictionary.get('ITEM_DESC')
#             output += f"order no: {order_no}\nitem: {item}\nsupplier: {supplier}\nlocation: {location}\nloc_type: {loc_type}\ndepartment: {department}\nitem_description: {item_desc}\n\n"

#         return output

# res=jsonConversion()
# out=res.order_details_prev_api()
# print(out)

def call_chatgpt_api( user_input: Text) -> Text:
        # user_input = tracker.get_slot('user_input')
        # api_key="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"
        api_key = "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"
        # def get_chatgpt_response(self, message):
        url = 'https://api.openai.com/v1/chat/completions'

        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'model': "gpt-3.5-turbo",
            'messages': [   {'role': 'system', 'content': 'You are an AI assistant for the user. You help to solve user query'},
                            {'role': 'user', 'content': 'You: ' + user_input}
                            ],
            'max_tokens': 100
        }
        response = requests.post(url, headers=headers, json=data)
                # response = requests.post(api_url, headers=headers, json=data)

        if response.status_code == 200:
            chatgpt_response = response.json()
            message = chatgpt_response['choices'][0]['message']['content']
            return message
        # elif response.status_code == 429:
        # # Retry with exponential backoff
        #     # time.sleep(1)  # Wait for 1 second before retrying
        #     return self.call_chatgpt_api(user_input)
        else:
            error_message = f"ChatGPT API request failed with status code: {response.status_code}"
            return error_message
            # dispatcher.utter_message(message)
        # else:
        #     # Handle error
        #     return "Sorry, I couldn't generate a response at the moment. Please try again later."
    
# res=jsonConversion()

# out=call_chatgpt_api('define stock ledger')
# print(out)
user_input = "what is climate change"
response =call_chatgpt_api(user_input)
print(response)






