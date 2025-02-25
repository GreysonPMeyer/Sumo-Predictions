# Sumo-Predictions
This project uses data science classification techniques to predict the outcome of Makuuchi sumo bouts. By leveraging historical match data, we aim to provide insights into which wrestler is most likely to win based on various features.

## Features
- **Classification Models**: Machine learning models trained to predict match outcomes.
- **Data Exploration**: Insights into sumo wrestling trends and features that influence bout outcomes.
- **Feature Engineering**: Transforming raw data into meaningful inputs for classification.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Getting Started](#getting-started)
3. [Dataset](#dataset)
4. [Methodology](#methodology)
5. [Results](#results)
6. [Usage](#usage)
7. [Technologies Used](#technologies-used)
8. [Future Work](#future-work)
9. [Contributing](#contributing)
10. [License](#license)

---

## Project Overview
The goal of this project is to:
- Improve understanding of sumo match dynamics.
- Provide reliable predictions of match outcomes using machine learning models.

---

## Getting Started
### Prerequisites
To run this project, you'll need:
- Python 3.9 or higher
- A working knowledge of pandas, scikit-learn, and matplotlib (or install requirements using the command below).

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/GreysonPMeyer/Sumo-Predictions.git

2. Navigate to the proper directort:
   cd sumo-match-outcome-predictor

3. Install dependencies:
pip install -r requirements.txt

## Dataset
The dataset is ultimate_sumo_dataset.py. It consists of sumo matches from 1985 - 2019, including features such as:

Wrestler names
Ranks
Historical win/loss records
Difference in rank between fighters

Data preprocessing is handled in data_preprocessing.py.

## Methodology
Steps
1. Data Cleaning: Removing null values and redundant information
2. Feature Engineering: Removing unneeded variables and creating derived variables such as rank difference and head-to-head record.
3. Model Training: Using classification algorithms such as:
   Linear Discriminant Analysis
   Quadratic Discriminant Analysis
   Logistic Regression
   Support Vector Classifiers
   Gaussian Naive Bayes
   K Nearest Neighbors
   Decision Trees
   Random Forests
   Bagging Classifier
   Pasting Classifier
   AdaBoost
   Voting Classifier
4. Evaluation: Models are evaluated using metrics such as accuracy, precision, recall, and roc_auc score.

   ## Results
The pasting classifier had the best overall performance with a 60.57% average of the above evaluation metrics.

## Technologies Used
Programming Language: Python
Libraries:
pandas, numpy (data processing)
scikit-learn (classification models)
matplotlib, seaborn (visualizations)

## Future Work
Incorporate more advanced features, such as:
A moving window of win-loss ratios for each pair of rikishi.
Wrestling styles and techniques.
Tournament-specific trends.
Experiment with deep learning models for prediction.
Develop a web app for users to input match data and get predictions.

## Acknowledgements
Data sourced from https://www.kaggle.com/datasets/thedevastator/sumo-wrestling-matches-results-1985-2019#:~:text=the%20original%20authors.-,Data%20Source,-License

