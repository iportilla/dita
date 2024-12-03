'''
    dita.py
'''

import streamlit as st
import requests
import json

# Ollama API endpoint
OLLAMA_API_URL = 'http://localhost:11434/api/generate'

def query_ollama(model_name, prompt):
    headers = {'Content-Type': 'application/json'}
    payload = {
        'model': model_name,
        'prompt': prompt
    }
    response = requests.post(OLLAMA_API_URL, headers=headers, data=json.dumps(payload), stream=True)
    if response.status_code == 200:
        response_text = ''
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode('utf-8'))
                response_text += data.get('response', '')
        return response_text
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
        return None

def main():
    st.title("DITA Converter with Ollama LLM")
    st.write("Convert product release announcements into DITA XML format using a local LLM via Ollama.")

    # Input fields
    announcement = st.text_area("Enter the product announcement:", height=300)

    prompt_options = {
        "Basic Conversion": "Please convert the following product release announcement into DITA XML format, ensuring all information is accurately represented with appropriate tags.\n\n{announcement}",
        "Structured with Specific DITA Elements": "Transform the product release message below into DITA format. Use appropriate DITA elements such as <concept>, <task>, and <reference> where applicable.\n\n{announcement}",
        "Focused on Topic Typing": "Rewrite the following announcement into DITA-compliant XML, organizing the content into topics like <title>, <shortdesc>, <body>, and include any necessary metadata.\n\n{announcement}",
        "Including Metadata and Attributes": "Convert this product release information into DITA format, including relevant metadata and attributes. Ensure the content is properly structured for integration into our documentation system.\n\n{announcement}",
        "Emphasizing Best Practices": "Please reformat the announcement below into DITA XML, adhering to DITA best practices for topic structure and tagging. Ensure the output is suitable for updating our existing documentation.\n\n{announcement}",
        "With Guidance on Content Segmentation": "Break down the following product release announcement into DITA topics, segregating concepts, tasks, and references as appropriate. Provide the content in valid DITA XML format.\n\n{announcement}",
        "For Modular Documentation": "Transform the announcement into modular DITA topics, ensuring each module can stand alone and is correctly linked. Use proper DITA tagging throughout.\n\n{announcement}"
    }

    prompt_choice = st.selectbox("Choose a prompt template:", list(prompt_options.keys()))
    model_name = st.text_input("Enter the Ollama LLM model name (e.g., 'llama3.1'): ", value="llama3.1")

    if st.button("Convert to DITA XML"):
        if not announcement.strip():
            st.error("Please enter the product announcement.")
        else:
            prompt_template = prompt_options[prompt_choice]
            prompt = prompt_template.format(announcement=announcement)
            
            with st.spinner("Generating DITA XML..."):
                dita_output = query_ollama(model_name, prompt)
                if dita_output:
                    st.subheader("Generated DITA XML:")
                    st.code(dita_output, language='xml')

if __name__ == "__main__":
    main()