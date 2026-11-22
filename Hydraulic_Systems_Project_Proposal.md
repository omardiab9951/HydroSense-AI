# **Project Proposal: AI-Based Condition Monitoring and Fault Diagnosis of Industrial Hydraulic Systems** 

## **1. Project Overview** 

The proposed project aims to develop a Machine Learning-based system for monitoring the condition of industrial hydraulic systems and identifying component degradation. 

The project will use real experimental sensor data collected from a hydraulic system to train ML models capable of identifying the operating condition of different hydraulic components. 

The main objective is to demonstrate how Data Science and Machine Learning can help industrial facilities monitor equipment health, identify potential faults, and support predictive maintenance decisions. 

## **2. Problem Statement** 

Hydraulic systems are widely used in industrial applications, including manufacturing machinery, industrial presses, construction equipment, and production systems. 

These systems depend on several important components, such as pumps, valves, coolers, and accumulators. 

Over time, these components may experience degradation or faults due to continuous operation, wear, leakage, temperature changes, and other operating conditions. 

Traditional maintenance approaches may involve periodic inspections or responding after a machine develops a problem. These approaches can result in unexpected equipment failures, production interruptions, increased maintenance costs, and reduced operational efficiency. 

Therefore, there is a need for a data-driven approach that can analyze industrial sensor measurements and identify component degradation automatically. 

#### **The main problem this project addresses is:** 

How can Machine Learning techniques analyze sensor measurements from an industrial hydraulic system to identify the condition and degradation level of its components? 

## **3. Proposed Solution** 

We propose developing an AI-based condition monitoring and fault diagnosis system using Machine Learning. 

The system will analyze measurements collected from multiple sensors installed in an experimental hydraulic system, including pressure, temperature, vibration, motor power, and fluid flow sensors. 

Using these measurements, ML models will learn patterns associated with different component conditions and predict the degradation level of the selected hydraulic component. 

The project will focus on predicting component conditions rather than simply detecting whether a machine is working or failing. 

Hydraulic Systems Condition Monitoring - Project Proposal  |  Page 1 

For example, the model could classify a hydraulic valve into different operating conditions: 

- Optimal switching. 

- Small switching delay. 

- Severe switching delay. 

- Near-total switching failure. 

The resulting predictions can help engineers understand equipment conditions and make more informed maintenance decisions. 

## **4. Dataset Description** 

**Dataset name:** Condition Monitoring of Hydraulic Systems. 

**Source:** UCI Machine Learning Repository. 

#### **Official dataset link:** 

https://archive.ics.uci.edu/dataset/447/condition+monitoring+of+hydraulic+systems 

**Dataset license:** Creative Commons Attribution 4.0 International (CC BY 4.0). 

The dataset is publicly available and can be downloaded and used directly, subject to its attribution requirements. 

### **Dataset characteristics** 

- 2,205 operating cycles. 

- 17 sensor channels. 

- 43,680 raw measurements per operating cycle. 

- Each operating cycle represents 60 seconds of system operation. 

- Real experimental measurements collected using a hydraulic test rig. 

### **Input Features (X)** 

The dataset includes different sensor measurements: 

- 1 **Pressure sensors (PS1–PS6):** Measure hydraulic pressure. 

- 2 **Motor power sensor (EPS1):** Measures motor power consumption. 

- 3 **Flow sensors (FS1–FS2):** Measure hydraulic fluid flow. 

- 4 **Temperature sensors (TS1–TS4):** Measure fluid temperatures. 

- 5 **Vibration sensor (VS1):** Measures system vibration. 

- 6 **Virtual sensors (CE, CP, SE):** Provide calculated indicators related to cooling and efficiency. 

### **Target Variables (Y)** 

The dataset provides condition labels for four hydraulic components: 

- 1 **Cooler condition:** Different cooling efficiency levels. 

- 2 **Valve condition:** Different switching performance levels. 

- 3 **Pump condition:** No leakage, weak leakage, or severe leakage. 

- 4 **Accumulator condition:** Different pressure levels. 

The project can focus on one component or investigate all four components. 

Hydraulic Systems Condition Monitoring - Project Proposal  |  Page 2 

## **5. Complete Machine Learning Pipeline** 

The project will follow the standard Data Science and Machine Learning workflow. 

### **Phase 1: Data Understanding** 

