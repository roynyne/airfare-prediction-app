import json 
from starlette.responses import JSONResponse

class BriefResults:
    def __init__(self):
        self.text ="""
        A data product that will help users in the USA to better estimate their local travel airfare. 
        Users will be able to provide details of their trip and the app will predict the expected flight fare.

        API endpoint for airfare prediction: "/airfare/predict"

        Github repo link - https://github.com/sidhantbajaj/airfare_web_service"""

    def response(self):
        return self.text
