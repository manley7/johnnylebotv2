# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet

import json
import gspread
import numpy as np
from datetime import date

import logging
import requests
import json
from rasa_core_sdk import Action
from oauth2client.client import SignedJwtAssertionCredentials

logger = logging.getLogger(__name__)




# class ActionSolde(Action):

#     def name(self):
#         return "action_rep_solde"    
      
#     def run(self, dispatcher, tracker, domain):
#         balance = "test"
#         return [SlotSet('SOLDE'), balance]
class ActionSolde(Action):
  
    def name(self):
        return "action_rep_solde"
    def run(self, dispatcher, tracker, domain):
      
        json_key = json.load(open("creds.json")) # json credentials you downloaded earlier
        scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
        credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope) # get email and key from creds
        file = gspread.authorize(credentials)
        client = "Client1" #get the name of the client
        sheet = file.open("Comptes Clients").worksheet(client)
        balance = sheet.cell(3,2).value
        return [SlotSet("SOLDE"), balance]

#         FONCTION VIREMENT
class ActionTransfert(Action):

    def name(self):
        return "action_transfert"
    def run(self, dispatcher, tracker, domain):

        json_key = json.load(open("creds.json")) # json credentials you downloaded earlier
        scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
        credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope) # get email and key from creds
        file = gspread.authorize(credentials)
        client1 = "Client1" # get the name of the client
        client2 = tracker.get_slot('DESTINATAIRE') # get the name of the receiver
        montant = tracker.get_slot('PRIX')
        #motif = tracker.get_slot('MOTIF')
        dateD = str(date.today().day)+"/"+str(date.today().month)
    
        virement = False
    
        # check the receiver ID
        banque = file.open("Comptes Clients").worksheet("Banque")
        i = 6
        while banque.cell(i,7).value != "":
            if banque.cell(i,7).value == client2:
                virement = True
            i=i+1
        # open accounts
        if virement == True:
            sheet = file.open("Comptes Clients").worksheet("Transactions")
            sheet1 = file.open("Comptes Clients").worksheet(client1)
            sheet2 = file.open("Comptes Clients").worksheet(client2)
            autorisation = 0
            balance = int(sheet1.cell(3,2).value)
    
            if balance + montant < autorisation:
                virement = False
    
        # write the transaction  
        if virement == True:
            i = 6
            while sheet1.cell(i,1).value != "":
                i = i+1
            sheet1.update_cell(i,1, dateD)
            sheet1.update_cell(i,2, client2)
            #sheet1.update_cell(i,3, motif)
            sheet1.update_cell(i,4, -1*montant)
            j = 6
            while sheet2.cell(j,1).value != "":
                j = j+1
            sheet2.update_cell(j,1, dateD)
            sheet2.update_cell(j,2, client1)
            #sheet2.update_cell(j,3, motif)
            sheet2.update_cell(j,4, montant)
            k = 6
            while sheet.cell(k,1).value != "":
                k = k+1
            sheet.update_cell(k,1, dateD)
            sheet.update_cell(k,2, client1)
            sheet.update_cell(k,3, client2)
            #sheet.update_cell(k,4, motif)
            sheet.update_cell(k,5, montant)
        return [SlotSet('CONFIRMATION_VIREMENT'), virement]