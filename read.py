import os
import time
import inspect
import configparser
from datetime import datetime
from PyViCare.PyViCare import PyViCare
from PyViCare.PyViCareHeatPump import HeatPump, Compressor
from PyViCare.PyViCareDeviceConfig import PyViCareDeviceConfig
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError
from PyViCare.PyViCareHeatingDevice import HeatingCircuit, HeatingDeviceWithComponent

"""
Install and run:

$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ python read.py

Call this every minute from crontab.

The output are csv-files by date (each day a new file).

"""
config = configparser.ConfigParser()
config.read("config.ini")

client_id = config["credentials"]["client_id"]
email = config["credentials"]["email"]
password = config["credentials"]["password"]


file_name = "heatpump"

#
# HeatPump related information
# 

def get_compressor_KompressorStatus(compressor : Compressor) -> str:
    if compressor.getActive():
        return "1"
    else: 
        return "0"

def get_compressor_KompressorPhase(compressor: Compressor) -> str:
    return compressor.getPhase()

def get_heatpump_AussenTemperatur(hp : HeatPump) -> str: 
    return str(hp.getOutsideTemperature())

def get_heatpump_VolumenStrom(hp: HeatPump) -> str:
    return str(hp.getVolumetricFlowReturn())

def get_heatpump_WEVorlauf(hp: HeatPump) -> str: 
    return str(hp.service.getProperty("heating.boiler.sensors.temperature.commonSupply")["properties"]["value"]["value"])

def get_heatpump_WERücklauf(hp: HeatPump) -> str: 
    return str(hp.getReturnTemperature())

def get_heatpump_VerbrauchHeute(hp: HeatPump) -> str: 
    return str(hp.getPowerConsumptionToday())

# Not Supported: getReturnTempPrimaryCircuit and getReturnTempSecondaryCircuit: 

# This seems to be in the Heatpump (on order of outside temp)
def get_heatpump_SupplyTempPrimaryCircuit(hp: HeatPump) -> str: 
    return str(hp.getSupplyTemperaturePrimaryCircuit())

# Buffer related information

def get_heatpump_SpeicherTemp(hp: HeatPump) -> str:
    return str(hp.getBufferMainTemperature())

# Not Supported
#
# def get_heatpump_BufferTopTemp(device: HeatPump) -> str:
#     return str(device.getBufferTopTemperature())

# Heat circuit related information 

# Heatcurve related infos

def get_circuit_HeizKurveNeigung(circ: HeatingCircuit) -> str: 
    return str(circ.getHeatingCurveSlope())

def get_circuit_HeizkurveNiveau(circ: HeatingCircuit) -> str:
    return str(circ.getHeatingCurveShift())

def get_circuit_Frostschutz(circ: HeatingCircuit) -> str: 
    if circ.getFrostProtectionActive():
        return "1"
    else:
        return "0"

def get_circuit_HKPumpeAktiv(circ: HeatingCircuit) -> str: 
    if circ.getCirculationPumpActive():
        return "1"
    else:
        return "0"

def get_circuit_HKSupplyTemp(circ: HeatingCircuit) -> str: 
    return str(circ.getSupplyTemperature())

# The Target Supply Temperature is calculated from other paramters, NOT READ FROM DEVICE
# ()
# def get_circuit_HKTargetSupplyTemp(circ: HeatingCircuit) -> str: 
#     return str(circ.getTargetSupplyTemperature())

def get_circuit_HKWunschTemp(circ: HeatingCircuit) -> str: 
    return str(circ.getCurrentDesiredTemperature())

# Handle NotSupportedFeatureError Exception

def try_func(name, func, device) -> str: 
    try: 
        return func(device)
    except PyViCareNotSupportedFeatureError:
        return "err in " + name

if __name__ == "__main__":
    file_name = file_name + "-" + datetime.now().strftime("%Y-%m-%d") + ".csv"


    vicare = PyViCare()
    vicare.initWithCredentials(email, password, client_id, "token.save")

    # Initialize the respective devices, we would like to query: 
    device: PyViCareDeviceConfig = vicare.devices[1]
    hp: HeatPump = device.asHeatPump()
    comp: Compressor = hp.compressors[0] # A compressor is a HeatingDeviceWithComponent
    circ: HeatingCircuit = hp.circuits[0]

    #
    # Which values to read out
    # 

    # Get all functions in the current module
    current_module = inspect.getmodule(inspect.currentframe())
    functions = inspect.getmembers(current_module, inspect.isfunction)
    
    # Filter functions starting with "get"
    get_functions = [(name, func) for name, func in functions if name.startswith("get")]

    # 
    # Read out values and store in CSV
    # 

    colnames = ["Timestamp"]
    for name, func in get_functions: 
        _, device, colname = name.split("_")
        colnames.append(colname)

    # Create file with header line if it does not exist yet.
    if not os.path.exists(file_name):
        with open(file_name, mode="w") as output:
            output.write(",".join(colnames))
            output.write("\n")

    # Append reads
    try: 
        print(",".join(colnames))
        results = [datetime.now().isoformat()]
        for name, func in get_functions:
            _, device, colname = name.split("_")
            if device == "heatpump": 
                value = try_func(name, func,hp)
            elif device == "compressor":
                value = try_func(name, func, comp)
            elif device == "circuit":
                value = try_func(name, func, circ)
            else: 
                value = None
                print("unknown device")
            results.append(value)

        print(",".join(results))

        with open(file_name, mode="a") as output:
            output.write(",".join(results))
            output.write("\n")

    except KeyboardInterrupt:
        print("Shutting down.")

