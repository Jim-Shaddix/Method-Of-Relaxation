[![Gitpod Ready-to-Code](https://img.shields.io/badge/Gitpod-Ready--to--Code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/Jim-Shaddix/Method-Of-Relaxation) 

# Method of Relaxation Dashboard 

## Dash Application:
![](assets/images/application.png)

* This application is deployed on heroku. You can visit the application 
[here!](https://method-of-relaxation.herokuapp.com/)

## Description:
This repository contains code for creating a dashboard application
that displays a surface plot that is associated with a solution to [Laplace's equation](https://en.wikipedia.org/wiki/Laplace%27s_equation)
that was computed using the [Method of Relaxation](https://en.wikipedia.org/wiki/Relaxation_(iterative_method)). 

This dashboard application was built using Python's dash library. 
It allows for the user to specify parameters
associated with a particular problem statement. 

The user can set: 
1. Dimensions of the rectangular system.
2. Constant Boundary Conditions around the rectangular system. 
3. The number of relaxation iterations to run the algorithm with.
 
 The program than uses the input parameters to approximate the solution to Laplace's equation using the
 **Method of Relaxation**.

## Dependencies
* python3.7
* Third party python libraries listed in **requirements.txt**

## Installation Instructions

1. Clone the repo
```Bash
git clone https://github.com/Jim-Shaddix/Personal-Website.git
```
2. You can than use the following command to download all the third party libraries
needed to run this program.
```Bash
pip install -r requirements.txt
```
3. Run the application!
```Bash
python app.py
```

### File Descriptions:
1. **app.py**: contains the code for the dash 
   application that is used for generating the dashboard.
2. **Potential.py**: contains data-structures, as well as the 
   algorithm for the Method of Relaxation that is used in the.
   **Dash-Application.py**
3. **How-It-Works.ipynb**: is a jupyter notebook that describes 
   how the Method of Relaxation works.
4. **Assets**: Contains the stylesheets that are used in the 
   dash application. 
   
