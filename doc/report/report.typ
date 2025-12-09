
#import "template/isc_template_report.typ": *

// Inline code formatting
#show raw.where(block: false): it => block(
  fill: rgb(220, 220, 220),
  radius: 0.5mm,
  inset: 0.2mm,
  it,
)
#show raw.where(block: true): set text(font: "Cascadia Code")

#show: project.with(
  title: "Stock Price Prediction using Machine Learning",
  sub-title: "Advanced MLOps Topic: Data Drift",
  course-name: "TSM-MachLeData",
  course-supervisor: "Beat Wolf
	Bertil Chapuis",
  semester: "S1 -",
  academic-year: "2025-2026",

  cover-image: image("template/cover.png"),
  cover-image-height: 10cm, // Default value = 10cm
  cover-image-caption: " ",

  authors: ("Justin Ferrara", "Luca Da Silva", "Rafael Cardoso", "Thomas Maksimous"),

  logo: image("template/logo.png"),
  date: datetime.today().display("[day].[month].[year]"),
  language: "en", // Or en if required
  version: "1.0.0",
)

#pagebreak()

= Introduction

The objective of this project is to create a simple predictive model capable of estimating future stock prices. The model uses historical monthly closing prices as input and predicts the closing prices for the following five days. The dataset consists of five years of historical data for several major technology companies listed on the NASDAQ.

As part of the advanced MLOps component, the project focuses on analysing data drift and its impact on model performance. Each week, a data drift analysis is done as well as a new model is re-trained with newly collected data. The performance of the newly created model is then compared to older versions. This approach allows us to evaluate whether previously trained models degrade over time as market conditions evolve. The goal is to understand how data drift affects predictive accuracy and to highlight the value of continuous monitoring and retraining within an MLOps workflow.

The results of this project will provide insights into the challenges of stock price prediction and the importance of managing data drift in machine learning systems deployed in dynamic environments.

#pagebreak()

= Advanced Topic - Data Drift

The following section provides an in-depth explanation of model drift, data drift, feature drift, and label drift, along with methods for detecting data drift in machine learning systems @evidently_data_drift_article @evidently_explainer_drift @detecting_data_drift_article_meduim @detecting_data_drift_article_mlmastery @detecting_data_drift_article_labelyourdata.

In machine learning systems, *model drift* (also known as concept drift) refers to the degradation of a model's predictive performance over time due to changes in the underlying data distribution or relationships between input and output variables. This phenomenon occurs because the model was trained on past data that may no longer represent current real-world conditions. In financial forecasting, for instance, market trends, investor behavior, or economic indicators may evolve, causing previously learned patterns to become outdated. Detecting and managing model drift is therefore critical to maintaining accuracy and reliability in predictive systems.

One key source of model drift is *data drift*, which occurs when the statistical properties of input features (the X variables) change over time. For example, if stock trading volumes or volatility levels shift due to external economic events, the distribution of input data no longer aligns with what the model originally learned. Data drift can be measured through statistical tests such as the Kolmogorov-Smirnov test or by comparing feature distributions between training and production data. Regular monitoring allows to identify when the input data environment has shifted significantly, prompting the need for model retraining or adjustment.

A related but distinct phenomenon is *feature drift*, which occurs when the relevance or predictive power of certain input features changes relative to others. For example, a feature like "daily trading volume" might become less predictive of price movement if market liquidity conditions change. Feature drift affects model interpretability and can mislead the model's weighting of inputs, even if overall data distributions appear stable. Detecting feature drift often involves monitoring metrics like feature importance or mutual information across time.

Finally, *label drift* (or target drift) refers to a change in the distribution of the target variable (Y). In stock prediction, this could occur if the overall market sentiment changes and the expected returns follow a different trend than before. Label drift can appear independently of input changes. For instance, when a company changes its dividend policy or experiences sudden external shocks. Continuous evaluation on recent labeled data helps detect this drift and guides the decision to retrain or recalibrate the model.

Together, these forms of drift—model, data, feature, and label, highlight the importance of dynamic monitoring and adaptation in MLOps. Properly managing them ensures that machine learning models remain accurate, fair, and robust in evolving real-world environments.

== Data Drift Detection

