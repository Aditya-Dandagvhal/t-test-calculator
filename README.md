# Small Sampling T-Test Analyzer

## Description
This project is a GUI-based application developed using Python and Tkinter to perform statistical t-tests. It helps users analyze sample data and make decisions based on hypothesis testing.

---

## Features
- One Sample T-Test
- Two Sample T-Test
- Paired T-Test
- User-friendly GUI interface
- Accurate statistical calculations

---

## Code Explanation

### 1. t_critical_value() Function
This function retrieves the critical t-value from a predefined t-table based on:
- Degrees of Freedom (df)
- Significance level (alpha)
- Type of test (one-tailed or two-tailed)

It ensures df stays within valid range and selects the closest alpha value.

---

### 2. One Sample T-Test
This function:
- Calculates mean and standard deviation of sample data
- Computes t-statistic using formula
- Compares calculated value with critical value
- Accepts or rejects null hypothesis

---

### 3. Two Sample T-Test
- Compares means of two independent samples
- Uses pooled standard deviation
- Determines statistical significance

---

### 4. Paired T-Test
- Used for dependent samples
- Calculates differences between pairs
- Performs t-test on differences

---

### 5. GUI (Tkinter)
- Entry fields for user input
- Buttons to trigger calculations
- Labels/text areas to display results

---

## Requirements
- Python installed
- Required libraries: math, statistics, tkinter

---

## How to Run
1. Download the project
2. Open in VS Code
3. Run:
   python t-test.py

---
