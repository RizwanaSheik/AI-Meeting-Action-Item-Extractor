\# AI Meeting Action-Item Extractor



An AI-powered application that converts meeting transcripts into structured action items using Google's Gemini API. It identifies tasks, responsible people, deadlines, status, confidence scores, and supporting evidence, then validates the results and flags items that require human review.



\## Features



\- \*\*Multiple file formats:\*\* Upload TXT, PDF, and DOCX meeting transcripts.

\- \*\*AI-powered extraction:\*\* Extract action items using the Gemini API.

\- \*\*Structured output:\*\* Organize tasks, owners, deadlines, status, confidence scores, and transcript evidence.

\- \*\*Validation:\*\* Detect missing owners, missing deadlines, invalid dates, invalid statuses, low-confidence items, and possible duplicate tasks.

\- \*\*Human-review queue:\*\* Identify extracted items that need additional review.

\- \*\*Evaluation metrics:\*\* Calculate precision, recall, and F1 score against reference annotations.

\- \*\*Export results:\*\* Download action items in CSV and JSON formats.

\- \*\*Streamlit dashboard:\*\* View transcripts, extracted items, validation results, and evaluation metrics.

\- \*\*Automated tests:\*\* Test preprocessing, extraction, validation, evaluation, and the complete pipeline.



\## Technology Stack



\- Python

\- Streamlit

\- Google Gemini API (`google-genai`)

\- Pandas

\- Scikit-learn

\- PyMuPDF-free PDF extraction with `pypdf`

\- `python-docx`

\- `python-dotenv`



\## Project Structure



```text

AI-Meeting-Action-Item-Extractor/

â”œâ”€â”€ app.py

â”œâ”€â”€ requirements.txt

â”œâ”€â”€ .env

â”œâ”€â”€ .gitignore

â”œâ”€â”€ src/

â”‚   â”œâ”€â”€ \_\_init\_\_.py

â”‚   â”œâ”€â”€ preprocessing.py

â”‚   â”œâ”€â”€ extraction.py

â”‚   â”œâ”€â”€ validation.py

â”‚   â”œâ”€â”€ pipeline.py

â”‚   â””â”€â”€ evaluation.py

â”œâ”€â”€ data/

â”‚   â”œâ”€â”€ sample\_transcripts/

â”‚   â”‚   â””â”€â”€ meeting\_001.txt

â”‚   â””â”€â”€ annotations/

â”‚       â”œâ”€â”€ meeting\_001.json

â”‚       â””â”€â”€ example\_meeting\_transcript.json

â”œâ”€â”€ outputs/

â”œâ”€â”€ tests/

â”‚   â”œâ”€â”€ \_\_init\_\_.py

â”‚   â”œâ”€â”€ test\_preprocessing.py

â”‚   â”œâ”€â”€ test\_extraction.py

â”‚   â”œâ”€â”€ test\_validation.py

â”‚   â”œâ”€â”€ test\_pipeline.py

â”‚   â””â”€â”€ test\_evaluation.py

â””â”€â”€ screenshots/

```



\## Installation and Setup



\### 1. Clone the repository



```bash

git clone YOUR\_GITHUB\_REPOSITORY\_URL

cd AI-Meeting-Action-Item-Extractor

```



Replace `YOUR\_GITHUB\_REPOSITORY\_URL` with your actual GitHub repository URL.



\### 2. Create a virtual environment



Windows PowerShell:



```powershell

python -m venv .venv

```



Activate it:



```powershell

.venv\\Scripts\\Activate.ps1

```



\### 3. Install dependencies



```powershell

python -m pip install -r requirements.txt

```



\### 4. Configure the Gemini API key



Create a `.env` file in the project root:



```text

GEMINI\_API\_KEY=YOUR\_GEMINI\_API\_KEY

```



Replace the placeholder with your own Gemini API key. Keep the key private and never commit the `.env` file to GitHub.



\### 5. Start the application



```powershell

python -m streamlit run app.py

```



Open the local URL displayed in the terminal.



\## How to Use



1\. Upload a meeting transcript in TXT, PDF, or DOCX format.

2\. Review the cleaned transcript.

3\. Click \*\*Extract Action Items\*\*.

4\. Review the extracted tasks and validation results.

5\. Inspect items in the human-review queue when needed.

6\. Download the results as CSV or JSON.

7\. View evaluation metrics when a matching reference annotation file exists.



\## Evaluation



The evaluation module compares extracted action items against manually prepared reference annotations. It calculates:



\- \*\*Precision:\*\* The proportion of predicted action items that match reference items.

\- \*\*Recall:\*\* The proportion of reference items successfully matched.

\- \*\*F1 Score:\*\* The harmonic mean of precision and recall.



Evaluation is available only when a corresponding annotation file exists in `data/annotations/`. Scores depend on annotation quality and the matching threshold. Results on a small sample dataset do not guarantee the same performance on unseen transcripts.



For an uploaded file named `example\_meeting\_transcript.pdf`, the application looks for:



```text

data/annotations/example\_meeting\_transcript.json

```



PDF and DOCX files can share the same annotation file when their transcript content is identical.



\## Run the Tests



Run the test modules from the project root:



```powershell

python -m tests.test\_preprocessing

python -m tests.test\_extraction

python -m tests.test\_validation

python -m tests.test\_evaluation

python -m tests.test\_pipeline

```



The extraction and pipeline tests call the Gemini API and may require a valid API key and available API quota. Run the other tests according to their implementation and dependencies.



\## Security



\- Store API credentials in `.env`.

\- Do not upload API keys, passwords, or confidential meeting transcripts to public repositories.

\- Keep `.env` and `.venv/` out of Git version control.

\- Review generated action items before relying on them for important decisions.



\## Future Improvements



\- Add OCR support for scanned PDFs.

\- Expand the annotated dataset and evaluate performance on more transcripts.

\- Improve confidence calibration and low-confidence detection.

\- Add human-review editing and approval workflows.

\- Add deployment and monitoring improvements.



\## Author



\*\*Sheik Rizwana Begum\*\*



AI Meeting Action-Item Extractor â€” a project exploring AI-powered information extraction, transcript processing, structured data validation, and evaluation.
