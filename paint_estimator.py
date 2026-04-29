"""
Rebeca Llontop
IS 303 - A01

Paint Estimator
Calculates the amount in gallons of paint needed to cover a room

Inputs:
- Room name (string)
- wall height in feet (float)
- total wall width in feet (float)

Processes:
- Multiply wall height by total wall width to get total square footage
- Divide total square footage by 350 to get gallons of paint needed 
(1 gallon covers 350 square feet)

Outputs:
- Print the name of room and the number of gallons needed
"""

#INPUTS
room_name = input("What is the name of the room? ")
wall_height = float(input("What is the height of the walls in feet? "))
total_wall_width = float(input("What is the total width of the walls in feet? "))

#PROCESSES
total_square_footage = wall_height * total_wall_width
gallons_needed = total_square_footage / 350

#OUTPUTS
print(f"For the {room_name}, you will need {gallons_needed:.2f} gallons of paint.")
