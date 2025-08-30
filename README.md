
<p align="center">
   <img src="https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white" alt="Python">
   <img src="https://img.shields.io/badge/Streamlit-%23FF4B4B.svg?logo=streamlit&logoColor=white" alt="Streamlit">
   <img src="https://img.shields.io/badge/LangGraph-Graph%20AI-purple" alt="LangGraph">
   <img src="https://img.shields.io/badge/License-MIT-green" alt="MIT License">
</p>

# 🌈 MultiToolBot

<p align="center">
   <b>An elegant, professional chatbot application built with Python and Streamlit, leveraging LangGraph for advanced conversational flows and modular tool integration.</b>
</p>

<p align="center">
   <img src="ezgif.com-speed (6).gif" alt="MultiToolBot Demo" width="600">
</p>

---

## ✨ Features

🎤 <b>Conversational AI</b>: Natural language understanding and response generation.<br>
🧩 <b>Modular Tooling</b>: Easily extendable with custom tools via <code>tools_setup.py</code>.<br>
🔗 <b>Graph-based Workflow</b>: Flexible conversation management using LangGraph.<br>
🎨 <b>Streamlit UI</b>: Clean, interactive web interface for seamless user experience.<br>

---

### 📦 Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/Sampavi01/MultiToolBot.git
    cd MultiToolBot
    ```
2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

### ▶️ Running the App
Start the Streamlit server:
```sh
streamlit run app.py
```

The app will be available at <span style="color:#FF4B4B">http://localhost:8501</span> by default.

---

## 🗂️ Project Structure
```text
LangGraph_Chatbot/
│
├── app.py              # Main Streamlit application
├── graph_setup.py      # LangGraph workflow setup
├── tools_setup.py      # Tool integration and configuration
├── requirements.txt    # Python dependencies
├── .gitignore          # Git ignore rules
└── __pycache__/        # Python cache files (ignored)
```

---


## 🛠️ Customization
- Add or modify tools in <code>tools_setup.py</code> to extend chatbot capabilities.
- Adjust conversation logic in <code>graph_setup.py</code>.

### 📁 Screenshots Folder

You can find all Streamlit screenshots in the [`images/` folder](./images/).

---

## 📄 License
This project is licensed under the MIT License.

---

<p align="center">
   <i>🌟 Crafted for professional, scalable conversational AI solutions. 🌟</i>
</p>
