from flask import Flask, render_template

app = Flask(__name__)

projects = [
    {
        "title": "Hotel UI/UX Project",
        "description": "This is a UI/UX project for a hotel booking system, created in Canva. The following images showcase different screens and design elements.",
        "images": ["image.png", "image2.png", "image3.png"],
        "technologies": ["Canva", "UI/UX Design"],
        "url": "https://www.canva.com/design/DAGK6yfEoWA/mNDmEE8oIVN4RM0U5U5BTw/edit?utm_content=DAGK6yfEoWA&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton"  # External link
    },
    {
        "title": "Boston House Prices",
        "description": "This project involves the analysis and modeling of Boston house prices using multivariable regression techniques. It includes data exploration, model training, and evaluation.",
        "images": ["boston_house_prices.jpg"],  
        "technologies": ["Python", "Pandas", "Scikit-learn", "Matplotlib", "Seaborn","Numpy"],
        "url": "pdf/Multivariable_Regression_and_Valuation_Model_(start).pdf" 
    }
]

@app.route("/")
def home():
    return render_template('home.html', projects=projects)

@app.route("/portfolio")
def portfolio():
    return render_template('index.html', projects=projects)

if __name__ == "__main__":
    app.run(debug=True)
