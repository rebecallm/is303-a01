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
bmi_category = ("Underweight" if bmi < 18.5 else
                "Normal weight" if 18.5 <= bmi < 24.9 else
                "Overweight" if 25 <= bmi < 29.9 else
                "Obesity" if bmi >= 30 else "Invalid BMI")

#OUTPUTS
print(f"{name}, your BMI is: {bmi:.2f}")
print (f"Your BMI Category is: {bmi_category}")