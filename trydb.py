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


class jsonConversion:
    def __init__(self):
        self.connection=None

#         config = configparser.ConfigParser()
#         configFile = 'oracle.ini'
#         config.read(configFile)
#         try:
#             #get the db connection details from config file
#             user = config.get('database','user')
#             pwd = config.get('database','pwd')
#             port = config.get('database','port')
#             sn = config.get('database','service_name')
#             dsn = config.get('database','dsn')
#             self.connection = oracledb.connect(user=user, password=pwd, dsn=dsn)
#             #print(user, pwd, dsn);
#         except oracledb.DatabaseError as e:
#             raise
#         except Exception as e:
#             raise
        with open('encrypted_config.ini', 'r') as encrypted_file:
            encrypted_config = encrypted_file.read()

        # Generate a secret key for decryption
        # secret_key = Fernet.generate_key()

        # # Create a Fernet cipher using the secret key
        # cipher = Fernet(secret_key)
        with open('secret.key', 'rb') as key_file:
            loaded_secret_key = key_file.read()

        # Decrypt the configuration string
        cipher = Fernet(loaded_secret_key)

        # Decrypt the configuration string
        decrypted_config = cipher.decrypt(encrypted_config.encode()).decode()

        # Convert the decrypted configuration string back to a configparser object
        decrypted_config_parser = configparser.ConfigParser()
        decrypted_config_parser.read_string(decrypted_config)

        try:
            # Get the db connection details from the decrypted configuration
            user = decrypted_config_parser.get('database', 'user')
            pwd = decrypted_config_parser.get('database', 'pwd')
            port = decrypted_config_parser.get('database', 'port')
            sn = decrypted_config_parser.get('database', 'service_name')
            dsn = decrypted_config_parser.get('database', 'dsn')
            self.connection = oracledb.connect(user=user, password=pwd, dsn=dsn)
        except oracledb.DatabaseError as e:
            raise
        except Exception as e:
            raise

    def CheckConn(self):
        cur=None
        try:
            cur = self.connection.cursor()
            cur.execute("""
            select 'Connection Succeded' from dual
            """)
            output = {}
            for text in cur:
                output['Connect Status'] = text[0]
            return output

        except Exception as e:
            raise
        finally:
            if cur is None:
                cur.close()

    def conversionOut(self,row):
        cur=self.connection.cursor()
        row_headers=[x[0] for x in cur.description]
        json_data=[]
        for result in row:
                json_data.append(dict(zip(row_headers,result)))
                val=json.dumps(json_data)
        return val

    # def user_input():
    #     item = input("Please enter item no: ")
    #     return item

    def getdetail(self,tracker:Tracker):
        item= tracker.get_slot('item')
        cur = self.connection.cursor()
        query = """select * from item_master where item=:item"""
        cur.execute(query, {'item': item})
        row_headers = [x[0] for x in cur.description]
        row = cur.fetchall()
        json_data = []
        val=""
        for result in row:
            json_data.append(dict(zip(row_headers, result)))
            val = json.dumps(json_data, default=str)
            # item_no = val[0]['ITEM']
        # if json_data:
            # val = json.dumps(json_data, default=str)
            val_dict = json.loads(val)
            item_no = val_dict[0]['ITEM']
            item_description = val_dict[0]['ITEM_DESC']
            department = val_dict[0]['DEPT']
            class_item = val_dict[0]['CLASS']
            subclass=val_dict[0]['SUBCLASS']
            return ((f"item no: {item_no}\nitem_description: {item_description}\ndepartment: {department}\nclass_item: {class_item}\nsubclass: {subclass}"))
            # return ((f"item no: {item_no}\nitem_description: {item_description}"))
            # return (item_no,item_description)
    def getdetail_supplier(self,tracker:Tracker):
        supp_item= tracker.get_slot('item')
        cur = self.connection.cursor()
        query = """select * from item_supplier where item=:supp_item"""
        cur.execute(query, {'supp_item': supp_item})
        row_headers = [x[0] for x in cur.description]
        row = cur.fetchall()
        json_data = []
        val=""
        for result in row:
            json_data.append(dict(zip(row_headers, result)))
            val = json.dumps(json_data, default=str)        
        
            val_dict = json.loads(val)
            item_supplier = val_dict[0]['SUPPLIER']    
            item = val_dict[0]['ITEM']   
                
            return (f"item supplier: {item_supplier}\nitem:{item}")
        
    # def getdetail_soh(self,tracker:Tracker):
    #     inventory_item= tracker.get_slot('inventory_item')
    #     cur = self.connection.cursor()
    #     query = """select * from item_loc_soh where item=:inventory_item"""
    #     cur.execute(query, {'inventory_item': inventory_item})
    #     row_headers = [x[0] for x in cur.description]
    #     row = cur.fetchall()
    #     json_data = []
    #     val=""
    #     for result in row:
    #         json_data.append(dict(zip(row_headers, result)))
    #         val = json.dumps(json_data, default=str)
    #         # item_no = val[0]['ITEM']
    #     # if json_data:
    #         # val = json.dumps(json_data, default=str)
    #         val_dict = json.loads(val)
    #         item_location = val_dict[0]['LOC']
    #         item_loc_type = val_dict[0]['LOC_TYPE']
    #         item_soh=val_dict[0]['STOCK_ON_HAND']  
    #         # out={"item_location":item_location,"item_loc_type":item_loc_type,"item_soh":item_soh}         
    #         return (f"item location: {item_location}\nitem_loc_type: {item_loc_type}\nitem_soh: {item_soh}")
            # return out
    def getdetail_total_soh_w(self,tracker:Tracker):
        inventory_item= tracker.get_slot('item')
        cur = self.connection.cursor()
        query = """select sum(stock_on_hand),count(loc_type) from item_loc_soh where item=:inventory_item and loc_type='W'"""
        # query1 = """select sum(stock_on_hand) from item_loc_soh where item=:item and loc_type='S'"""
        cur.execute(query, {'inventory_item': inventory_item})
        # cur.execute(query1, {'item': item})
        row_headers = [x[0] for x in cur.description]
        row = cur.fetchall()
        json_data = []
        val=""
        for result in row:
            json_data.append(dict(zip(row_headers, result)))
            val = json.dumps(json_data, default=str)  
            val_dict = json.loads(val)
            total_soh_warehouse = val_dict[0]['SUM(STOCK_ON_HAND)']
            total_no_of_warehouse_ranged=val_dict[0]['COUNT(LOC_TYPE)']
            if total_soh_warehouse is None or total_no_of_warehouse_ranged == 0:
                    raise ValueError("Sorry, I couldn't find any details for the item number you provided. Can you provide the correct item number?")
            
            return (f"total_soh_warehouse: {total_soh_warehouse}\ntotal_no_of_warehouse: {total_no_of_warehouse_ranged}")
    # out=getdetail_total_soh_w()
    # print(out)
    def getdetail_total_soh_s(self,tracker:Tracker):
            inventory_item= tracker.get_slot('item')
            cur = self.connection.cursor()
            # query = """select sum(stock_on_hand) from item_loc_soh where item=:item and loc_type='W'"""
            query = """select sum(stock_on_hand),count(loc_type) from item_loc_soh where item=:inventory_item and loc_type='S'"""
            cur.execute(query, {'inventory_item': inventory_item})
            # cur.execute(query1, {'item': item})
            row_headers = [x[0] for x in cur.description]
            row = cur.fetchall()
            json_data = []
            val=""
            for result in row:
                json_data.append(dict(zip(row_headers, result)))
                val = json.dumps(json_data, default=str)  
                val_dict = json.loads(val)
                total_soh_store = val_dict[0]['SUM(STOCK_ON_HAND)']
                total_no_of_store_ranged=val_dict[0]['COUNT(LOC_TYPE)']
                if total_soh_store is None or total_no_of_store_ranged == 0:
                    raise ValueError("Sorry, I couldn't find any details for the item number you provided. Can you provide the correct item number?")
                return (f"total_soh_store: {total_soh_store}\ntotal_no_of_store: {total_no_of_store_ranged}")
    
    # 
    # def order_details_prev_api(self,tracker:Tracker):
    #     prev_item=tracker.get_slot('item')
    #     # order_no=input('enter order no:')


    #     url = 'http://192.168.161.85:8000/order'
    #     # 'http://192.168.161.85:8000/order' -- to previous item order details
    #     headers = {'Content-Type': 'application/json'}
    #     data = {"item": prev_item}
    #     response = requests.post(url, headers=headers, json=data)
        
    #     json_data = json.loads(response.json())
    #     dict=json.dumps(json_data)
    #     # print(json_data)
    #     # print(type(dict))
    #     # if json_data is None:
    #     #      print("Sorry, the item number you provided has no order in approved status. Can you provide the correct item number?")
    #     # else:
    #     output = ''
    #     # dictionary=json_data[0]
    #     for dictionary in json_data:
    #             # dictionary=json_data[0]
    #         # if isinstance(dictionary, dict):
    #             order_no = dictionary['ORDER_NO']
    #             item = dictionary['ITEM']
    #             supplier = dictionary['SUPPLIER']
    #             location = dictionary['LOCATION']
    #             loc_type = dictionary['LOC_TYPE']
    #             department=dictionary['DEPT']
    #             item_desc=dictionary['ITEM_DESC']
                
    #             # quantity_ordered = dictionary['QTY_ORDERED']
    #             # quantity_received = dictionary['QTY_RECEIVED']
    #             output += f"order no:{order_no}\nitem:{item}\nsupplier:{supplier}\nlocation:{location}\nloc_type:{loc_type}\ndepartment:{department}\nitem_description:{item_desc}\n\n"
                
        
    #     return output

    def order_details_prev_api(self,tracker:Tracker):
        prev_item = tracker.get_slot('item')
        # prev_item=input('enter item no:')

        url = 'http://192.168.161.85:8000/order'
        headers = {'Content-Type': 'application/json'}
        data = {"item": prev_item}
        response = requests.post(url, headers=headers, json=data)

        # if response.status_code != 200:
        #     return "wrong_item_number"

        try:
            json_data = json.loads(response.json())
        except json.JSONDecodeError:
            return "Sorry, the item number you provided has no order in approved status. Can you provide the correct item number?"

        if not json_data or not isinstance(json_data, list):
            return "Sorry, the item number you provided has no order in approved status. Can you provide the correct item number?"

        output = ''
        for dictionary in json_data:
            order_no = dictionary.get('ORDER_NO')
            item = dictionary.get('ITEM')
            supplier = dictionary.get('SUPPLIER')
            location = dictionary.get('LOCATION')
            loc_type = dictionary.get('LOC_TYPE')
            department = dictionary.get('DEPT')
            item_desc = dictionary.get('ITEM_DESC')
            output += f"order no: {order_no}\nitem: {item}\nsupplier: {supplier}\nlocation: {location}\nloc_type: {loc_type}\ndepartment: {department}\nitem_description: {item_desc}\n\n"

        return output

    
    def order_details_not_prev_api(self, tracker: Tracker):
        order_no = tracker.get_slot('order_no')
        url = 'http://192.168.161.85:8000/ord_for_ordno'
        headers = {'Content-Type': 'application/json'}
        data = {"order_no": order_no}
        response = requests.post(url, headers=headers, json=data, timeout=120)
        json_data = json.loads(response.json())
        dict=json.dumps(json_data)
        # print(json_data)
        # print(type(dict))
        
        output = ''
        # dictionary=json_data[0]
        for dictionary in json_data:
                # dictionary=json_data[0]
            # if isinstance(dictionary, dict):
                order_no = dictionary['ORDER_NO']
                item = dictionary['ITEM']
                supplier = dictionary['SUPPLIER']
                location = dictionary['LOCATION']
                loc_type = dictionary['LOC_TYPE']
                department=dictionary['DEPT']
                item_desc=dictionary['ITEM_DESC']
                
                # quantity_ordered = dictionary['QTY_ORDERED']
                # quantity_received = dictionary['QTY_RECEIVED']
                output += f"order no:{order_no}\nitem:{item}\nsupplier:{supplier}\nlocation:{location}\nloc_type:{loc_type}\ndepartment:{department}\nitem_description:{item_desc}\n\n"
                # if not json_data:
                #     return "This order is not in approved status."  
        return output
    
    def order_details(self,tracker:Tracker):
        order_number = tracker.get_slot('order_no')
        # order_number=input("eneter order no")
        url = 'http://192.168.161.85:6000/order'
        headers = {'Content-Type': 'application/json'}
        data = {"order no": order_number}
        response = requests.post(url, headers=headers, json=data, timeout=120)
        # json_data = json.loads(response.json())
        # dict=json.dumps(json_data)
        # print(json_data)
        # print(type(dict))
        try:
            json_data = json.loads(response.json())
        except json.JSONDecodeError:
            return "Sorry, I can't find details for the provided order number. Can you provide the correct order number?"

        if not json_data or not isinstance(json_data, list):
            return "Sorry, I can't find details for the provided order number. Can you provide the correct order number?"
        
        output = ''
        
        for data in json_data:
            order_no = data['ORDER_NO']
            item = data['ITEM']
            supplier = data['SUPPLIER']
            location = data['LOCATION']
            quantity_ordered = data['QTY_ORDERED']
            quantity_received = data['QTY_RECEIVED']
            output += f"order no:{order_no}\nitem:{item}\nsupplier:{supplier}\nlocation:{location}\nquantity ordered:{quantity_ordered}\nquantity received:{quantity_received}\n\n"

        return output
    
    def call_chatgpt_api(self, user_input: Text) -> Text:
        # user_input = tracker.get_slot('user_input')
        api_key = "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"
        # api_key="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"
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
#     # out=call_chatgpt_api('define stock ledger')
#     # print(out)

# res=jsonConversion()
# out=res.order_details()
# print(out)