# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

import os
import json
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet,UserUtteranceReverted
from trydb import jsonConversion
# from trydb import getdetail_total_soh_s,getdetail_total_soh_w
import requests
# import pandas as pd
# class ActionDefaultFallback(Action):
#     def name(self) -> Text:
#         return "action_default_fallback"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="I'm sorry, I didn't understand. Could you please rephrase your question?")

#         return []
class Itemdetails(Action):
    def name(self)-> Text:
        return "action_get_itemdetail"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
      
        item = tracker.latest_message.get('text')
        # order_no = tracker.latest_message.get('text')
        print(item)
        # print(order_no)
        object= jsonConversion()
        getdetail_item=object.getdetail(tracker)
        # print(getdetail_item)
        if not getdetail_item:
            dispatcher.utter_message(text="Sorry, I couldn't find any details for the item number you provided. Can you provide the correct item number?")
        # getdetail_supplier=object.getdetail_supplier(tracker)
        # getdetail_soh=object.getdetail_soh(tracker)
        # getdetail_total_soh_w=object.getdetail_total_soh_w(tracker)
        # getdetail_total_soh_s=object.getdetail_total_soh_s(tracker)
        else:
            dispatcher.utter_message(text=getdetail_item)
        # dispatcher.utter_message(json_message={"custom": json.dumps(getdetail_item)})
        # dispatcher.utter_message(text=getdetail_supplier)
        # dispatcher.utter_message(text=getdetail_total_soh_w)
        # dispatcher.utter_message(text=getdetail_total_soh_s)
        
        return [SlotSet('item', item)]
    
class Supplierdetails(Action):
    def name(self)-> Text:
        return "action_get_supplierdetail"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
      
        supp_item = tracker.latest_message.get('text')
        # order_no = tracker.latest_message.get('text')
        print(supp_item)
        # print(order_no)
        object= jsonConversion()
        # getdetail_item=object.getdetail(tracker)
        getdetail_supplier=object.getdetail_supplier(tracker)
        # print(getdetail_supplier)
        if not getdetail_supplier:
            dispatcher.utter_message(text="Sorry, I couldn't find any details for the item number you provided. Can you provide the correct item number?")
        else:
            dispatcher.utter_message(text=getdetail_supplier)
        return [SlotSet('item',supp_item)]
    


class Inventorydetails(Action):
    def name(self)-> Text:
        return "action_get_inventorydetail"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
      
        inventory_item = tracker.latest_message.get('text')
        # order_no = tracker.latest_message.get('text')
        print(inventory_item)
        # print(order_no)
        object= jsonConversion()
        # getdetail_item=object.getdetail(tracker)
        # getdetail_supplier=object.getdetail_supplier(tracker)
        # getdetail_soh=object.getdetail_soh(tracker)
        # getdetail_total_soh_w=object.getdetail_total_soh_w(tracker)
        try:
            getdetail_total_soh_w = object.getdetail_total_soh_w(tracker)
            getdetail_total_soh_s = object.getdetail_total_soh_s(tracker)
            dispatcher.utter_message(text=str(getdetail_total_soh_w))
            dispatcher.utter_message(text=str(getdetail_total_soh_s))
            error_message=""



        except ValueError as e:
            error_message = (
                str(e)
                if str(e)
                else "Invalid item number"
                )
        dispatcher.utter_message(text=error_message)
        return [SlotSet('item', inventory_item)]

             
        # return [SlotSet('item', inventory_item)]
        
        # return [SlotSet('item', inventory_item)]
        # if getdetail_total_soh_s is None and getdetail_total_soh_w is None:
        #     dispatcher.utter_message(text="Sorry, I couldn't find any details for the item number you provided. Can you provide the correct item number?")
        # else:
        #     if getdetail_total_soh_w is not None:
        #         dispatcher.utter_message(text=getdetail_total_soh_w)
        #     if getdetail_total_soh_s is not None:
        #         dispatcher.utter_message(text=getdetail_total_soh_s)
        # return [SlotSet('item', inventory_item)]
    

    
