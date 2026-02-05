# Correlation Analysis Summary

## Data Relationship Types in Health and Sports Science

This document summarizes the various types of relationships that may exist between data in the health and sports science domain, including linear and non-linear relationships, along with corresponding detection techniques.

---

## 1. Relationship Types Overview

| Category | Relationship Type | Description | Health Domain Example | Detection Technique |
|----------|------------------|-------------|----------------------|---------------------|
| **Linear** | Positive Correlation | Variable A increases, Variable B also increases proportionally | Steps↑ → Calories burned↑ | Pearson Correlation |
| **Linear** | Negative Correlation | Variable A increases, Variable B decreases proportionally | Age↑ → Max heart rate↓ | Pearson Correlation |
| **Non-linear** | Monotonic Non-linear | Continuous increase/decrease, but non-uniform rate | Exercise frequency↑ → Cardio fitness↑ (diminishing returns) | Spearman Rank Correlation |
| **Non-linear** | U-shaped | Minimum point exists, higher at both ends | BMI vs Mortality (both underweight and overweight increase risk) | Polynomial Regression |
| **Non-linear** | Inverted U-shaped | Optimal point exists, lower at both ends | Exercise volume↔HRV (moderate is best) | Polynomial Regression |
| **Non-linear** | Threshold Effect | Sudden change at a critical point | SpO2: >95% normal, <90% dangerous | Piecewise Regression |
| **Non-linear** | Lag Effect | Impact appears with delay | Today's intense exercise → Tomorrow's HRV change | Time-lagged Correlation |
| **Non-linear** | Interaction Effect | Multiple variables combined produce special effects | Caffeine + Evening exercise → Poor sleep | Mutual Information, Random Forest |

---

## 2. Detailed Descriptions

### 2.1 Linear Relationships

#### 2.1.1 Positive Correlation
- **Definition**: When one variable increases, another variable also increases proportionally
- **Mathematical Characteristic**: Correlation coefficient r > 0
- **Health Domain Examples**:
  - Steps ↔ Calories burned
  - Exercise duration ↔ Heart rate elevation
  - Training load ↔ Fatigue perception
- **Detection Technique**: Pearson Correlation Coefficient
- **Python Implementation**: `scipy.stats.pearsonr()`

#### 2.1.2 Negative Correlation
- **Definition**: When one variable increases, another variable decreases proportionally
- **Mathematical Characteristic**: Correlation coefficient r < 0
- **Health Domain Examples**:
  - Age ↔ Max heart rate (decreases ~1 bpm per year of age)
  - Stress index ↔ HRV
  - Sedentary time ↔ Cardiorespiratory fitness
- **Detection Technique**: Pearson Correlation Coefficient
- **Python Implementation**: `scipy.stats.pearsonr()`

---

### 2.2 Non-linear Relationships

#### 2.2.1 Monotonic Non-linear (Diminishing/Increasing Returns)
- **Definition**: Variable continuously increases or decreases, but at a non-uniform rate
- **Health Domain Examples**:
  - Exercise frequency ↔ Cardio fitness: 0→3 times/week shows significant improvement, 3→6 times/week shows smaller gains
  - Meditation duration ↔ Stress reduction: First 10 minutes most effective
  - Sleep duration ↔ Recovery effect: First 6 hours most significant
- **Detection Technique**: Spearman Rank Correlation
- **Python Implementation**: `scipy.stats.spearmanr()`
- **Identification Method**: When |Spearman| > |Pearson| + 0.2, suggests non-linearity

#### 2.2.2 U-shaped Relationship
- **Definition**: A minimum point exists, with higher values at both ends
- **Health Domain Examples**:
  - BMI ↔ Mortality rate: Both underweight and overweight increase risk
  - Sodium intake ↔ Cardiovascular risk
- **Detection Technique**: Polynomial Regression (quadratic term)
- **Python Implementation**: `numpy.polyfit(x, y, 2)`

