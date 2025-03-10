#1. Project "DE_covid"
# This project analyzes database that contains information on the spread of the COVID-19 virus using Python and provides data visualizations (dashboard).

#2. Prerequisites
#  To run the code, you will need the following Python libraries:
- **numpy**: For numerical operations
- **matplotlib**: For data visualization
- **pandas**: For data manipulation and analysis
- ...

# Follow the steps below to set up your environment and run the project.

#3. Installation instructions
# To install the required libraries, you can use **pip** (Python's package installer):
```bash
pip install numpy matplotlib pandas
```
# Clone this repository:
```bash
   git clone https://github.com/yourusername/yourproject.git
   cd DE_Covid
```
#4. Project Usage
# After installing the required libraries, you can run the Python code:
```bash
python main.py
```
# This will execute the main script of the project, which contains the analysis and visualizations.

#5. Repository Structure
# The repository has the following structure:

- **`data/`**: Contains all datasets used for the project. This folder may include both raw and processed data.
   - **`day_wise.csv`**: The original, unprocessed dataset.
   - **`....csv`**: The cleaned and processed version of the dataset ready for analysis.

- **`scripts`**: Contains the source code for the project.
   - **`main.py`**:The main script for running the data analysis and generating dashboard.
   - **`graphical_display.py`**: .
   - **`SIRmodel.py`**: Function for part 1.2 of the project.
   - **`groupings.py`**: Functions that group the amounts of people in each category over all available dates by country or US state. 

- **`dashboard`**: Contains the code relating to the visualization of the data in a streamlit dashboard.
   - **`dashboard.py`**: The script that generates the dashboard and executes calls to all the other involved functions.
   - **`maps.py`**: Contains functions to produce maps of the world and individual continents, containing the percentages of active Covid cases in the population with data extracted from worldometer_data and country_wise.
...

   - **`README.md`**: This file! It contains the project documentation, including setup instructions, usage details, and other important information about the project.

# Project Link: https://github.com/beatricepicard/DE_covid

#6. Project covid 3 members

# Nataliia Krysanova
# Béatrice Picard
# Eirini Papathanasiadi
# Melanie Ackermann





