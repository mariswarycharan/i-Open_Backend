from fastapi import FastAPI
import pandas as pd
from typing import List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
    
# Function to calculate total cost for a drug
def calculate_total_cost(dosage, cost_per_vial, procedure_cost, consulting_charges, oct_cost, travel_cost, food_cost, miscellaneous_cost, patient_lost_opportunity_cost, caregiver_lost_opportunity_cost):
    dosage = int(dosage)
    dosage_half = dosage / 2

    total_package_cost = int((cost_per_vial + procedure_cost) * dosage)
    total_consulting_charges = int(consulting_charges * (dosage + dosage_half))
    total_oct_charges = int(oct_cost * (dosage + dosage_half))
    total_travel_food_cost = int((travel_cost + food_cost + miscellaneous_cost) * (dosage + dosage_half))
    total_opportunity_cost_lost = int((patient_lost_opportunity_cost * (dosage + dosage_half)) + (caregiver_lost_opportunity_cost * (dosage + dosage_half)))

    total_cost_per_patient = (total_package_cost + total_consulting_charges + total_oct_charges +
                            total_travel_food_cost + total_opportunity_cost_lost)
    
    return total_package_cost, total_consulting_charges, total_oct_charges, total_travel_food_cost, total_opportunity_cost_lost, total_cost_per_patient

from fastapi import FastAPI, Form

app = FastAPI()

