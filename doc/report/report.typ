
#import "template.typ": *
#import "@preview/codelst:2.0.0": sourcecode
#import "@preview/wrap-it:0.1.1": wrap-content

#show: project.with(
  title: "TSM-MachLeData",
  subtitle: "Stock Price Prediction using Machine Learning",
  author: "Justin Ferrara
  Luca Da Silva
  Rafael Cardoso
  Thomas Maksimous",
  affiliation: "HES-SO Master",
  date: datetime(year: 2025, month: 10, day: 20).display("[day].[month].[year]"),
  Licence: "-",
  logo: "assets/HES_SO_Logo_RGB.png",
  toc_title: "Table of Contents",
)

//set block-quote
#let blockquote = rect.with(stroke: (left: 2.5pt + luma(170)), inset: (left: 1em))
#let primary-color = rgb("E94845")
#let secondary-color = rgb(255, 80, 69, 60%)

#show raw.where(block: true): block.with(
  fill: rgb(240, 240, 240), // Fond gris clair
  inset: 8pt, // Marge intérieure
  radius: 4pt, // Coins arrondis
  width: 100%, // Largeur
)
#show raw.where(block: true): set text(font: "Source Code Pro")

#pagebreak()

= Introduction

The objective is to create a simple predictive market model. The model would take as input the stock closing price for each month, with the goal of predicting the closing prices for the next 5 days. The dataset would consist of the past year's data for the top 100 stocks of a stock market index.

As an advanced MLOps problem, we will study the data drift in our results. The goal is to fine-tune our model every week using the new data from the previous week. We will then compare the performance of our models over time. The objective here is to observe whether the performance of older models degrades over time compared to their updated fine-tuned versions. (Model drift)

#pagebreak()

= Advanced Topic - Data Drift

In machine learning systems, *model drift* (also known as concept drift) refers to the degradation of a model's predictive performance over time due to changes in the underlying data distribution or relationships between input and output variables. This phenomenon occurs because the model was trained on past data that may no longer represent current real-world conditions. In financial forecasting, for instance, market trends, investor behavior, or economic indicators may evolve, causing previously learned patterns to become outdated. Detecting and managing model drift is therefore critical to maintaining accuracy and reliability in predictive systems.

One key source of model drift is *data drift*, which occurs when the statistical properties of input features (the X variables) change over time. For example, if stock trading volumes or volatility levels shift due to external economic events, the distribution of input data no longer aligns with what the model originally learned. Data drift can be measured through statistical tests such as the Kolmogorov-Smirnov test or by comparing feature distributions between training and production data. Regular monitoring allows to identify when the input data environment has shifted significantly, prompting the need for model retraining or adjustment.

A related but distinct phenomenon is *feature drift*, which occurs when the relevance or predictive power of certain input features changes relative to others. For example, a feature like "daily trading volume" might become less predictive of price movement if market liquidity conditions change. Feature drift affects model interpretability and can mislead the model's weighting of inputs, even if overall data distributions appear stable. Detecting feature drift often involves monitoring metrics like feature importance or mutual information across time.

Finally, *label drift* (or target drift) refers to a change in the distribution of the target variable (Y). In stock prediction, this could occur if the overall market sentiment changes and the expected returns follow a different trend than before. Label drift can appear independently of input changes. For instance, when a company changes its dividend policy or experiences sudden external shocks. Continuous evaluation on recent labeled data helps detect this drift and guides the decision to retrain or recalibrate the model.

Together, these forms of drift—model, data, feature, and label, highlight the importance of dynamic monitoring and adaptation in MLOps. Properly managing them ensures that machine learning models remain accurate, fair, and robust in evolving real-world environments.

TODO more references and go deeper

= Project Scoping

The project aims to develop a machine learning model to predict stock opening prices, while implementing a comprehensive MLOps lifecycle to ensure the model's robustness and adaptability over time.

== Objectives

The objective of this project is to predict the opening stock value of different companies using machine learning techniques. The purpose is to provide useful insights to investors, helping them make more informed and data-driven investment decisions. The key problem to solve is the accurate prediction of stock prices, which varies due to market volatility and numerous influencing factors.

The advanced MLOps topic covered in this project will be Model Drift detection and mitigation, more specifically the Data Drift and Feature Drift aspects. In this context, we will monitor how changes in the input data distribution over time affect the model's performance. The main goal is to maintain the model's reliability and adaptability, ensuring it remains at its best performance level even as market conditions evolve.

== Requirements

This project will require the following resources:
- Financial datasets containing daily stock data (open, close, high, low, volume, etc.) with sufficient historical depth.
- Development environment for data science and MLOps:
  - Python (pandas, scikit-learn, TensorFlow/PyTorch)
  - DVC or MLflow for experiment tracking and versioning
  - Docker and GitHub Actions for CI/CD
  - Cloud or local deployment environment (e.g., Google Cloud, Azure, or Kubernetes cluster)

