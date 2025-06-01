from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests

def detect_language(message: str) -> str:
    """Detects the language of the input message based on Swahili keywords."""
    swahili_keywords = [
        "mambo", "habari", "jambo", "salaam", "vipi", "asubuhi", "mchana", "jioni",
        "shikamoo", "niaje", "salama", "heko", "safi", "kipekee", "sasa", "poa",
        "karibu", "mchakato", "mauzo", "mteja", "usajili", "nida", "simu", "malipo",
        "mkopo", "lipa", "thibitisha", "hakikisha", "bonyeza", "hatua", "kianzio",
        "data", "hitilafu", "sawazisha", "wateja", "portal", "waranti", "matengenezo",
        "potea", "ripoti", "huduma", "funga", "lock", "bei", "kuuzia"
    ]
    english_keywords = [
        "hi", "hello", "hey", "morning", "afternoon", "evening", "what's up", "sup",
        "yo", "greetings", "howdy", "hiya", "good", "night", "cheers", "aloha",
        "welcome", "sales", "process", "payment", "methods", "maintenance", "lost",
        "phone", "bot", "identity", "lock", "pricing", "sync", "users", "portal",
        "error", "success", "failed"
    ]
    
    message_lower = message.lower()
    swahili_score = sum(1 for keyword in swahili_keywords if keyword in message_lower)
    english_score = sum(1 for keyword in english_keywords if keyword in message_lower)
    
    return "swahili" if swahili_score > english_score else "english"

class ActionSetLanguage(Action):
    def name(self) -> Text:
        return "action_set_language"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        language = detect_language(tracker.latest_message.get("text", ""))
        return [SlotSet("language", language)]

class ActionSyncPortalUsers(Action):
    def name(self) -> Text:
        return "action_sync_portal_users"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        language = tracker.get_slot("language") or detect_language(tracker.latest_message.get("text", ""))
        try:
            # Mock API call (replace with real endpoint)
            response = requests.post("http://localhost:5005/sync_users", timeout=5)
            
            if response.status_code == 200:
                dispatcher.utter_message(response=f"utter_sync_portal_users_success/{language}")
            else:
                dispatcher.utter_message(response=f"utter_sync_portal_users_failure/{language}")
        except requests.RequestException as e:
            dispatcher.utter_message(response=f"utter_sync_portal_users_error/{language}", error=str(e))
        return []

class ActionSetSlotGreetingKeyword(Action):
    def name(self) -> str:
        return "action_set_slot_greeting_keyword"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        user_message = tracker.latest_message.get("text", "").lower()
        greeting_keywords = [
            "mambo", "habari", "jambo", "salaam", "vipi", "za asubuhi", "za mchana", "za jioni",
            "habari za asubuhi", "habari za mchana", "habari za jioni", "mambo vipi", "sasa", "poa",
            "shikamoo", "niaje", "salama", "heko", "safi", "kipekee", "vipi sasa", "habari yako",
            "jambo vipi", "za usiku", "karibu", "hi", "hello", "hey", "good morning", "good afternoon",
            "good evening", "morning", "afternoon", "evening", "what's up", "sup", "yo", "greetings",
            "howdy", "hiya", "good day", "hello there", "hey there", "hi there", "good night", "night",
            "cheers", "aloha", "welcome", "how's it going"
        ]
        
        for keyword in greeting_keywords:
            if keyword in user_message:
                return [SlotSet("greeting_keyword", keyword)]
        
        return [SlotSet("greeting_keyword", "hello")]

class ActionRespondByLanguage(Action):
    def name(self) -> Text:
        return "action_respond_by_language"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message.get("intent", {}).get("name", "")
        language = tracker.get_slot("language") or detect_language(tracker.latest_message.get("text", ""))
        
        intent_to_utterance = {
            "greet": "utter_greet",
            "ask_bot_identity": "utter_ask_bot_identity",
            "ask_sales_process": "utter_ask_sales_process",
            "ask_payment_methods": "utter_ask_payment_methods",
            "ask_maintenance": "utter_ask_maintenance",
            "ask_lost_phone": "utter_ask_lost_phone",
            "lock_phone": "utter_lock_phone",
            "phone_pricing": "utter_phone_pricing",
            "nlu_fallback": "utter_fallback"
        }
        
        utterance = intent_to_utterance.get(intent, "utter_fallback")
        dispatcher.utter_message(response=f"{utterance}/{language}")
        
        return []