Data drift detection involves monitoring changes in the statistical properties of input features over time. Common techniques include:
- Statistical tests: Methods like the Kolmogorov-Smirnov test or Chi-squared test compare feature distributions between training and production data to identify significant shifts @evidently_data_drift_article @evidently_explainer_drift.
- Distance metrics: Measures such as Kullback-Leibler divergence or Jensen-Shannon divergence quantify the difference between probability distributions of features over time @evidently_data_drift_article @evidently_explainer_drift.
- Visualization: Tools like histograms, box plots, or density plots help visualize changes in feature distributions @detecting_data_drift_article_mlmastery.
- Machine learning-based methods: Unsupervised models (e.g., autoencoders) can learn normal data patterns and flag deviations as potential drift @detecting_data_drift_article_mlmastery.

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

These constraints come with risks including potential costs associated with cloud technologies and APIs, the inherent instability of models due to unpredictable market dynamics, and the possibility of overfitting, which could reduce the model's ability to generalize effectively to unseen market conditions.

= Fisrt Version

TODO cite @stock_ml_repo_pr6

== Data Engineering

The data engineering phase is crucial for the success of the stock price prediction project. It involves several key steps to ensure that the data is properly collected, processed, and stored for effective use in machine learning models.

=== Data Acquisition

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

The data spans from 11/10/2020 to 11/07/2025 for each stock, providing a comprehensive dataset for training and evaluating the machine learning models.

=== Data Preprocessing

The preprocessing steps involved cleaning the data and transforming the data into a suitable format for modelling. We performed the following preprocessing tasks:
- Checking for missing values and handling them appropriately (e.g., imputation or removal).
- Converting the closing prices to float data variables, representing the variation in percent from the previous closing price.
- Normalizing the data to ensure that all features are on a similar scale, which is important for machine learning algorithms.
- Splitting the data into training, validation, and test sets to evaluate the model's performance effectively.

=== Data Storage