#### 2.2.3 Inverted U-shaped Relationship
- **Definition**: An optimal point exists, with lower values at both ends
- **Health Domain Examples**:
  - Exercise volume ↔ HRV: Moderate exercise improves HRV, excessive exercise reduces it
  - Sleep duration ↔ Cognitive performance: 7-8 hours optimal
  - Caffeine intake ↔ Exercise performance: Moderate enhances, excessive diminishes
  - Training intensity ↔ Adaptation effect
- **Detection Technique**: Polynomial Regression (negative quadratic coefficient)
- **Python Implementation**: `numpy.polyfit(x, y, 2)`, check quadratic coefficient

#### 2.2.4 Threshold Effect
- **Definition**: At a critical point, the relationship changes suddenly
- **Health Domain Examples**:
  - SpO2: >95% normal, <90% suddenly dangerous
  - Sleep duration: <5 hours causes sharp cognitive decline
  - Exercise heart rate: Exceeding 85% max HR enters anaerobic zone
  - HRV threshold: Below certain value indicates overtraining
- **Detection Technique**: Piecewise Regression
- **Python Implementation**: `pwlf` library or custom segmented model

#### 2.2.5 Lag Effect
- **Definition**: Impact of one variable appears in another variable after a time delay
- **Health Domain Examples**:
  - Today's exercise → Tomorrow's HRV: HRV first decreases then increases (24-48 hours)
  - Stress event → Sleep quality: Stress may affect sleep 1-2 days later
  - Dietary changes → Weight: Effects take weeks to manifest
  - Training load → Fatigue accumulation: 1-3 day delay
- **Detection Technique**: Time-lagged Correlation Analysis
- **Python Implementation**: `pandas.DataFrame.shift()` + correlation analysis

#### 2.2.6 Interaction Effect
- **Definition**: Two or more variables combined produce special effects; individually may show no correlation
- **Health Domain Examples**:
  - Caffeine + Exercise timing: Afternoon caffeine + evening exercise = poor sleep
  - Stress + Alcohol: Alcohol's impact on HRV is greater under high stress
  - Altitude + Exercise intensity: Moderate intensity at high altitude causes heart rate response similar to high intensity at low altitude
  - Age + Exercise type: Recovery differences in elderly for HIIT vs aerobic
- **Detection Technique**: Mutual Information, Random Forest Feature Importance
- **Python Implementation**: `sklearn.feature_selection.mutual_info_regression()`

---

## 3. Technical Approach Summary

| Relationship Type | Primary Detection Method | Python Library/Function | Output Metric | Applicable Scenario |
|-------------------|-------------------------|------------------------|---------------|---------------------|
| Linear Positive | Pearson Correlation | `scipy.stats.pearsonr()` | r value (-1 to 1) | Continuous variables, normal distribution |
| Linear Negative | Pearson Correlation | `scipy.stats.pearsonr()` | r value (-1 to 1) | Continuous variables, normal distribution |
| Monotonic Non-linear | Spearman Rank | `scipy.stats.spearmanr()` | ρ value (-1 to 1) | Ordinal variables, non-normal |
| U-shaped/Inverted U | Polynomial Regression | `numpy.polyfit()` | Quadratic coefficient, R² | Optimal/worst point exists |
| Threshold Effect | Piecewise Regression | `pwlf` / custom | Breakpoint location, slope change | Critical point detection |
| Lag Effect | Lagged Correlation | `pandas.shift()` + correlation | Optimal lag time, correlation strength | Time series data |
| Interaction Effect | Mutual Information | `sklearn.mutual_info_regression()` | MI value | Discover complex dependencies |
| Interaction Effect | Random Forest | `sklearn.RandomForestRegressor()` | Feature importance | Auto-discover interactions |

---

## 4. MVP Implementation Priority

| Priority | Relationship Type | Rationale |
|----------|------------------|-----------|
| P0 (Must Have) | Linear Correlation | Foundational functionality |
| P0 (Must Have) | Monotonic Non-linear | Low implementation cost |
| P0 (Must Have) | Inverted U-shaped | Core health domain scenario |
| P1 (Important) | Threshold Effect | Health alert functionality |
| P1 (Important) | Lag Effect | Behavioral impact insights |
| P2 (Enhancement) | Interaction Effect | Auto-discover complex patterns |

---

*Document Version: 1.0*  
*Created: 2026-02-04*
