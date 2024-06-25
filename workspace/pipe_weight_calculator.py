"""This module provides a function to calculate the volume and weight of a PVC pipe
based on its diameter, thickness, and length.
"""
from math import pi

PVC_DENSITY = 1450  # kg/m^3


def main() -> None:
    """This function prompts the user to enter the diameter (in millimeters),
    thickness (in millimeters), and length (in feet) of a PVC pipe.
    It then calculates the volume (in cubic meters) and weight (in kilograms)
    of the pipe and prints the results.
    """
    try:
        diameter_mm = float(input('Enter Diameter (MM): '))
        thickness_mm = float(input('Enter Thickness (MM): '))
        length_ft = float(input('Enter Length (FT): '))

        diameter_m = diameter_mm / 1000
        thickness_m = thickness_mm / 1000
        length_m = length_ft * 0.3048

        inner_diameter = diameter_m - (2 * thickness_m)
        volume = pi * ((diameter_m / 2) ** 2 - (inner_diameter / 2) ** 2) * length_m
        weight = volume * PVC_DENSITY

        print(f'\nUnit Volume = {volume:.4f} M^3')
        print(f'Unit Weight = {weight:.4f} Kg')
    except ValueError:
        print('One or more invalid input!')


if __name__ == '__main__':
    main()
