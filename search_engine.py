import json
import pandas as pd
import requests

class SearchEngine:
    def __init__(self):
        self.API_KEY = "invisible_in_here" #Save it into enviromental variables if possible
        self.MY_ID = "some_id_of_yours"
        self.URL = "https://www.googleapis.com/customsearch/v1"

    # Set up google API + save retrieved .json on server
    def first_page_raw(self, query:str) -> dict:
        params = {
        "key" : self.API_KEY,
        "cx" : self.MY_ID,
        "q" : query
        }

        r = requests.get(self.URL, params=params)
        
        # Make json if query pass correctly
        if r.status_code == 200:
            try:
                with open(f"./{query}.json", "w", encoding="utf-8") as f:
                    f.write(r.text)
                return r.json()
            except Exception as e:
                print(f"Sorry, you had error {e}")
        else:
            print(r.status_code)
            return None
    
    # Extract relevant data from raw_json
    def extract_data(self,query ,raw_json:dict) -> dict:
        # Query is going to be retrieved from session
        with open(f"{query}.json", "r", encoding="utf-8") as f:
            data = f.read()
            data_dict = json.loads(data)

        self.result_count = data_dict["queries"]["request"][0]["count"]

        extracted_data = []
        # Clean data for 
        for x in range(0, self.result_count):
            self.extracted_title = data_dict["items"][x]["title"]
            self.extracted_url = data_dict["items"][x]["link"]
            self.extracted_web_name = data_dict["items"][x]["displayLink"]
            self.extracted_body = data_dict["items"][x]["snippet"]
        
            extracted_data.append({
            "title": self.extracted_title,
            "url": self.extracted_url,
            "web_name": self.extracted_web_name,
            "body": self.extracted_body
            })
        
        return extracted_data
    
    # Function which will save extracted data into new_json
    def new_json(self, query:str, extracted: list[dict]):
        try:
            with open(f"{query}_relevant.json", "w", encoding="utf-8") as f:
                json.dump(extracted, f,  ensure_ascii=False, indent=4)   
        except Exception as e:
            print(f"Error creating new json with relevant info: {e}")
        
    def new_csv(self, query:str, extracted: list[dict]):
        try:
            self.df = pd.DataFrame(extracted)
            self.df.to_csv(f"{query}_relevant_csv.csv",  encoding="utf-8-sig", index=False)
        except Exception as e:
            print(f"Sorry, there is problem with creating csv file: {e}")