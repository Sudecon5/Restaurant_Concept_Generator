# Restaurant Concept Generator 🍽️

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-7E5BEF?style=for-the-badge)
![Mistral](https://img.shields.io/badge/Mistral-7E5BEF?style=for-the-badge)

A creative AI-powered tool that generates unique restaurant concepts, names, and menu ideas based on user preferences. Powered by Ollama's Mistral LLM and built with Streamlit.

## 🌟 Live Demo

Check out the live application:  
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://restaurantconceptgenerator-xha3xahxm2bbsxi8cbdoqt.streamlit.app)

## ✨ Features

- Generate creative restaurant name suggestions
- Get complete menu ideas tailored to your cuisine preferences
- Customizable based on location, theme, or dietary restrictions
- AI-powered concept generation using Mistral LLM
- User-friendly Streamlit interface

## 🛠️ Technologies Used

- **Frontend**: Streamlit
- **AI Backend**: Ollama with Mistral LLM
- **Programming Language**: Python

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Ollama installed and running locally
- Mistral model downloaded in Ollama

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Sudecon5/Restaurant_Concept_Generator.git
   cd Restaurant_Concept_Generator

2. Activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use venv\Scripts\activate
   ```

3.Install Dependencies:
   ```bash
    pip install -r requirements.txt
  ```

4. Run the Streamlit App
   ```bash
   streamlit run app.py
   ```
## 🤖 How It Works

- **User Input**:
  - Users enter their preferences including:
    - Cuisine type (Italian, Japanese, Fusion, etc.)
    - Location or theme (Beachside, Urban, Rustic, etc.)
    - Dietary preferences (Vegan, Gluten-free, etc.)
    - Any other special requirements

- **AI Processing**:
  - The application sends these parameters to Ollama's Mistral LLM
  - The AI analyzes the inputs using its trained knowledge
  - Generates creative concepts based on culinary trends and cultural influences

- **Output Generation**:
  - Creates unique restaurant name suggestions
  - Develops complete menu items with descriptions
  - Suggests complementary decor and ambiance ideas

- **Presentation**:
  - Results are formatted in an attractive Streamlit UI
  - Organized into clear sections (Name, Concept, Menu)
  - Displayed with appropriate styling for readability
  - Option to regenerate or refine results
