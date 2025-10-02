### requirements.txt
```txt
pandas>=1.3.0
matplotlib>=3.5.0
seaborn>=0.11.0
streamlit>=1.12.0
wordcloud>=1.8.0
jupyter>=1.0.0
numpy>=1.21.0
```

### README.md
```markdown
# CORD-19 Data Analysis Project

## Overview
This project analyzes the CORD-19 dataset containing COVID-19 research papers metadata. It includes data exploration, cleaning, visualization, and an interactive Streamlit application.

## Project Structure
```
Frameworks_Assignment/
│
├── data_exploration.py      # Part 1: Data loading and exploration
├── data_cleaning.py         # Part 2: Data cleaning and preparation
├── analysis_visualization.py # Part 3: Analysis and visualization
├── app.py                   # Part 4: Streamlit application
├── requirements.txt         # Python dependencies
├── README.md               # Project documentation
└── images/                 # Generated visualizations
```

## Setup Instructions

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Download the dataset:**
   - Download `metadata.csv` from [CORD-19 Kaggle](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge)
   - Place it in the project root directory

3. **Run the analysis:**
   ```bash
   # Run data exploration
   python data_exploration.py
   
   # Run data cleaning
   python data_cleaning.py
   
   # Run analysis and visualization
   python analysis_visualization.py
   
   # Run Streamlit app
   streamlit run app.py
   ```

## Key Findings

### Publication Trends
- Rapid increase in COVID-19 research publications starting 2020
- Peak publication year identified with maximum research output

### Journal Analysis
- Identification of top journals publishing COVID-19 research
- Distribution of publications across different sources

### Content Analysis
- Most frequent words in paper titles reflect research focus areas
- Abstract length distribution shows typical paper structure

## Challenges and Learnings

### Challenges
1. **Data Size:** Large dataset required efficient memory management
2. **Missing Data:** Significant missing values in certain columns
3. **Data Quality:** Inconsistent date formats and text data

### Learnings
1. **Data Cleaning:** Effective strategies for handling real-world messy data
2. **Visualization:** Creating meaningful charts for different data types
3. **Interactive Apps:** Building user-friendly interfaces for data exploration

## Streamlit Application Features
- Interactive filters for year range and journals
- Real-time visualizations updates
- Data sampling and statistics
- Responsive layout for different screen sizes

## Future Enhancements
- Advanced text analysis of abstracts
- Author collaboration networks
- Topic modeling of research themes
- Integration with full text analysis
```

## Usage Instructions

1. **First, install all required packages:**
```bash
pip install pandas matplotlib seaborn streamlit wordcloud jupyter
```

2. **Run the scripts in order:**
```bash
# Start with exploration
python data_exploration.py

# Then clean the data
python data_cleaning.py

# Generate visualizations
python analysis_visualization.py

# Finally, run the Streamlit app
streamlit run app.py
```

3. **For the Streamlit app, open your browser and go to:**
```
http://localhost:8501
```