class Orderdetail_prev_item(Action):
    def name(self)-> Text:
        return "action_order_details_previous_item"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
      
        # item = tracker.latest_message.get('text')
        prev_item = tracker.latest_message.get('text')
        # print(item)
        # print("order for item:",prev_item)
        
        object= jsonConversion()
        # try:
        order_details=object.order_details_prev_api(tracker)
        print(order_details)
        if not order_details:
            dispatcher.utter_message(text="Sorry, the item number you provided has no order in approved status. Can you provide the correct item number?")
        else:
            dispatcher.utter_message(text=order_details)

        return [SlotSet('item', prev_item)]
    
# class Orderdetail_prev_item(Action):
#     def name(self)-> Text:
#         return "action_order_details_previous_item"
    
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
      
#         # item = tracker.latest_message.get('text')
#         prev_item = tracker.latest_message.get('text')
#         # print(item)
#         # print("order for item:",prev_item)
#         object= jsonConversion()
#         order_details=object.order_details_prev_api(tracker)
#         if not order_details:
#             dispatcher.utter_message(text="Sorry, the item number you provided has no order in approved status. Can you provide the correct item number?")
#         else:
         
#             dispatcher.utter_message(text=order_details)
       
#         return [SlotSet('item', prev_item)]
    
class Orderdetail_not_prev_item(Action):
    def name(self)-> Text:
        return "action_order_details_not_previous_item"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
      
        
        order_no = tracker.latest_message.get('text')
        # print(order_no)
        print("order for new order no:",order_no)
        object= jsonConversion()
        order_details=object.order_details_not_prev_api(tracker)
        dispatcher.utter_message(text=order_details)

        return [SlotSet('order_no', order_no)]

class Transferdetails(Action):
    def name(self) -> Text:
        return "get_transfer_action"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        transfer_no = tracker.get_slot('transfer_no')

        print("transfer no:",transfer_no)
       
        # Define the request payload
        payload = {
            "transfer no": transfer_no
        }
        
        # Send the POST request to the API and store the response
        try:
            response = requests.post("http://192.168.161.85:6000/transfer", json=payload, timeout=120)
            response.raise_for_status()
            response_data = json.loads(response.json())
            # print(type(response_data))
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text=f"An error occurred: {e}")
            return []

            # Check if the response is empty
        if not response_data:
            dispatcher.utter_message(text="The response is empty.")
            return []
            

        item=response_data[0]["ITEM"]
        from_loc_type=response_data[0]["FROM_LOC_TYPE"]
        from_loc=response_data[0]["FROM_LOC"]
        to_loc_type=response_data[0]["TO_LOC_TYPE"]
        to_loc=response_data[0]["TO_LOC"]
        transfer_quantity=response_data[0]["TSF_QTY"]

        dispatcher.utter_message(f"ITEM: {item}")
        dispatcher.utter_message(f"from_loc_type: {from_loc_type}")
        # dispatcher.utter_message(f": {from_loc_type}")
        dispatcher.utter_message(f"from_loc: {from_loc}")
        dispatcher.utter_message(f"to_loc_type: {to_loc_type}")
        dispatcher.utter_message(f"to_loc: {to_loc}")
        dispatcher.utter_message(f"transfer_quantity: {transfer_quantity}")
        # dispatcher.utter_message(f"SOH_UPDATE_DATETIME: {SOH_UPDATE_DATETIME}")

        return [SlotSet('transfer_no', transfer_no)]

