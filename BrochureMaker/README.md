# 📖 Brochure Maker

An AI-powered brochure generation application built with Streamlit that automatically creates professional company or event brochures from a website URL.

## Features

* 🌐 Website content analysis and extraction
* 🤖 AI-generated brochure content
* 🎨 Multiple brochure tones:

  * Business
  * Professional
  * Humorous/Jovial
  * Snarky
* 🖼️ Automatic website image scraping
* 📤 Custom image upload support
* 🚫 Option to generate brochures without images
* 📄 HTML brochure generation
* ⬇️ Download-ready brochure output
* 🖨️ Print-friendly design (Save as PDF via browser)

---

## Application Workflow

### Step 1: Enter Brochure Details

Users provide:

* Company/Event Website URL
* Content Tone
* Company/Event Type
* Company/Event Name

### Step 2: Website Analysis

The application:

1. Scrapes website content
2. Extracts relevant assets and images
3. Sends extracted information to the first LLM processing layer

```python
response, img_links = llm1_controller(url, type_select)
```

### Step 3: Image Selection

Users can choose from:

#### Option A: Scraped Website Images

* Select an image extracted from the website

#### Option B: Upload Custom Image

* Upload PNG/JPG/JPEG files

#### Option C: No Image

* Generate a brochure without graphical elements

### Step 4: AI Content Generation

A second LLM refines and generates brochure-ready content using:

* Website data
* Selected tone
* Company/Event name
* Company/Event type

```python
text1 = llm2_controller(
    llm_response,
    tone,
    name,
    type_select
)
```

### Step 5: Brochure Generation

The application generates a complete HTML brochure:

```python
htmlfile = generate_brochure_html(
    brochure_text,
    selected_image,
    name
)
```

### Step 6: Preview & Download

Users can:

* Preview brochure inside Streamlit
* Download HTML brochure
* Print to PDF using browser (Ctrl + P)

---

## Project Structure

```text
project/
│
├── app.py
├── llmController.py
├── makeBrouchure.py
├── requirements.txt
└── README.md
```

### app.py

Main Streamlit application containing:

* UI components
* State management
* User workflow
* Brochure preview/download

### llmController.py

Contains:

#### llm1_controller()

Responsible for:

* Website scraping
* Content extraction
* Image collection

#### llm2_controller()

Responsible for:

* Brochure copy generation
* Tone customization
* Content refinement

### makeBrouchure.py

Contains:

#### generate_brochure_html()

Responsible for:

* HTML template generation
* Image integration
* Styling and formatting

---

## Session State Management

The application uses Streamlit Session State for maintaining user progress.

| Variable          | Purpose                |
| ----------------- | ---------------------- |
| img_links         | Scraped image URLs     |
| state_step        | Current workflow stage |
| selected_img      | Selected image         |
| selected_img_flag | Image selection status |
| llm_response      | First LLM response     |
| llm2_text         | Final brochure content |
| llm2_processed    | Processing status      |

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd brochure-maker
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

#### Windows

```bash
venv\Scripts\activate
```

#### Linux/Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Application

```bash
streamlit run app.py
```

Application will be available at:

```text
http://localhost:8501
```

---

## Usage Example

1. Enter:

```text
Website: https://company.com
Name: Company XYZ
Type: Company
Tone: Professional
```

2. Submit form

3. Select image source:

   * Website image
   * Upload image
   * No image

4. Wait for AI processing

5. Preview brochure

6. Download HTML file

7. Save as PDF using browser print functionality

---

## Technologies Used

* Python
* Streamlit
* Large Language Models (LLMs)
* HTML/CSS
* Website Scraping

---

## Future Enhancements

* Direct PDF generation
* Multiple brochure templates
* Theme customization
* Logo extraction
* Multi-page brochure support
* Brand color detection
* Social media integration
* Export to DOCX and PPT

---

## License

This project is intended for educational and business brochure generation purposes.