The raw and pre-processed data are stored in a structured format using CSV files and DVC for version control. This allows us to track changes in the data over time and ensures reproducibility in our experiments. The data is stored in a dedicated S3 bucket for easy access and scalability (as shown in the tutorial #link("https://mlops.swiss-ai-center.ch/")[https://mlops.swiss-ai-center.ch/]).

== ML Model Development

To develop the machine learning model for stock price prediction, we followed the #link("https://mlops.swiss-ai-center.ch/")[https://mlops.swiss-ai-center.ch/] guide to set up our MLOps pipeline. This involved several key steps to ensure that the model is trained, validated, and deployed effectively.

=== Feature Engineering

TODO

=== Model Training and Validation

The model is trained using the pre-processed data, which includes the stock closing prices and other relevant features. We used LSTM (Long Short-Term Memory) neural networks, which are well-suited for time series data like stock prices. The training process involves optimizing the model's parameters to minimize the prediction error on the training set.

The validation set is used to tune hyperparameters and prevent overfitting.

TODO more details

=== Model Evaluation

The model's performance is evaluated using metrics such as Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and R-squared (R²). These metrics provide insights into how well the model predicts stock prices compared to actual values. We also perform back testing to assess the model's performance over historical data.

Here is a brief explanation of the evaluation metrics used:
- The Mean Absolute Error (MAE) measures the average absolute difference between predicted and actual values, showing how far predictions are from reality on average.
- The Root Mean Squared Error (RMSE) calculates the square root of the average squared errors, giving more weight to larger mistakes and highlighting significant prediction deviations.
- The R-squared (R²) indicates how well the model explains the variance in the actual data, with values closer to 1 representing better predictive accuracy.

The best and worst predictions are visualized using plots to illustrate the model's performance and to better understand its strengths and weaknesses.

== Deployment

To deploy the model, we use the #link("https://mlops.swiss-ai-center.ch/")[https://mlops.swiss-ai-center.ch/] guidelines to set up a base environment for deployment.

The model is trained locally. On every pull request, the model is retrained in a Kubernetes pod using GitHub Actions. The trained model is then containerized using Docker and deployed to a cloud environment (e.g., AWS, GCP, or Azure) for scalability and accessibility. This setup corresponds to the #link("https://mlops.swiss-ai-center.ch/part-3-serve-and-deploy-the-model/chapter-37-use-a-self-hosted-runner-for-the-cicd-pipeline/")[Chapter 3.7] of the MLOps guide.

TODO

=== CI/CD Pipeline

The CI/CD pipeline, defined in the MLOps workflow, automates the entire lifecycle of model development, testing, and deployment using GitHub Actions, DVC, CML, and BentoML. It runs on a self-hosted runner for training tasks and on GitHub-hosted runners for deployment.

The pipeline is triggered automatically when:
- Code is pushed to the main branch,
- A pull request is opened, or
- It is manually triggered via the GitHub Actions interface.

It consists of two main jobs:
1. Train and Report (train-and-report)

  Triggered on pull requests, this job automates model training and performance reporting:
  - Checks out the repository and sets up `Python 3.12`.
  - Installs dependencies and authenticates with Google Cloud.
  - Reproduces the model training pipeline using DVC (`dvc repro --pull`).
  - Pushes updated model artifacts and metrics to the DVC remote storage.
  - Automatically commits changes to `dvc.lock`.
  - Generates a CML report comparing the new experiment results to the main branch, including:
    - Parameter and metric differences (dvc params diff, dvc metrics diff),
    - Visual comparisons of plots (training history, prediction previews, and confusion matrices).
  - Publishes the report as a comment in the pull request for review.
2. Publish and Deploy (publish-and-deploy)

  Runs when changes are merged into the main branch. It performs the following steps:
  - Checks out the repository and installs dependencies.
  - Authenticates with Google Cloud and reproduces the final model pipeline using DVC.
  - Imports and builds the BentoML model artifact.
  - Containerizes the Bento model and pushes Docker images to the Google Container Registry.
  - Retrieves credentials for the Google Kubernetes Engine (GKE) cluster.
  - Updates the Kubernetes deployment manifest to reference the new image version (based on the Git SHA).
  - Applies the updated deployment and service configuration to deploy the new model version to Kubernetes.

=== Infrastructure

The infrastructure for deploying the machine learning model is set up using Google Cloud Platform (GCP). We utilize Google Kubernetes Engine (GKE) to manage the containerized application, ensuring scalability and reliability. The model is containerized using Docker, allowing for consistent deployment across different environments.

=== Scalability

As the model is deployed on GKE, it can easily scale based on demand. Kubernetes allows us to define resource limits and auto-scaling policies to handle varying workloads. This ensures that the application remains responsive even during peak usage times.

= Performance Improvements

As seen in the previous section, the initial model@stock_ml_repo_pr6 was not performing well, with high error rates and low predictive accuracy. To address these issues, we implemented several performance improvements to enhance the model's capabilities, described in detail in PR @stock_ml_repo_pr10.

== Feature Engineering Enhancements

To improve the model's performance, we extended the input data to include the past 60 days of stock prices instead of just 30 days. This provided the model with more historical context, allowing it to capture longer-term trends and patterns in stock price movements.

We also added new features derived from the existing data, to provide additional insights for the model. These features are described in the following table:
- *Short-term trend indicators:* Computed 5-day and 10-day simple moving averages (SMA_5, SMA_10) to smooth short-horizon fluctuations and capture underlying price trends.
- *Recent-information-weighted trend measure:* Incorporated a 5-day exponential moving average (EMA_5) to assign greater weight to recent observations and enhance sensitivity to short-term market movements.
- *Volatility approximation:* Derived a High-Low price spread feature as a proxy for intraday volatility.
- *Directional price-movement ratio:* Constructed an Open-to-Close price ratio to quantify daily directional bias.
- *Volume-based activity metric:* Calculated the percentage change in trading volume to characterize shifts in market activity.

== Model Architecture Optimization

To avoid overfitting and improve generalization, we increased the dropout rate in the LSTM layers from 0.1 to 0.2. This adjustment helped the model to better handle unseen data by preventing it from relying too heavily on specific neurons during training.

== Results

The performance improvements led to significant enhancements in the model's predictive accuracy and reliability. The key results are summarized in the pull request @stock_ml_repo_pr10, which includes:
- A reduction in Mean Absolute Error (MAE) from 1.87 to 0.66.
- An decrease in R2 Score from 0.00 to -1.19 (which is not an improvement but expected due to the nature of stock price prediction).
- Visualizations comparing the model's predictions before and after the improvements, demonstrating better alignment with actual stock prices.

= Data Drift Analysis and Integration

To strengthen the robustness of the stock-prediction workflow, data drift detection was integrated directly into the MLOps pipeline with pull request @stock_ml_repo_pr12. The `Evidently` package was added as the primary toolkit for measuring drift on the prepared datasets @evidently_data_drift_preset. The package `Evidently` was chosen due to its comprehensive suite of drift detection methods, based on multiple algorithms depending on the column type @evidently_explainer_drift.

== Prepared Step Improvements

The data preparation stage was expanded to output two parallel datasets:

- Candidate data: the newly prepared dataset generated from the latest weekly ingestion (from folder `data/raw_candidate/`).
- Current data: the previously accepted dataset used for training the active model (from folder `data/raw/`).

These datasets are stored in `data/prepared/` and `data/prepared_candidate/` respectively, allowing for direct comparison of feature distributions over time.

== Pipeline Enhancements

A new data drift detection step was added to the workflow. This component:

- Loads the current and candidate prepared datasets.
- Uses Evidently to compute drift metrics across all features.
- Generates:
  - An HTML report for human-readable inspection.
  - A JSON report containing structured drift statistics suitable for automated analysis.
- Stores both reports as pipeline artifacts.
- Inserts a summary of the JSON report into pipeline comments for quick visibility during CI/CD reviews.

This approach ensures that every potential model update is automatically preceded by a drift evaluation that highlights feature-level changes.

The pipeline comment summarizes the key findings from the JSON report, including:
- If a significant drift was detected for any features.
- The number of drifted columns (features).
- The number of columns analyzed (features).

An example of the pipeline comment is shown in pull request @stock_ml_repo_pr12. The @evidently_html_report_no_drift shows the generated report from the `Evidently` package on the original data without drift.

#figure(
  image("./img/originalDataDrift.png"),
  caption: [
    Data Drift Report Example from Evidently
  ],
) <evidently_html_report_no_drift>