class Shipmentdetails(Action):
    def name(self) -> Text:
        return "get_shipment_action"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        t_no = tracker.get_slot('t_no')

        print("transfer no. for shipment:",t_no)
       
        # Define the request payload
        payload = {
            "transfer no": t_no
        }
        
        # Send the POST request to the API and store the response
        try:
            response = requests.post("http://192.168.161.85:6000/shipment", json=payload, timeout=120)
            response.raise_for_status()
            response_data = json.loads(response.json())
            # print(type(response_data))
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text=f"An error occurred: {e}")
            return []

            # Check if the response is empty
        if not response_data:
            dispatcher.utter_message(text="The response is empty.")
            return []
            

        item=response_data[0]["ITEM"]
        shipment=response_data[0]["SHIPMENT"]
        order_no=response_data[0]["ORDER_NO"]
        ASN=response_data[0]["ASN"]
        quantity_received=response_data[0]["QTY_RECEIVED"]
        bol_no=response_data[0]["BOL_NO"]
        to_loc=response_data[0]["TO_LOC"]
        to_loc_type=response_data[0]["TO_LOC_TYPE"]
        from_loc=response_data[0]["FROM_LOC"]
        bill_to_loc=response_data[0]["BILL_TO_LOC"]
        bill_to_loc_type=response_data[0]["BILL_TO_LOC_TYPE"]
        distro_no=response_data[0]["DISTRO_NO"]

        dispatcher.utter_message(f"ITEM: {item}")
        dispatcher.utter_message(f"shipment: {shipment}")
        dispatcher.utter_message(f"order_no: {order_no}")
        dispatcher.utter_message(f"ASN: {ASN}")
        dispatcher.utter_message(f"quantity_received: {quantity_received}")
        dispatcher.utter_message(f"bol_no: {bol_no}")
        dispatcher.utter_message(f" bill_to_loc: { bill_to_loc}")
        dispatcher.utter_message(f"bill_to_loc_type: {bill_to_loc_type}")
        dispatcher.utter_message(f"distro_no: {distro_no}")
        dispatcher.utter_message(f"from_loc: {from_loc}")
        dispatcher.utter_message(f"to_loc_type: {to_loc_type}")
        dispatcher.utter_message(f"to_loc: {to_loc}")
        
        # dispatcher.utter_message(f"SOH_UPDATE_DATETIME: {SOH_UPDATE_DATETIME}")

        return [SlotSet('t_no', t_no)]
    
# class ActionSaveConversation(Action):

#     def name(self) -> Text:
#         return "action_save_conversation"
    
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         conversation=tracker.events
#         print(conversation)
#         if not os.path.isfile('chats.csv'):
#             with open('chats.csv','w') as file:
#                 file.write("intent,user_input,entity_name,entity_value,action,bot_reply\n")
#         chat_data=''
#         for i in conversation:
#             if i['event'] == 'user':
#                 chat_data+=i['parse_data']['intent']['name']+','+i['text']+','
#                 print('user: {}'.format(i['text']))
#                 if len(i['parse_data']['entities']) > 0:
#                     chat_data+=i['parse_data']['entities'][0]['entity']+','+i['parse_data']['entities'][0]['value']+','
#                     print('extra data:', i['parse_data']['entities'][0]['entity'], '=',
#                           i['parse_data']['entities'][0]['value'])
#                 else:
#                     chat_data+=",,"
#             elif i['event'] == 'bot':
#                 print('Bot: {}'.format(i['text']))
#                 try:
#                     chat_data+=i['metadata']['utter_action']+','+i['text']+'\n'
#                 except KeyError:
#                     pass
#         else:
#             with open('chats.csv','a') as file:
#                 file.write(chat_data)

#         dispatcher.utter_message(text="All Chats saved.")

#         return []
    

    
class Orderdetail(Action):
    def name(self)-> Text:
        return "action_order_detail_normal"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
      
        # item = tracker.latest_message.get('text')
        # order_no = tracker.latest_message.get('text')
        # # print(item)
        # print(order_no)
        # object= jsonConversion()
        # order_details=object.order_details_api(tracker)
        # dispatcher.utter_message(text=order_details)
        order_number = tracker.latest_message.get('text')
        print(order_number)
        object=jsonConversion()
        order_details=object.order_details(tracker)
        if not order_details:
            dispatcher.utter_message(text="Sorry, I can't find details for the provided order number. Can you provide the correct order number?")
        else:
            dispatcher.utter_message(text=order_details)        
        return [SlotSet('order_number', order_number)]
    
# class GPT(Action):
#     def name(self)-> Text:
#         return "action_call_GPT"
    
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
      