- Understand the hydraulic system and its components. 

- Understand the dataset structure and sensor measurements. 

- Identify input features and target variables. 

- Understand how the data was collected. 

### **Phase 2: Exploratory Data Analysis (EDA)** 

- Analyze feature distributions. 

- Investigate sensor measurement patterns. 

- Identify relationships between sensor measurements. 

- Analyze component condition distributions. 

- Visualize correlations and possible degradation patterns. 

### **Phase 3: Data Cleaning** 

- Check for missing values. 

- Identify duplicate records. 

- Investigate unusual sensor readings and potential outliers. 

- Check data consistency across sensor files. 

- Handle any identified data quality issues appropriately. 

### **Phase 4: Data Integration and Feature Engineering** 

- Combine measurements from different sensor files. 

Extract statistical features from the sensor signals, such as: 

- Mean. 

- Standard deviation. 

- Minimum. 

- Maximum. 

- Root Mean Square (RMS). 

- Generate a structured dataset suitable for ML training. 

- Investigate and remove irrelevant or redundant features when justified. 

### **Phase 5: Data Preprocessing** 

- Encode categorical target variables if necessary. 

- Scale numerical features when required by the selected algorithm. 

- Investigate class imbalance. 

- Apply appropriate techniques if class imbalance affects model performance. 

- Split the data into training and testing sets while considering the experimental cycle structure. 

Hydraulic Systems Condition Monitoring - Project Proposal  |  Page 3 

### **Phase 6: Machine Learning Model Development** 

Several classification algorithms will be investigated and compared, including: 

- Logistic Regression. 

- Decision Tree. 

- Random Forest. 

- Support Vector Machine (SVM). 

- XGBoost. 

The models will be trained using the engineered sensor features to predict hydraulic component conditions. 

### **Phase 7: Model Evaluation** 

The models will be evaluated using appropriate classification metrics: 

- Accuracy. 

- Precision. 

- Recall. 

- F1-score. 

- Confusion Matrix. 

The objective is to identify the most suitable model for predicting component degradation. 

### **Phase 8: Model Interpretation** 

Feature importance and model interpretation techniques will be used to investigate which sensor measurements contribute most to identifying component degradation. 

## **6. Expected Outcomes** 

The expected outcome is a trained Machine Learning model capable of identifying the operating condition of a hydraulic component based on industrial sensor measurements. 

The project should demonstrate: 

- How industrial sensor data can be transformed into useful information. 

- How Machine Learning can identify patterns associated with component degradation. 

- Which algorithms perform best for the selected classification task. 

- Which sensor measurements are most informative for fault diagnosis. 

- How data-driven condition monitoring can support industrial maintenance decisions. 

## **7. Potential Project Contribution** 

Rather than simply implementing an existing classification algorithm, the project will investigate the effectiveness of different Machine Learning approaches. 

Potential contributions include: 

- Comparing raw sensor representations with statistical feature extraction. 

- Comparing multiple ML algorithms. 

- Investigating the importance of different sensor measurements. 

- Studying the effect of class imbalance on model performance. 

Hydraulic Systems Condition Monitoring - Project Proposal  |  Page 4 

- Investigating the ability to identify early-stage degradation. 

The final contribution will depend on the experiments and results obtained. 

## **8. Project Scope and Limitations** 

This project will focus on offline Machine Learning experimentation using the publicly available UCI dataset. 

It will not initially involve connecting to physical industrial machinery, installing sensors, or implementing a live industrial monitoring system. 

The dataset was collected from an experimental hydraulic test rig, not an Egyptian factory. Therefore, the results will demonstrate a methodology potentially applicable to industrial facilities in Egypt, but will not establish performance on Egyptian factory equipment without further validation. 

Additionally, the project focuses on component condition classification rather than predicting exact failure times or Remaining Useful Life (RUL). 

## **9. Suggested Project Title** 

#### **AI-Based Condition Monitoring and Fault Diagnosis of Industrial Hydraulic Systems Using Machine Learning** 

## **10. Main Objective** 

To develop and evaluate a Machine Learning-based approach for identifying degradation conditions in industrial hydraulic systems using experimental multisensor data, following a complete Data Science pipeline from data exploration and preprocessing to model training, evaluation, and interpretation. 

Hydraulic Systems Condition Monitoring - Project Proposal  |  Page 5 

