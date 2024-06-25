class Pipe:
    def __init__(self, diameter_mm, thickness_mm, length_ft):
        self.diameter_mm = float(diameter_mm)
        self.thickness_mm = float(thickness_mm)
        self.length_ft = float(length_ft)
        self.pi = 3.14159
        self.pvc_density = 1450

    def calculate(self):
        try:
            diameter_m = self.diameter_mm / 1000
            thickness_m = self.thickness_mm / 1000
            length_m = self.length_ft * 0.3048

            inner_diameter = diameter_m - (2 * thickness_m)
            volume = (self.pi * ((diameter_m / 2) ** 2 - (inner_diameter / 2) ** 2) * length_m)
            weight = volume * self.pvc_density

            round_volume = round(volume, 4)
            round_weight = round(weight, 4)

            print('Unit Volume = ' + str(round_volume) + 'M^3')
            print('Unit Weight = ' + str(round_weight) + 'Kg')

        except ValueError:
            print('One or more invalid input!')


# Create an instance of the Pipe class
pipe = Pipe(input('Enter Diameter (MM): '), input('Enter Thickness (MM): '), input('Enter Length (FT): '))

# Call the calculate method
pipe.calculate()
