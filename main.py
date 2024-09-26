from flask import Flask, render_template, request, session, send_file
from search_engine import SearchEngine

# WSGI app
app = Flask(__name__)

# For cookie reading ---> sessions are then allowed
app.secret_key = "thiskeyshouldntbeherebutfornowitisok.1084"

# Homepage setup 
@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == "POST":
        # Retrieve info from user's input
        users_query = request.form.get('query')
        
        # Thanks to seesion we can use user's input later in this app
        session['users_query'] = users_query

        search = SearchEngine()
        
        # If API connection is not sucessful for some reason || Problem to save file
        try:
            search.first_page_raw(users_query)
        except Exception as e:
            print(f"Sorry, we had some issue: {e}")    

    return render_template("index.html") # Created HTML code for pretty looks

# Button "Download Raw data in JSON"
@app.route('/download_raw_json', methods=['POST'])
def download_raw_json():
    # Cookie give me last user's input again
    users_query = session.get("users_query", None) 

    # Still same logic
    path = f"{users_query}.json"

    # Returning downloadable .json file instead of redering webpage
    return send_file(path, as_attachment=True, download_name="raw_json.json", mimetype="application/json")

# Button "Download Clean Data in JSON"
@app.route('/download_clean_json', methods=['POST'])
def download_clean_json():
    # Read user's data from cookie...
    query = session.get("users_query", None)

    # Naming logic
    path = f"{query}.json"
    path_for_download = f"{query}_relevant.json"

    # It would be better to not repeat code but for this short porgram not the horror story
    search = SearchEngine()
    try:
        extracted_data = search.extract_data(query, path)
        search.new_json(query, extracted_data)
    except Exception as E:
        print("Sorry, there is some problem, file is probably not saved correctly")

    # Return cleaned .json file
    return send_file(path_for_download, as_attachment=True, download_name="relevant_data.json", mimetype="application/json")

# Button "Download Clean Data in CSV"
@app.route('/download_clean_csv', methods=['POST'])
def download_clean_csv():
    query = session.get("users_query", None)
    path = f"{query}.json"
    path_for_download = f"{query}_relevant_csv.csv"

    search = SearchEngine()
    try:
        extracted_data = search.extract_data(query, path)
        search.new_csv(query, extracted_data)  # Use new_csv to generate the CSV file
    except Exception as e:
        print("Sorry, there is some problem, file is probably not saved correctly")
        
    # Return cleaned .csv file    
    return send_file(path_for_download, as_attachment=True, download_name="relevant_data_in_csv.csv", mimetype="text/csv")

# Must exists for flask to work - only direct execution - not from elsewhere
if __name__ == '__main__':
    app.run(debug=True)