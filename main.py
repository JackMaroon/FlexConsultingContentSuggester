import sys
import random
import csv
from datetime import datetime, timedelta
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt

# OpenAI API configuration
API_URL = "http://localhost:1234/v1/chat/completions"
headers = {"Content-Type": "application/json"}

# List of content themes for financial consultants
themes = [
    "Investment Strategies", "Retirement Planning", "Tax Tips", "Market Analysis",
    "Personal Finance", "Economic Trends", "Risk Management", "Wealth Building",
    "Financial Technology", "Industry News"
]

# List of content types
content_types = [
    "Article", "Infographic", "Short Video", "Poll", "Case Study", "Q&A Session",
    "Client Testimonial", "Market Update", "Tips and Tricks", "Book Recommendation"
]

def query(prompt):
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 150
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def generate_local_ai_content_idea(theme, content_type):
    prompt = f"""Generate a LinkedIn post for a financial consultant.
    Theme: {theme}
    Content Type: {content_type}
    The post should include:
    1. An attention-grabbing opening
    2. A key insight or tip related to {theme}
    3. A call-to-action
    Keep the post concise and professional, suitable for LinkedIn."""

    try:
        output = query(prompt)
        if 'choices' in output and len(output['choices']) > 0:
            generated_text = output['choices'][0]['message']['content'].strip()
        else:
            generated_text = str(output)  # Convert to string in case of unexpected output
        return post_process_content(generated_text, theme, content_type)
    except Exception as e:
        print(f"Error generating AI content: {e}")
        return f"Error: Could not generate content for {theme} - {content_type}. Please try again."

def post_process_content(content, theme, content_type):
    # Remove any text before the actual content (if any)
    content = content.split("LinkedIn post:")[-1].strip()

    # Truncate to 200 characters if longer
    if len(content) > 200:
        content = content[:197] + "..."

    # Ensure the theme is mentioned
    if theme.lower() not in content.lower():
        content = f"{theme}: " + content

    # Add hashtags
    content += f" #{theme.replace(' ', '')} #{content_type.replace(' ', '')}"

    # Check for key components
    if '?' not in content and '!' not in content:
        content = f"🤔 {content}"  # Add an attention-grabbing emoji if no question/exclamation

    if 'http' not in content and 'link' not in content.lower():
        content += " Learn more: [link]"  # Add a generic CTA if none exists

    return content

def create_content_calendar(start_date, num_weeks):
    calendar = []
    current_date = start_date
    for _ in range(num_weeks):
        for _ in range(3):  # 3 posts per week
            theme = random.choice(themes)
            content_type = random.choice(content_types)
            ai_content = generate_local_ai_content_idea(theme, content_type)
            calendar.append((current_date.strftime("%Y-%m-%d"), ai_content))
            current_date += timedelta(days=2)  # Post every other day
        current_date += timedelta(days=1)  # Move to the next week
    return calendar

class ContentSuggesterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LinkedIn Content Suggester with AI")
        self.setGeometry(100, 100, 1000, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.create_widgets()

    def create_widgets(self):
        # Input layout
        input_layout = QHBoxLayout()

        self.start_date_label = QLabel("Start Date (YYYY-MM-DD):")
        self.start_date_input = QLineEdit(datetime.now().strftime("%Y-%m-%d"))
        input_layout.addWidget(self.start_date_label)
        input_layout.addWidget(self.start_date_input)

        self.num_weeks_label = QLabel("Number of Weeks:")
        self.num_weeks_input = QLineEdit("4")
        input_layout.addWidget(self.num_weeks_label)
        input_layout.addWidget(self.num_weeks_input)

        self.generate_button = QPushButton("Generate Calendar")
        self.generate_button.clicked.connect(self.generate_calendar)
        input_layout.addWidget(self.generate_button)

        self.layout.addLayout(input_layout)

        # Calendar display
        self.calendar_table = QTableWidget(0, 3)
        self.calendar_table.setHorizontalHeaderLabels(["Date", "Content", "Actions"])
        self.calendar_table.horizontalHeader().setStretchLastSection(True)
        self.layout.addWidget(self.calendar_table)

        # Save button
        self.save_button = QPushButton("Save to CSV")
        self.save_button.clicked.connect(self.save_to_csv)
        self.layout.addWidget(self.save_button)

    def generate_calendar(self):
        try:
            start_date = datetime.strptime(self.start_date_input.text(), "%Y-%m-%d").date()
            num_weeks = int(self.num_weeks_input.text())

            calendar = create_content_calendar(start_date, num_weeks)

            self.calendar_table.setRowCount(0)
            for date, content in calendar:
                row_position = self.calendar_table.rowCount()
                self.calendar_table.insertRow(row_position)
                self.calendar_table.setItem(row_position, 0, QTableWidgetItem(date))
                self.calendar_table.setItem(row_position, 1, QTableWidgetItem(content))

                regenerate_button = QPushButton("Regenerate")
                regenerate_button.clicked.connect(lambda _, r=row_position: self.regenerate_content(r))
                self.calendar_table.setCellWidget(row_position, 2, regenerate_button)

        except ValueError:
            QMessageBox.critical(self, "Error", "Invalid date format. Please use YYYY-MM-DD.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def regenerate_content(self, row):
        theme = random.choice(themes)
        content_type = random.choice(content_types)
        new_content = generate_local_ai_content_idea(theme, content_type)
        self.calendar_table.setItem(row, 1, QTableWidgetItem(new_content))

    def save_to_csv(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)")
        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["Date", "Content"])  # Header
                    for row in range(self.calendar_table.rowCount()):
                        date = self.calendar_table.item(row, 0).text()
                        content = self.calendar_table.item(row, 1).text()
                        writer.writerow([date, content])
                QMessageBox.information(self, "Success", f"Calendar saved to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = ContentSuggesterApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()