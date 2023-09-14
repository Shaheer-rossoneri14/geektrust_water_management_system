import math
from src.constants import *

class apartment():
    
    def __init__(self, type_of_bhk, corporation_borewell_ratio):
        self.total_guests = 0

        if type_of_bhk == BHK_2:
            self.total_tenants = 3
        elif type_of_bhk == BHK_3:
            self.total_tenants = 5
        else:
            raise Exception("Input for type of bhk is wrong!")
        
        self.monthly_water_allowance = self.total_tenants*10*30
        self.allocated_coorporation_water = 0
        self.allocated_borewell_water = 0
        self.total_water_consumption = self.monthly_water_allowance
        self.total_bill = 0
        self.allot_water(corporation_borewell_ratio)   


    def add_guests(self,no_of_guests):
        self.total_guests += no_of_guests
        self.total_water_consumption += no_of_guests*10*30

    def get_allocation(self, corporation_borewell_ratio):
        cw_multiplier, bw_multiplier = map(int, corporation_borewell_ratio.split(':'))
        total_allowance = self.monthly_water_allowance
        cw = (cw_multiplier/(cw_multiplier+bw_multiplier))*total_allowance
        bw = (bw_multiplier/(cw_multiplier+bw_multiplier))*total_allowance
        
        return cw, bw

    
    def get_cost_by_corporate(self):
        rate = CORPORATE_WATER_RATE
        cost = self.allocated_coorporation_water*rate
        
        return cost

    
    def get_cost_by_borewell(self):
        rate = BOREWELL_WATER_RATE
        cost = self.allocated_borewell_water*rate
        
        return cost
    

    def get_cost_by_tank(self, water_quantity):
        cost = 0

        if water_quantity <= 500:
            cost = water_quantity * 2
        elif water_quantity <= 1500:
            cost = 500 * 2 + (water_quantity - 500) * 3
        elif water_quantity <= 3000:
            cost = 500 * 2 + 1000 * 3 + (water_quantity - 1500) * 5
        else:
            cost = 500 * 2 + 1000 * 3 + 1500 * 5 + (water_quantity - 3000) * 8

        return cost
        

    def calculate_billings(self):
        total = 0
        total += self.get_cost_by_corporate() + self.get_cost_by_borewell()
        additional_water_used = self.total_water_consumption - self.monthly_water_allowance
        total += self.get_cost_by_tank(additional_water_used)
        self.total_bill = math.ceil(total)


    def allot_water(self, corporation_borewell_ratio):
        [allocated_coorporation_water, allocated_borewell_water] = self.get_allocation(corporation_borewell_ratio)
        self.allocated_borewell_water = allocated_borewell_water
        self.allocated_coorporation_water = allocated_coorporation_water
