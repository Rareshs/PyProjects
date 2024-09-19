import requests
from flask import Flask, render_template, request

app = Flask(__name__)

def fetch_data(endpoint, params=None):
    url = f"https://www.dnd5eapi.co/api/{endpoint}"
    print("Request URL:", url, "Params:", params)  # Debugging line
    response = requests.get(url, params=params)
    return response.json()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/classes")
def classes():
    data = fetch_data("classes")
    classes = data.get('results', [])
    return render_template("classes.html", classes=classes)

@app.route("/classes/<class_id>")
def class_detail(class_id):
    class_info = fetch_data(f"classes/{class_id}")
    return render_template("class_details.html", class_info=class_info)

@app.route("/spells")
def spells():
    level_filter = request.args.get('level')
    school_filter = request.args.get('school')

    # Prepare query parameters
    params = {}
    if level_filter:
        params['level'] = level_filter
    if school_filter:
        params['school'] = school_filter

    data = fetch_data("spells", params=params)
    spells = data.get('results', [])

    # print("Filtered spells count:", len(spells))  # Debugging line
    # print("Response Data:", data)  # Debugging line

    return render_template("spells.html", spells=spells)

@app.route("/spells/<spell_id>")
def spell_detail(spell_id):
    spell_info = fetch_data(f"spells/{spell_id}")
    return render_template("spell_detail.html", spell=spell_info)

if __name__ == "__main__":
    app.run(debug=True)
