import requests
from flask import Flask, render_template, request

app = Flask(__name__)

def fetch_data(endpoint):
    response = requests.get(f"https://www.dnd5eapi.co/api/{endpoint}")
    return response.json()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/classes")
def classes():
    data = fetch_data("classes")
    classes = data.get('results', [])
    return render_template("classes.html", classes=classes)

@app.route("/spells")
def spells():
    level_filter = request.args.get('level')
    school_filter = request.args.get('school')

    # Fetch spells data
    data = fetch_data("spells")
    spells = data.get('results', [])

    # Debugging: Print a sample spell to check the school structure
    if spells:
        print("Sample spell:", spells[0])

    if level_filter:
        levels = [int(level) for level in level_filter.split(',')]
        spells = [spell for spell in spells if spell['level'] in levels]

    if school_filter:
        schools = [school.strip().lower() for school in school_filter.split(',')]
        # Filtering spells based on the school index
        spells = [spell for spell in spells if spell.get('school', {}).get('index', '').lower() in schools]

    print("Filtered spells count:", len(spells))  # Debugging line

    return render_template("spells.html", spells=spells)

@app.route("/spells/<spell_id>")
def spell_detail(spell_id):
    spell_info = requests.get(f"https://www.dnd5eapi.co/api/spells/{spell_id}").json()
    return render_template("spell_detail.html", spell=spell_info)

if __name__ == "__main__":
    app.run(debug=True)
