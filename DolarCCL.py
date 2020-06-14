import requests
import json
import pandas as pd
url = 'https://api.invertironline.com/token'
usuario = 'Reemplazar por usuario'                         #Insertar usuario obtenido en IOL
password = 'Reemplazar por password'                       #Password de IOL

data = { 
    'username' : usuario,
    'password': password,
    'grant_type': 'password'    
}  

r = requests.post(url=url,data=data)
print(r)
token = json.loads(r.text)
bearer = token['access_token']
refresh = token['refresh_token']



datos4principales = [['GGAL','GGAL',10,'Grupo Financiero Galicia'],['YPFD','YPF',1,'YPF'],
                     ['PAMP','PAM',25,'Pampa Energía'],['BMA','BMA',10,'Banco Macro']]
datos = [['GGAL','GGAL',10,'Grupo Financiero Galicia'],['YPFD','YPF',1,'YPF'],
         ['PAMP','PAM',25,'Pampa Energía'],['BMA','BMA',10,'Banco Macro'],
         ['BBAR','BBAR',3,'BBVA Banco Frances'],
         ['CEPU','CEPU',10,'Central Puerto'],['CRES','CRESY',10,'Cresud'],
         ['EDN','EDN',20,'Edenor'],['TGSU2','TGS',5,'Transp. de Gas del Sur'],
         ['PAMP','PAM',25,'Pampa Energia'],['SUPV','SUPV',5,'Supervielle'],
         ['TECO2','TEO',5,'Telecom Argentina'],['IRSA','IRS',10,'Irsa']]


def iniciar():
    #Calcular Promedio 4 acciones con mas volumen: GGAL, YPF, PAMP, BMA
    promedio = calcPromedio()    
    #Mostrar Segun cada accion - Debe traer un diccionario con el nombre de la accion y el precio de su CCL
    cclTodas = cclAcciones()
    cclTodas['PROMEDIO 4 > VOL'] = promedio
    dataFrame = crearDf(cclTodas)
    return dataFrame
    

def calcPromedio():
    suma = 0
    n = 0
    for accion in datos4principales:
        try:
            suma = suma + calcularCCL(accion[0],accion[1],accion[2])
            n = n + 1             
        except:
            print("No se pudo calculo el ccl de " + accion[3])
    return suma / n

def cclAcciones():
    data = {}
    for accion in datos:
        try:
            data[accion[3]] = calcularCCL(accion[0],accion[1],accion[2])            
        except:
            print('No se pudo calcular el CCL de ' + accion[3])    
    return data

def crearDf(dicc):    
    df = pd.DataFrame([[key, dicc[key]] for key in dicc.keys()], columns=['Accion', 'CCL'])
    return df


def consultaCotizacion(simbolo,mercado):  #sin puntas
    cotizacion = requests.get(url="https://api.invertironline.com/api/v2/{}/Titulos/{}/Cotizacion".format(mercado,simbolo), headers={'Authorization':'Bearer '+bearer})
    simb = json.loads(cotizacion.text)    
    puntas = simb["ultimoPrecio"]
    return puntas

def calcularCCL(simboloLocal , simboloExt , factorConversion):
    ccl = tipoDeCambioComprador = consultaCotizacion(simboloLocal,'bCBA') / consultaCotizacion(simboloExt,'nYSE') * factorConversion
    return ccl

iniciar()
        
    
                    
        
    
        