Monitoring tools to track model drift (e.g., Evidently AI, Prometheus + Grafana, or custom scripts).

== Project Constraints and Associated Risks

The project operates under multiple constraints and risks that could influence its success. Time limitations may restrict the extent of model experimentation and deployment testing, while limited financial domain expertise could block accurate interpretation of market-related outcomes. Additionally, access to reliable financial data may be limited or require paid sources, and the technical complexity of implementing MLOps processes such as continuous integration, monitoring, and retraining adds further challenges.

These constraints comes with risks including potential costs associated with cloud technologies and APIs, the inherent instability of models due to unpredictable market dynamics, and the possibility of overfitting, which could reduce the model's ability to generalize effectively to unseen market conditions.

= Data Engineering

The data engineering phase is crucial for the success of the stock price prediction project. It involves several key steps to ensure that the data is properly collected, processed, and stored for effective use in machine learning models.

== Data Acquisition

To acquire the necessary data for stock price prediction, we used the #link("https://www.nasdaq.com")[https://www.nasdaq.com] website to download historical stock data for 20 stocks in the NASDAQ index. The data collected is in CSV format, and contains columns such as Date, Close, Open, High, Low, and Volume for the past 5 years. The following companies were selected for this project:
- Apple Inc. (AAPL)
- AMD Inc. (AMD)
- Amazon.com, Inc. (AMZN)
- ASML Holding N.V. (ASML)
- Broadcom Inc. (AVGO)
- Cisco Systems, Inc. (CSCO)
- Alphabet Inc. (GOOGL)
- International Business Machines Corporation (IBM)
- Facebook, Inc. (META)
- Microsoft Corporation (MSFT)
- Micron Technology, Inc. (MU)
- Netflix, Inc. (NFLX)
- NVIDIA Corporation (NVDA)
- Oracle Corporation (ORCL)
- Palantir Technologies Inc. (PLTR)
- Qualcomm Incorporated (QCOM)
- Starbucks Corporation (SBUX)
- Tencent Holdings Ltd. (TCEHY)
- Tesla, Inc. (TSLA)
- Taiwan Semiconductor Manufacturing Company Ltd. (TSM)

== Data Preprocessing

The preprocessing steps involved cleaning the data and transforming the data into a suitable format for modeling. We performed the following preprocessing tasks:
- Checking for missing values and handling them appropriately (e.g., imputation or removal).
- Converting the closing prices to float data variables, representing the variation in percent from the previous closing price.
- Normalizing the data to ensure that all features are on a similar scale, which is important for machine learning algorithms.
- Splitting the data into training, validation, and test sets to evaluate the model's performance effectively.

== Data Storage

The raw and preprocessed data are stored in a structured format using CSV files and DVC for version control. This allows us to track changes in the data over time and ensures reproducibility in our experiments. The data is stored in a dedicated S3 bucket for easy access and scalability (as shown in the tutorial #link("https://mlops.swiss-ai-center.ch/")[https://mlops.swiss-ai-center.ch/]).

= ML Model Development

To develop the machine learning model for stock price prediction, we followed the #link("https://mlops.swiss-ai-center.ch/")[https://mlops.swiss-ai-center.ch/] guide to set up our MLOps pipeline. This involved several key steps to ensure that the model is trained, validated, and deployed effectively.

== Feature Engineering

TODO

== Model Training and Validation

The model is trained using the preprocessed data, which includes the stock closing prices and other relevant features. We used LSTM (Long Short-Term Memory) neural networks, which are well-suited for time series data like stock prices. The training process involves optimizing the model's parameters to minimize the prediction error on the training set.

The validation set is used to tune hyperparameters and prevent overfitting.

TODO more details

== Model Evaluation

The model's performance is evaluated using metrics such as Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and R-squared (R²). These metrics provide insights into how well the model predicts stock prices compared to actual values. We also perform backtesting to assess the model's performance over historical data.

Here is a brief explanation of the evaluation metrics used:
- The Mean Absolute Error (MAE) measures the average absolute difference between predicted and actual values, showing how far predictions are from reality on average.
- The Root Mean Squared Error (RMSE) calculates the square root of the average squared errors, giving more weight to larger mistakes and highlighting significant prediction deviations.
- The R-squared (R²) indicates how well the model explains the variance in the actual data, with values closer to 1 representing better predictive accuracy.

The best and worst predictions are visualized using plots to illustrate the model's performance and to better understand its strengths and weaknesses.

= Deployment

TODO

== CI/CD Pipeline

TODO

== Infrastructure

TODO

== Scalability

TODO

= Monitoring

TODO

== Data Drift Detection

TODO

= Conclusion

Assessment ??

TODO