== Data Drift Detection Strategy

The first step in our data drift detection strategy is to compare the statistical distributions of features between the current and candidate datasets. Using Evidently built-in statistical tests (e.g., Kolmogorov-Smirnov test for continuous features, Chi-squared test for categorical features), we assess whether significant changes have occurred in the input data over time.

The second step to detect data drift involves a dual-model strategy within the pipeline. The idea is to train and evaluate two models in parallel: a base model that remains fixed over time (based on initial data), and a new model, trained with the latest data (`candidate` model) on a weekly basis.

By comparing the performance difference between these two models over time, we can infer whether drift is present. When the fine-tuned model consistently outperforms the fixed base model on new data, it signals that the distribution has shifted and that continuous retraining is necessary for optimal predictive accuracy.

== Monitoring Approach

Monitoring is performed exclusively through the pipeline rather than a dedicated external monitoring service. This setup enables:

- Regular evaluation of drift through Evidently
- Tracking performance of both base and fine-tuned models
- Automated generation of drift reports as part of routine CI/CD operations

Although this approach ensures consistent oversight during the weekly data refresh cycle, it does not offer real-time monitoring or the granular diagnostics provided by specialized observability platforms. Nonetheless, it remains a practical approach within the project scope and supports effective detection of data drift and early signs of model degradation.

== Results and Findings

The integration of data drift detection into the MLOps pipeline provided valuable insights into the stability of the input data over time. However, the analysis revealed that no significant data drift was detected between the current and candidate datasets. Both models—the fixed base model and the fine-tuned candidate model—performed similarly over time, indicating that the underlying data distribution remained relatively stable during the evaluation period. This might be attributed to the nature of stock market data, which can exhibit periods of stability interspersed with volatility. The pull request @stock_ml_repo_pr12 contains detailed results and visualizations from the drift analysis.

To have a better comprehension of the data drift and to show a sample of the results obtained, a fake data drift has been implemented in branch @stock_ml_repo_branch_artificial_drift. This allows to see how the data drift detection works in practice and to validate the effectiveness of the implemented approach. The @evidently_html_report_simulated_drift shows an example of data drift detected using the fake data drift implementation.

#figure(
  image("./img/simulatedDataDrift.png"),
  caption: [
    Artificial Data Drift Report Example from Evidently
  ],
) <evidently_html_report_simulated_drift>

= Conclusion

This project demonstrated how a complete MLOps workflow can support the development of a stock price prediction model, from data acquisition and preprocessing to training, deployment, and automated monitoring. Although stock forecasting remains challenging and the model's predictive performance is limited, the improvements introduced—especially in feature engineering and model tuning—led to more stable results.

Data drift detection was successfully integrated into the pipeline using Evidently. While no real drift was observed in the available data, the artificial drift experiment confirmed that the system can identify and report distribution changes when they occur. This validates the monitoring approach and ensures that future updates can be assessed reliably.

The project's main limitations are the restricted feature set and the simplicity of the model architecture. Future work could include richer financial indicators, macroeconomic variables, more advanced models, and real-time monitoring. Despite these limitations, the project provides a solid foundation for an automated, drift-aware forecasting pipeline.

#pagebreak()

// Bibliography
#bibliography("./assets/bib.yml", full: true)
