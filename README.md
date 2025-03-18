# DE_Covid Project

## Overview
This project analyzes a database containing information on the spread of the COVID-19 virus using Python. It provides data visualizations and a dashboard to better understand the trends and patterns of the virus.

---

## Prerequisites
To run this project, you will need the following Python libraries:

- **numpy**: For numerical operations
- **matplotlib**: For data visualization
- **pandas**: For data manipulation and analysis
- **sqlite3**: For database access
- **streamlit**: For creation of the dashboard 
- **datetime**: For handling dates
- **plotly.express**: For maps visualizations 

---

## Installation Instructions
### Step 1: Install Required Libraries
To install the required dependencies, use **pip**:
```bash
pip install numpy matplotlib pandas
```

### Step 2: Clone This Repository
```bash
   git clone https://github.com/yourusername/yourproject.git
   cd DE_Covid
```

---

## Project Usage
Once the required libraries are installed, you can run the main script:
```bash
python main.py
```
This will execute the analysis and generate the required visualizations.

---

## Repository Structure
The repository consists of the following directories and files:


📂 **data/** — Contains all datasets used for the project.
   - 📄 `day_wise.csv` — The original, unprocessed dataset.
   - 📄 `covid_database.db` — The database containing the tables used for the analysis.

📂 **scripts/** — Contains the source code for the project.
   - 📄 `main.py` — The main script for running the data analysis and generating the dashboard.
   - 📄 `graphical_display.py` — Script for visualization components.
   - 📄 `SIRmodel.py` — Functions related to epidemiological modeling.
   - 📄 `groupings.py` — Functions for grouping COVID-19 data by country or US state.
   - 📄 `generate_new_complete.py` — Script for creating a new completed dataframe from various sources.

📄 **README.md** — This file! Contains documentation and setup instructions.

- **`dashboard`**: Contains the code relating to the visualization of the data in a streamlit dashboard.
   - **`dashboard.py`**: The script that generates the dashboard and executes calls to all the other involved functions.
   - **`maps.py`**: Contains functions to produce maps of the world and individual continents, containing the percentages of active Covid cases in the population with data extracted from new_complete.
   - **requirements.txt**: Contains the necessary libraries and is needed to deploy the dashboard.
...
---

## Project Link
🔗 [GitHub Repository](https://github.com/beatricepicard/DE_covid)

---

## Project Team
This project was developed by:
- **Nataliia Krysanova**
- **Béatrice Picard**
- **Eirini Papathanasiadi**
- **Melanie Ackermann**

---

✨ *Thank you for checking out this project! If you find it useful, consider giving it a star ⭐ on GitHub!*"""