# DeFi-smart-assistant

A RAG (Retriever Augmented Generation) powered smart assistant for DeFi.

## Prerequisites

- Python (version 3.11.8)
- Pip (version 23.3.1)
- A `.env` file with the following fields
    ```text
    PINECONE_API_KEY=<your_api_key>
    PINECONE_INDEX_NAME=<index_name>
- `Ollama`

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/your-repository.git
    ```

2. Navigate to the project directory:

    ```bash
    cd project-directory
    ```

3. Create a new python environment (here we are using conda)

    ```bash
    conda create --name <myenv> python=3.11
    conda activate <myenv>
    ```

4. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Load in `mistral-7B` and run the app:

    ```bash
    ollama pull mistral
    streamlit run app.py
    ```

2. The app will open in your web browser.

## License

This project is licensed under the [MIT License](LICENSE).
 
