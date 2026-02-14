from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

# ================= HOME PAGE =================
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>CurricuForge - AI Curriculum Designer</title>
            <style>
                body { font-family: Arial; background-color: #f4f4f4; text-align: center; }
                .container { margin-top: 100px; }
                input { padding: 10px; width: 300px; }
                button { padding: 10px 20px; background-color: #007bff; color: white; border: none; cursor:pointer; }
                button:hover { background-color: #0056b3; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>CurricuForge</h1>
                <h3>Generative AI–Powered Curriculum Design</h3>
                <form action="/generate" method="post">
                    <input type="text" name="course" placeholder="Enter Course Name" required>
                    <br><br>
                    <button type="submit">Generate Curriculum</button>
                </form>
            </div>
        </body>
    </html>
    """

# ================= GENERATE CURRICULUM =================
@app.post("/generate", response_class=HTMLResponse)
def generate(course: str = Form(...)):

    prompt = f"""
    Design a complete industry-aligned undergraduate curriculum for the course: {course}

    Include:
    1. Course Overview
    2. Course Objectives
    3. 5 Units with topics
    4. Learning Outcomes
    5. Skills Developed
    6. Tools & Technologies
    7. Real-world Applications
    8. Assessment Strategy
    9. Capstone Project
    10. Industry Alignment
    """

    API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

    try:
        response = requests.post(API_URL, json={"inputs": prompt}, timeout=30)

        if response.status_code == 200:
            data = response.json()

            if isinstance(data, list):
                result = data[0].get("generated_text", "No output generated.")
            else:
                result = "Unexpected API response format."
        else:
            result = f"API Error: {response.status_code}"

    except Exception as e:
        result = f"Error connecting to AI service: {str(e)}"

    return f"""
    <html>
        <head>
            <title>Generated Curriculum</title>
            <style>
                body {{ font-family: Arial; padding: 40px; background-color: #ffffff; }}
                pre {{ white-space: pre-wrap; }}
                a {{ text-decoration: none; color: blue; }}
            </style>
        </head>
        <body>
            <h2>Generated Curriculum for: {course}</h2>
            <pre>{result}</pre>
            <br>
            <a href="/">⬅ Back</a>
        </body>
    </html>
    """
