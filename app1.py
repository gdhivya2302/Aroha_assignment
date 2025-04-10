import os
import groq
from flask import Flask, request

app = Flask(__name__)

# Retrieve API key from environment variables (fallback to hardcoded key if not set)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")

if not GROQ_API_KEY:
    raise ValueError("Error: API key not found. Set GROQ_API_KEY environment variable.")

# Initialize Groq client
client = groq.Groq(api_key=GROQ_API_KEY)

def generate_recipe(ingredients):
    prompt = f"I have {', '.join(ingredients)}. Create a unique recipe with a title, ingredients list, steps, cooking time, and serving size."

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",  # Check Groq documentation for available models
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error: {e}"

@app.route("/", methods=["GET", "POST"])
def index():
    recipe = None
    if request.method == "POST":
        ingredients = request.form.get("ingredients").split(",")
        recipe = generate_recipe(ingredients)
    
    if recipe:
        return f"""
        <div class="recipe-container">
            <h1>AI-Generated Recipe</h1>
            <pre>{recipe}</pre>
        </div>
        """
    
    return '''
    <html>
    <head>
        <title>AI Recipe Generator</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background: linear-gradient(to right, #a8e6cf, #dcedc1); /* Light green gradient */
                color: #333;
                margin: 0;
                padding: 0;
            }
            h1 {
                font-size: 36px;
                font-weight: bold;
                color: #333;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            }
            .container {
                width: 90%;
                margin: 0 auto;
                text-align: center;
                padding: 20px;
            }
            form {
                background-color: rgba(255, 255, 255, 0.9);
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.3);
                margin-top: 50px;
                display: inline-block;
                max-width: 600px;
                width: 100%;
            }
            textarea {
                width: 100%;
                height: 120px;
                padding: 12px;
                border: 1px solid #ddd;
                border-radius: 8px;
                font-size: 16px;
                box-sizing: border-box;
            }
            button {
                background-color: #a8e6cf; /* Light green button color */
                color: white;
                border: none;
                padding: 12px 25px;
                font-size: 18px;
                cursor: pointer;
                border-radius: 6px;
                margin-top: 15px;
                transition: background-color 0.3s;
            }
            button:hover {
                background-color: #81c784; /* Darker green on hover */
            }
            .recipe-container {
                background-color: rgba(255, 255, 255, 0.9);
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2);
                margin-top: 50px;
                max-width: 800px;
                margin-left: auto;
                margin-right: auto;
            }
            pre {
                font-size: 18px;
                white-space: pre-wrap;
                word-wrap: break-word;
                color: #333;
                padding: 15px;
                background-color: #f0f0f0;
                border-radius: 8px;
                box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.1);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>AI Recipe Generator</h1>
            <form method="POST">
                <label for="ingredients">Enter available ingredients:</label><br><br>
                <textarea name="ingredients" required></textarea><br><br>
                <button type="submit">Generate Recipe</button>
            </form>
        </div>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(debug=True)
