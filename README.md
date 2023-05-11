# Housing_Price_Prediction_Project

This project aims to predict housing prices in King County, WA using multiple regression analysis. The training data provided by Flatiron School's Data Science Immersive program phase 2 final project will be utilized. The SciKit Python library will be used to build and train the final model.

# Business Problem
A Seattle real estate company intends to expand its portfolio in King County and seeks accurate sales price predictions for properties. This will enable them to strategize their investment options effectively and maximize profits. A multiple linear regression model will be constructed based on the provided property data to address this challenge.

During the exploratory phase, the following questions will be addressed:

* Which location in the county has the highest property value?
* Which property aspects contribute to its value?
* Does renovation have an effect on property value?

# Approach
The project began with data integrity checks and statistical tests, including ANOVA and Welch's T-test, to identify significant factors within the data. The analysis revealed that the property's zip code, renovation status, presence of a basement, and property condition were significant factors influencing its value.

Next, various features were engineered to enhance the linear regression modeling. Some features were transformed into Bernoulli distributions to be used as categorical data, such as the presence of a master bathroom. Ordinal values like bedrooms and bathrooms were squared to emphasize the impact of multiple bedrooms and bathrooms on property prices.

Finally, four linear regression models were created. The baseline model utilized the statsmodels OLS method and heavily relied on engineered features. Three additional models were developed using Scikit-Learn libraries: basic linear regression, linear regression with recursive feature elimination, and linear regression with recursive feature elimination and cross-validation. After conducting coefficient analysis, the model employing recursive feature elimination demonstrated the most stability and was selected as the final implementation.

The repository contains the code, data, and findings summarizing the project's methodology and insights gained from the analysis.
