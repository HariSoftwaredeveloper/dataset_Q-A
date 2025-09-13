How to use this code:

    Save this code to a Python file, e.g., app.py.

    Make sure you have installed required libraries:

text
pip install streamlit faiss-cpu sentence-transformers openai pandas numpy

Set your OpenAI API key as an environment variable in your terminal:

    Linux/macOS:

text
export OPENAI_API_KEY="your_api_key_here"

Windows PowerShell:

    text
    setx OPENAI_API_KEY "your_api_key_here"

Then restart your terminal/IDE.

Run the app:

text
streamlit run app.py

The app will open in the browser allowing you to ask medical questions.