#         # item = tracker.latest_message.get('text')
#         # order_no = tracker.latest_message.get('text')
#         # # print(item)
#         # print(order_no)
#         # object= jsonConversion()
#         # order_details=object.order_details_api(tracker)
#         # dispatcher.utter_message(text=order_details)
#         user_message = tracker.latest_message.get('text')
#         print(user_message)
#         object=jsonConversion()
#         details_gpt=object.call_chatgpt_api(tracker)
#         dispatcher.utter_message(text=details_gpt)        
#         return [SlotSet('user_input', user_message)]

class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
    
    # Get user message from Rasa tracker
        # user_message = next(tracker.get_latest_entity_values("user_input"), None)
        # user_message = tracker.latest_message.get('text')
        # print(user_message)
        user_messages = [event['text'] for event in tracker.events if event['event'] == 'user']
        user_input = user_messages[-2] if len(user_messages) >= 2 else None  
        # print(user_input)
        # print(user_messages)

        if user_input:
            # user_input = user_message[-1]
            # print (user_input)
            object=jsonConversion()
            response = object.call_chatgpt_api(user_input)
            # Send the response to the user

            dispatcher.utter_message(response)

        return []
    #     api_key = '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'
    # # def get_chatgpt_response(self, message):
    #     url = 'https://api.openai.com/v1/chat/completions'
    #     headers = {
    #         'Authorization': f'Bearer {api_key}',
    #         'Content-Type': 'application/json'
    #     }
    #     data = {
    #         'model': "gpt-3.5-turbo",
    #         'messages': [   {'role': 'system', 'content': 'You are an AI assistant for the user. You help to solve user query'},
    #                         {'role': 'user', 'content': 'You: ' + user_message}
    #                         ],
    #         'max_tokens': 100
    #     }
    #     response = requests.post(url, headers=headers, json=data)
    #             # response = requests.post(api_url, headers=headers, json=data)

    #     if response.status_code == 200:
    #         chatgpt_response = response.json()
    #         message = chatgpt_response['choices'][0]['message']['content']
    #         dispatcher.utter_message(message)
    #     else:
    #         # Handle error
    #         return "Sorry, I couldn't generate a response at the moment. Please try again later."
        
    #             # Revert user message which led to fallback.
    #     return [SlotSet('user_input',user_message)]
# import requests
# from typing import Any, Dict, List, Text
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher

# class ActionCallGPT(Action):
#     def name(self) -> Text:
#         return "action_call_GPT"

#     def call_chatgpt_api(self, prompt: str) -> str:
#         api_key = "your_api_key"
#         url = 'https://api.openai.com/v1/chat/completions'

#         headers = {
#             'Authorization': f'Bearer {api_key}',
#             'Content-Type': 'application/json'
#         }
#         data = {
#             'model': "gpt-3.5-turbo",
#             'messages': [
#                 {'role': 'system', 'content': 'You are an AI assistant for the user. You help to solve user queries'},
#                 {'role': 'user', 'content': 'You: ' + prompt}
#             ],
#             'max_tokens': 100
#         }
#         response = requests.post(url, headers=headers, json=data)

#         if response.status_code == 200:
#             chatgpt_response = response.json()
#             message = chatgpt_response['choices'][0]['message']['content']
#             return message
#         else:
#             # Handle error
#             return "Sorry, I couldn't generate a response at the moment. Please try again later."

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         user_input = tracker.get_slot('user_input')
#         print(user_input)
#         if user_input is not None:
#             if user_input.lower() == "others":
#                 # User selected "Others", call the ChatGPT API with a prompt
#                 prompt = "Enter your prompt here"
#                 response = self.call_chatgpt_api(prompt)
#                 dispatcher.utter_message(text=response)
#             else:
#                 # User input is recognized, perform the corresponding action
#                 # ... perform the desired action here ...
#                 dispatcher.utter_message(text="Performing action based on recognized input.")
#         else:
#             dispatcher.utter_message(text="Sorry, I didn't receive any input.")
#         return []



    