# FlexConsultingContentSuggester

This application helps financial consultants generate engaging LinkedIn content using AI. The tool uses a locally hosted model by default but can be configured to use any AI model, including OpenAI's. It generates professional and relevant posts based on specified themes and content types, allows users to generate a content calendar, and saves the generated content to a CSV file.

## Features

- **AI-Generated Content**: Uses a locally hosted AI model by default. It can be configured to use any AI model, including OpenAI's GPT-3.5-turbo, to generate LinkedIn posts based on specified themes and content types.
- **Content Calendar**: Automatically generates a content calendar with posts scheduled for several weeks.
- **Customizable Inputs**: Users can specify the start date and the number of weeks for the content calendar.
- **CSV Export**: Save the generated content calendar to a CSV file.
- **Regenerate Content**: Regenerate individual content entries if needed.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/linkedin-content-suggester.git
    cd linkedin-content-suggester
    ```

2. Create a virtual environment and install dependencies:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3. Ensure you have the locally hosted AI model running. If you wish to use OpenAI's API instead, you can set it up by following the instructions on the [OpenAI documentation](https://beta.openai.com/docs/).

4. Update the API URL and headers in the code if necessary:
    ```python
    # Example for locally hosted model
    API_URL = "http://localhost:1234/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    
    # Example for OpenAI
    API_URL = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": "Bearer YOUR_OPENAI_API_KEY",
        "Content-Type": "application/json"
    }
    ```

## Usage

1. Run the application:
    ```bash
    python main.py
    ```

2. Use the GUI to specify the start date and number of weeks for the content calendar.

3. Click "Generate Calendar" to create the content calendar.

4. View and regenerate content as needed using the provided buttons.

5. Save the content calendar to a CSV file by clicking "Save to CSV".

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Google](https://ai.google.dev/gemma) for providing the open source gemma 2 model.
- [PyQt5](https://pypi.org/project/PyQt5/) for the GUI framework.
- [Aiohttp](https://docs.aiohttp.org/en/stable/) for asynchronous HTTP requests.
