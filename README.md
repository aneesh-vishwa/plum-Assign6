# AI-Powered Health Risk Profiler

This backend service was developed for the SDE Intern Assignment. The goal was to build a system that can take a lifestyle survey—either as text or a scanned image—and generate a structured health risk profile with actionable recommendations.

I chose this problem because it seemed like a practical application of data processing and API development. The focus was on creating a reliable, easy-to-use endpoint that could handle different types of input gracefully.

## Core Features

* **Handles Both Text and Image Input:** A single endpoint can process direct text submissions or uploaded images of survey forms.
* **OCR for Images:** Uses Google's Tesseract engine to extract text from images, making it possible to digitize paper forms. 
* **Rule-Based Logic:** Implements a straightforward engine to identify risk factors, calculate a risk level, and provide corresponding advice.
* **Robust Error Handling:** Includes a guardrail to reject incomplete submissions, ensuring the data quality is sufficient for analysis.
* **Structured JSON Output:** The API's responses are strictly typed and follow the predefined schemas from the assignment.

## How It Works (Architecture)

I designed the application with a modular pipeline in mind, using FastAPI. This keeps the code clean and easy to follow.

1.  **API Endpoint (`/profile`):** The entry point of the application. It's built to accept `multipart/form-data`, allowing it to handle both text (`survey_text`) and file (`survey_image`) fields.
2.  **OCR Service:** If an image is provided, this service takes over.It uses `pytesseract` to convert the image into a raw string of text.
3.  **Parsing & Validation Service:** This is a key step. It takes the raw text and parses it line-by-line to extract the key-value pairs.I also built the main 
**guardrail** here: if more than 50% of the required fields are missing, the service rejects the request with an error.
4.  **Risk Engine:** This is where the core logic lives. It takes the clean, parsed data and:
    * Identifies risk factors (like "smoking" or "low exercise").
    * Calculates a score to determine if the risk is "high," "medium," or "low."
    * Maps the identified factors to a list of helpful, non-diagnostic recommendations.
5.  **JSON Response:** The final, structured data is packaged into a clean JSON object and sent back to the user.

## How I Addressed the Evaluation Criteria

I focused on meeting each of the assignment's evaluation criteria:

* **Correctness of API responses and adherence to JSON schemas.**
    * I used Pydantic models (`src/utils/schemas.py`) to strictly define the structure of the API's output. This guarantees that every successful response and every error message conforms exactly to the required JSON schema.

* **Handling of both text and image inputs with OCR.**
    * The `/profile` endpoint was designed from the ground up to handle both input types. The logic checks if an image is present and routes it through the `ocr_service` before it hits the same parsing logic that the text input uses.

* **Implementation of guardrails and error handling.**
    * The primary guardrail is implemented in `src/services/parser_service.py`. [cite_start]It checks for missing fields and returns a specific `400 Bad Request` error if the input data is insufficient, as specified in the assignment.

* **Code organization, clarity, and reusability.**
    * The project is structured into separate directories (`api`, `services`, `utils`) to separate concerns. Each service has a single responsibility (e.g., OCR, parsing), which makes the code easy to read and maintain.

* **Effective use of AI for chaining and validation.**
    * The project demonstrates a clear "chain" where the output of one step becomes the input for the next (OCR -> Parser -> Risk Engine). The validation is handled in the parsing step, ensuring that the data passed down the chain is clean and complete enough for processing.

## Getting Started

Here’s how to get the project running on your local machine.

#### 1. Prerequisites
* Python 3.8+
* Tesseract OCR Engine (must be installed and available in your system's PATH).

#### 2. Setup
```bash
# Clone this repository to your machine
git clone <your-github-repo-url>
cd health-risk-profiler

# Set up and activate a Python virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install all the necessary packages
pip install -r requirements.txt
```

#### 3. Run the Server
```bash
# Start the FastAPI server
uvicorn main:app --reload
```
The server will be live at `http://127.0.0.1:8000`. When you open this in a browser, you'll be redirected to the interactive `/docs` page.

## How to Test the API

Here are the `curl` commands to test the endpoints.

#### Text Input Example
.  Run this command in your terminal:
    ```bash
    curl -X POST -F "survey_text=<survey.txt" [http://127.0.0.1:8000/profile](http://127.0.0.1:8000/profile)
    ```

#### Image Input Example
1.  Save a survey image (like one of the test images provided) as `test_survey.png`.
2.  Run this command:
    ```bash
    curl -X POST -F "survey_image=@test_survey.png" [http://127.0.0.1:8000/profile](http://127.0.0.1:8000/profile)
    ```

---

## Final Thoughts

I really enjoyed working on this project and figuring out the challenges along the way, especially getting the different input methods to work smoothly. I'm always looking to learn more and improve.

If you have any feedback or suggestions, please feel free to reach out.

* **Email:** [aneeshvishwa.dorishetty69@gmail.com]
* **LinkedIn:** [https://www.linkedin.com/in/aneesh-vishwa-dorishetty-47a335281/]