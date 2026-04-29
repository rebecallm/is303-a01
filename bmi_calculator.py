'''
Rebeca Llontop
IS 303 - A01

BMI Calculator
Calculates body mass index from height and weight

Inputs:
-Name (string)
-Height in inches (float)
-Weight in pounds (float)

Processes:
- Convert height and weight to appropriate units
- Calculate BMI: (weight in pounds / (height in inches)^2) * 703

Outputs:
- Print name and BMI index 
- BMI Category 

'''
#INPUTS
name = input("What is your name? ")
height = float(input("What is your height in inches? "))
weight = float(input("How much do you weigh in pounds? "))

#PROCESSES
bmi = (weight / (height ** 2)) * 703

#OUTPUTS
print(f"{name}, your BMI is: {bmi:.2f}")