# Superside - Project Quotation Tool

## 📌 Overview
The **Superside Project Quotation Tool** is a web application built with **Streamlit** that helps Project Managers generate quotations for creative projects efficiently. This project was developed in just a few hours as a proof of concept (POC) for a solution to present during a company recruitment assessment. The tool uses **AI-powered analysis** to identify project components from a brief and estimates work hours based on predefined complexity metrics.

## 🚀 Features
- **Project Brief Analysis**: AI extracts relevant project components.
- **Dynamic Data Editing**: Modify extracted components.
- **Automated Quotation Calculation**: Estimates work hours.
- **JSON Export**: Download quotations in JSON format.

## 📂 Project Structure

```sh
|-- src/
|   |-- main.py                  # Streamlit app main file
|   |-- structured_data.json     # JSON file containing project components
|   |-- quotation_hours.csv      # CSV file mapping work hours to project components
|-- requirements.txt             # Required Python dependencies
|-- README.md                    # Project documentation
```

## 🛠️ Installation & Setup

### 1️⃣ Prerequisites
Ensure **Python 3.8+** is installed.

### 2️⃣ Clone the Repository
```sh
git clone https://github.com/YOUR-USERNAME/superside-quotation-tool.git
cd superside-quotation-tool
```
### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```
### 4️⃣ Set Up OpenAI API Key
Create a ```.streamlit/secrets.toml``` file:
```ini
[secrets]
OPENAI_API_KEY = "your-api-key"
```
### 5️⃣ Run the Application
```sh
streamlit run src/main.py
```
## 🧩 How It Works
1. **Enter Project Brief**: Provide a textual description of the project.
2. **Identify Components**: AI extracts key project elements from the database.
3. **Modify Components**: Users can edit, add, or remove items in the interactive table.
4. **Generate Quotation**: The system calculates estimated work hours.
5. **Download Output**: Save the quotation in JSON format.

## 💡 Technologies Used
- **Streamlit** - Web UI framework for Python.
- **OpenAI API** - Used to analyze project briefs.
- **Pandas** - Data manipulation and calculations.
- **JSON & CSV** - Data storage for project components and estimations.

## 🔄 Future Improvements
- ✅ Improve AI accuracy for better component extraction.
- ✅ Enhance UI/UX for better usability.

## 👨‍💻 Author
**Paolo Piacenti** - _AI Product Manager_

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Made with ❤️ by Paolo Piacenti 🚀