origins = [
    "http://10.1.75.50:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "http://0.0.0.0:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def status_check():    
    return {"status": "Healthy and running project is on live"}


class InputData(BaseModel):
    account_type: str = "Government Account"
    drugs_selected: List[str] = ["Drug 1", "Drug 2", "Drug 3", "Drug 4", "Drug 5"]
    disease_indication: str = "WET AMD"
    time_horizon: str = "1"
    government_ac: str = "Yes"
    patient_support: str = "Yes"
    naive_switch: str = "Naive"
    clinical_status: str = "Per Label"
    drug1_dosage: int = 3
    drug2_dosage: int = 3
    drug3_dosage: int = 5
    drug4_dosage: int = 8
    drug5_dosage: int = 8
    procedure_cost: int = 1000
    oct_cost: int = 200
    consulting_charges: int = 200
    miscellaneous_cost: int = 100
    travel_cost: int = 100
    food_cost: int = 100
    patient_lost_opportunity_cost: int = 1000
    caregiver_lost_opportunity_cost: int = 1000
    First_Drug: str = "Drug 1"
    Second_Drug: str = "Drug 2"

@app.post("/submit")
async def submit_form(data: InputData):
    
    print(data)
    
    account_type = data.account_type
    drugs_selected = data.drugs_selected
    disease_indication = data.disease_indication
    time_horizon = data.time_horizon
    government_ac = data.government_ac
    patient_support = data.patient_support
    naive_switch = data.naive_switch
    clinical_status = data.clinical_status
    drug1_dosage = data.drug1_dosage
    drug2_dosage = data.drug2_dosage
    drug3_dosage = data.drug3_dosage
    drug4_dosage = data.drug4_dosage
    drug5_dosage = data.drug5_dosage
    procedure_cost = data.procedure_cost
    oct_cost = data.oct_cost
    consulting_charges = data.consulting_charges
    miscellaneous_cost = data.miscellaneous_cost
    travel_cost = data.travel_cost
    food_cost = data.food_cost
    patient_lost_opportunity_cost = data.patient_lost_opportunity_cost
    caregiver_lost_opportunity_cost = data.caregiver_lost_opportunity_cost
    First_Drug = data.First_Drug
    Second_Drug = data.Second_Drug
    
    
    
    if account_type == "Government Account":
        drug1_cost_per_vial=60000  #---Drug 1 = Faricimab
        drug2_cost_per_vial=45000 #---Drug 2 = Aflibercept
        drug3_cost_per_vial=25000 #---Drug 3 = Brolucizumab
        drug4_cost_per_vial=18000  #---Drug 4 = Ranibizumab
        drug5_cost_per_vial=10000  #---Drug 5 = Rani Biosimilar
        
    if account_type == "Trade Account":
        if patient_support == "Yes":
            drug1_cost_per_vial=30000 
            drug2_cost_per_vial=24000 
            drug3_cost_per_vial=35000 
            drug4_cost_per_vial=25000 
            drug5_cost_per_vial=20000 
            
        else:
            drug1_cost_per_vial=75000  
            drug2_cost_per_vial=60000 
            drug3_cost_per_vial=35000 
            drug4_cost_per_vial=25000  
            drug5_cost_per_vial=20000 
    
    
    drug_dosages = {
        ("WET AMD", "1", "Naive", "Per Label"): {"Drug 1": 6, "Drug 2": 8, "Drug 3": 8, "Drug 4": 12, "Drug 5": 12},
        ("WET AMD", "2", "Naive", "Per Label"): {"Drug 1": 9, "Drug 2": 14, "Drug 3": 12, "Drug 4": 24, "Drug 5": 24},
        ("WET AMD", "3", "Naive", "Per Label"): {"Drug 1": 12, "Drug 2": 20, "Drug 3": 16, "Drug 4": 36, "Drug 5": 36},
        ("WET AMD", "4", "Naive", "Per Label"): {"Drug 1": 15, "Drug 2": 26, "Drug 3": 20, "Drug 4": 48, "Drug 5": 48},
        ("WET AMD", "5", "Naive", "Per Label"): {"Drug 1": 18, "Drug 2": 32, "Drug 3": 24, "Drug 4": 60, "Drug 5": 60},
        ("DME", "1", "Naive", "Per Label"): {"Drug 1": 6, "Drug 2": 9, "Drug 3": 9, "Drug 4": 12, "Drug 5": 12},
        ("DME", "2", "Naive", "Per Label"): {"Drug 1": 9, "Drug 2": 15, "Drug 3": 13, "Drug 4": 24, "Drug 5": 24},
        ("DME", "3", "Naive", "Per Label"): {"Drug 1": 12, "Drug 2": 21, "Drug 3": 17, "Drug 4": 36, "Drug 5": 36},
        ("DME", "4", "Naive", "Per Label"): {"Drug 1": 15, "Drug 2": 27, "Drug 3": 21, "Drug 4": 48, "Drug 5": 48},
        ("DME", "5", "Naive", "Per Label"): {"Drug 1": 18, "Drug 2": 33, "Drug 3": 25, "Drug 4": 60, "Drug 5": 60},
        ("WET AMD", None, "Switch", "Per Label"): {"Drug 1": 3, "Drug 2": 6, "Drug 3": 4, "Drug 4": 12, "Drug 5": 12},
        ("DME", None, "Switch", "Per Label"): {"Drug 1": 3, "Drug 2": 6, "Drug 3": 4, "Drug 4": 12, "Drug 5": 12},
    }
    
    if clinical_status == "Per Label":
        
        key = (disease_indication, time_horizon if naive_switch == "Naive" else None, naive_switch, clinical_status)
        dosage_info = drug_dosages.get(key, {})
        
        drug_dosages_side_bar_data = dosage_info
        
        dosage_info = { i:j for i,j in dosage_info.items() if i in drugs_selected }

        try:drug1_dosage = dosage_info.get("Drug 1") 
        except: drug1_dosage = 0
        try:drug2_dosage = dosage_info.get("Drug 2") 
        except: drug2_dosage = 0
        try:drug3_dosage = dosage_info.get("Drug 3") 
        except: drug3_dosage = 0
        try:drug4_dosage = dosage_info.get("Drug 4") 
        except: drug4_dosage = 0
        try:drug5_dosage = dosage_info.get("Drug 5") 
        except: drug5_dosage = 0

    else:
        drug_dosages_side_bar_data = {}
    
    # ------------------------------------------- bar graph data ----------------------------------------------
    
    # Dictionary to hold drug details
    drugs = {
        'Drug 1': {'dosage': drug1_dosage, 'cost_per_vial': drug1_cost_per_vial},
        'Drug 2': {'dosage': drug2_dosage, 'cost_per_vial': drug2_cost_per_vial},
        'Drug 3': {'dosage': drug3_dosage, 'cost_per_vial': drug3_cost_per_vial},
        'Drug 4': {'dosage': drug4_dosage, 'cost_per_vial': drug4_cost_per_vial},
        'Drug 5': {'dosage': drug5_dosage, 'cost_per_vial': drug5_cost_per_vial}
    }
    
    drugs = {i: (j if i in drugs_selected else None) for i, j in drugs.items()}
    
    # Dictionary to hold calculated costs
    drug_costs = {}

    # Calculate costs for each drug
    for drug, details in drugs.items():
        if details != None:
            drug_costs[drug] = calculate_total_cost(details['dosage'], details['cost_per_vial'], procedure_cost, consulting_charges, oct_cost, travel_cost, food_cost, miscellaneous_cost, patient_lost_opportunity_cost, caregiver_lost_opportunity_cost)
        if details == None:
            drug_costs[drug] = (0, 0, 0, 0, 0, 0)

    # Unpack costs for individual drugs if needed
    drug1_total_package_cost, drug1_total_consulting_charges, drug1_total_oct_charges, drug1_total_travel_food_cost, drug1_total_opportunity_cost_lost, drug1_total_cost_per_patient = drug_costs['Drug 1']
    drug2_total_package_cost, drug2_total_consulting_charges, drug2_total_oct_charges, drug2_total_travel_food_cost, drug2_total_opportunity_cost_lost, drug2_total_cost_per_patient = drug_costs['Drug 2']
    drug3_total_package_cost, drug3_total_consulting_charges, drug3_total_oct_charges, drug3_total_travel_food_cost, drug3_total_opportunity_cost_lost, drug3_total_cost_per_patient = drug_costs['Drug 3']
    drug4_total_package_cost, drug4_total_consulting_charges, drug4_total_oct_charges, drug4_total_travel_food_cost, drug4_total_opportunity_cost_lost, drug4_total_cost_per_patient = drug_costs['Drug 4']
    drug5_total_package_cost, drug5_total_consulting_charges, drug5_total_oct_charges, drug5_total_travel_food_cost, drug5_total_opportunity_cost_lost, drug5_total_cost_per_patient = drug_costs['Drug 5']

    bar_graph_data = pd.DataFrame(columns=["Total Package Cost","Consulting Charges","OCT Charges","Travel and Food Costs","Total Opportunity Cost Lost","Total Cost/Patient"])
    bar_graph_data.loc[0] = [drug1_total_package_cost, drug1_total_consulting_charges, drug1_total_oct_charges, drug1_total_travel_food_cost, drug1_total_opportunity_cost_lost, drug1_total_cost_per_patient]
    bar_graph_data.loc[1] = [drug2_total_package_cost, drug2_total_consulting_charges, drug2_total_oct_charges, drug2_total_travel_food_cost, drug2_total_opportunity_cost_lost, drug2_total_cost_per_patient]
    bar_graph_data.loc[2] = [drug3_total_package_cost, drug3_total_consulting_charges, drug3_total_oct_charges, drug3_total_travel_food_cost, drug3_total_opportunity_cost_lost, drug3_total_cost_per_patient]
    bar_graph_data.loc[3] = [drug4_total_package_cost, drug4_total_consulting_charges, drug4_total_oct_charges, drug4_total_travel_food_cost, drug4_total_opportunity_cost_lost, drug4_total_cost_per_patient]
    bar_graph_data.loc[4] = [drug5_total_package_cost, drug5_total_consulting_charges, drug5_total_oct_charges, drug5_total_travel_food_cost, drug5_total_opportunity_cost_lost, drug5_total_cost_per_patient]
    
    # ------------------------------------------ Total Package Cost ------------------------------------------
    
    Total_Package_Cost_data = pd.DataFrame(columns=["Total Package Cost", "Direct Costs", "Indirect Costs","Total Cost"])
    
    
    for i in range(len(bar_graph_data)):
        val = bar_graph_data.iloc[i]
        Total_Package_Cost_value = val["Total Package Cost"]
        Direct_Costs = val["Consulting Charges"] + val["OCT Charges"]
        Indirect_Costs = val["Travel and Food Costs"] + val["Total Opportunity Cost Lost"]
        total_costs = Total_Package_Cost_value + Direct_Costs + Indirect_Costs
        Total_Package_Cost_data.loc[i] = [Total_Package_Cost_value, Direct_Costs, Indirect_Costs, total_costs]

    # ------------------------------------------ Cumulative Costs Comparison ------------------------------------------
    
    cumulative_predefined_drug1_perlabel_dosage_y1=6
    cumulative_predefined_drug2_perlabel_dosage_y1=8
    cumulative_predefined_drug3_perlabel_dosage_y1=8
    cumulative_predefined_drug4_perlabel_dosage_y1=12
    cumulative_predefined_drug5_perlabel_dosage_y1=12

    dist_y1 = {"Drug 1": cumulative_predefined_drug1_perlabel_dosage_y1, "Drug 2": cumulative_predefined_drug2_perlabel_dosage_y1, "Drug 3": cumulative_predefined_drug3_perlabel_dosage_y1, "Drug 4": cumulative_predefined_drug4_perlabel_dosage_y1, "Drug 5": cumulative_predefined_drug5_perlabel_dosage_y1}
    
    cumulative_predefined_drug1_perlabel_dosage_y2345=3
    cumulative_predefined_drug2_perlabel_dosage_y2345=6
    cumulative_predefined_drug3_perlabel_dosage_y2345=4
    cumulative_predefined_drug4_perlabel_dosage_y2345=12
    cumulative_predefined_drug5_perlabel_dosage_y2345=12
    
    dist_y2345 = {"Drug 1": cumulative_predefined_drug1_perlabel_dosage_y2345, "Drug 2": cumulative_predefined_drug2_perlabel_dosage_y2345, "Drug 3": cumulative_predefined_drug3_perlabel_dosage_y2345, "Drug 4": cumulative_predefined_drug4_perlabel_dosage_y2345, "Drug 5": cumulative_predefined_drug5_perlabel_dosage_y2345}
    
    dist_cost_per_vial = {"Drug 1": drug1_cost_per_vial, "Drug 2": drug2_cost_per_vial, "Drug 3": drug3_cost_per_vial, "Drug 4": drug4_cost_per_vial, "Drug 5": drug5_cost_per_vial}
    dist_dosage = {"Drug 1": drug1_dosage, "Drug 2": drug2_dosage, "Drug 3": drug3_dosage, "Drug 4": drug4_dosage, "Drug 5": drug5_dosage}
    
    def calculate_cumulative_costs( Time_Horizon_value, cumulative_predefined_value_drug_num,cumulative_predefined_value_drug_num_2345,drug_cost_per_vial_value,drug_dosage_value):
        dist_all = {}
        indirect_cost = 0
        direct_cost = 0
        total_package_cost = 0
        
        for i in range(0,int(Time_Horizon_value)):
            
            if clinical_status=="Per Label":
                
                
                if i == 0 : 
                    
                    cumulative_direct_cost_y1=(consulting_charges*cumulative_predefined_value_drug_num)+(consulting_charges*(cumulative_predefined_value_drug_num//2))+(oct_cost*cumulative_predefined_value_drug_num)+(oct_cost*(cumulative_predefined_value_drug_num//2))
            
                    cumulative_indirect_cost_y1=((travel_cost+miscellaneous_cost+food_cost)*cumulative_predefined_value_drug_num)+((travel_cost+miscellaneous_cost+food_cost)*(cumulative_predefined_value_drug_num//2))+(patient_lost_opportunity_cost*cumulative_predefined_value_drug_num)+(patient_lost_opportunity_cost*(cumulative_predefined_value_drug_num//2))+(caregiver_lost_opportunity_cost*cumulative_predefined_value_drug_num)+(caregiver_lost_opportunity_cost*(cumulative_predefined_value_drug_num//2))

                    cumulative_total_package_cost_y1=(drug_cost_per_vial_value+procedure_cost)*cumulative_predefined_value_drug_num
                    
                if i == 1 or i == 2 or i == 3 or i == 4:
                    
                    cumulative_direct_cost_y1=int(((consulting_charges*cumulative_predefined_value_drug_num_2345)+(consulting_charges*(cumulative_predefined_value_drug_num_2345/2))+(oct_cost*cumulative_predefined_value_drug_num_2345)+(oct_cost*(cumulative_predefined_value_drug_num_2345/2))))

                    cumulative_indirect_cost_y1=int((((travel_cost+miscellaneous_cost+food_cost)*cumulative_predefined_value_drug_num_2345)+((travel_cost+miscellaneous_cost+food_cost)*(cumulative_predefined_value_drug_num_2345/2))+(patient_lost_opportunity_cost*cumulative_predefined_value_drug_num_2345)+(patient_lost_opportunity_cost*(cumulative_predefined_value_drug_num_2345/2))+(caregiver_lost_opportunity_cost*cumulative_predefined_value_drug_num_2345)+(caregiver_lost_opportunity_cost*(cumulative_predefined_value_drug_num_2345/2))))

                    cumulative_total_package_cost_y1=(drug_cost_per_vial_value+procedure_cost)*cumulative_predefined_value_drug_num_2345
                
            
            if  clinical_status =="RWE":
                
                if i == 0 : 
                    
                    cumulative_direct_cost_y1=int((consulting_charges*drug_dosage_value)+(consulting_charges*(drug_dosage_value/2))+(oct_cost*drug_dosage_value)+(oct_cost*(drug_dosage_value/2)))
                    cumulative_indirect_cost_y1=int(((travel_cost+miscellaneous_cost+food_cost)*drug_dosage_value)+((travel_cost+miscellaneous_cost+food_cost)*(drug_dosage_value/2))+(patient_lost_opportunity_cost*drug_dosage_value)+(caregiver_lost_opportunity_cost*(drug_dosage_value/2)))   
                    cumulative_total_package_cost_y1=(drug_cost_per_vial_value+procedure_cost)*cumulative_predefined_value_drug_num
                
                if i == 1 or i == 2 or i == 3 or i == 4:
                    
                    cumulative_direct_cost_y1=int(((consulting_charges*drug_dosage_value)+(consulting_charges*(drug_dosage_value/2))+(oct_cost*drug_dosage_value)+(oct_cost*(drug_dosage_value/2))))
                    cumulative_indirect_cost_y1=int(((travel_cost+miscellaneous_cost+food_cost)*drug_dosage_value)+((travel_cost+miscellaneous_cost+food_cost)*(drug_dosage_value/2))+(patient_lost_opportunity_cost*drug_dosage_value)+(caregiver_lost_opportunity_cost*(drug_dosage_value/2)))   
                    cumulative_total_package_cost_y1=(drug_cost_per_vial_value+procedure_cost)*cumulative_predefined_value_drug_num_2345

            
            indirect_cost += cumulative_indirect_cost_y1
            direct_cost += cumulative_direct_cost_y1
            total_package_cost += cumulative_total_package_cost_y1
            
            dist_all[i] = [indirect_cost, direct_cost, total_package_cost]  
            
        # print(dist_all)
        return dist_all
    
        
    d1 = calculate_cumulative_costs( time_horizon, dist_y1[First_Drug],dist_y2345[First_Drug],dist_cost_per_vial[First_Drug],dist_dosage[First_Drug])
    d2 = calculate_cumulative_costs( time_horizon,dist_y1[Second_Drug],dist_y2345[Second_Drug],dist_cost_per_vial[Second_Drug],dist_dosage[Second_Drug])
    
    bar_graph_data = [ {"data": list(j.values()) } for i,j in bar_graph_data.to_dict().items() ]
    dir_indir_total_cost = {0:"Direct Costs",1:"Indirect Costs",2:"Package Cost"}
    Total_Package_Cost_data = [ {"data":[ i for ids,i in enumerate(list(i.values())) if ids != 3 ] } for i in Total_Package_Cost_data.to_dict(orient="records")]
    
    return {"drug_dosages_side_bar_data" : drug_dosages_side_bar_data,
            "bar_gragh_data": bar_graph_data,
            "Total_Package_Cost": Total_Package_Cost_data,
            "First_Drug_data" : d1,
            "Second_Drug_data" : d2}
            
