from lecroydso.errors import DSOConnectionError, DSOIOError
from lecroydso  import ActiveDSO, LeCroyDSO
import pyvisa as visa
import pylab as pylab
import matplotlib.pyplot as plt

connection_string = 'COM7:19200,8,N,1'  #Checker dans le device manager du pc (COM? et baudrate)
sara = '1000000000' #Taux d'échantillonnage 1GS/s (vérifier avant mesures)

def vicpactivedso():
    try:
        print('Trying to make a connection to : COM7:19200,8,N,1')
        dso = LeCroyDSO(ActiveDSO('COM7:19200,8,N,1'))
        print(dso.query('*IDN?'))
        dso.set_default_state()
        
        # send VBS style command
        dso.write_vbs('app.Acquisition.C1.VerScale=0.01')
        
        # query V/DIV
        response = dso.query('C1:VDIV?')
        print("V/DIV : ",response)

        # query it VBS style
        vbs_response = dso.query_vbs('app.Acquisition.C1.VerScale')
        print(vbs_response)

        #début acquisition trace
        
        dso.write("chdr off")
        vdiv = response
        ofst = dso.query("c1:ofst?")
        print("Offset en CH1 : ",ofst)
        tdiv = 0.2e-3 ##Paramétrer la période en fonction du réglage de l'oscilloscope
        print("t/DIV = ",tdiv)
        sara = '1000000000' ## Fréquence d'échantillonnage, ici 1GS/s.
        print("sara = ",sara)
        sara_unit = {'G':1E9,'M':1E6,'k':1E3}
        for unit in sara_unit.keys():
            if sara.find(unit)!=-1:
             sara = sara.split(unit)
             sara = float(sara[0])*sara_unit[unit]
             break
        sara = float(sara)
        dso.timeout = 30000 #default value is 2000(2s) #valeur d'origine : 30000
        dso.chunk_size = 20*1024*1024 #default value is 20*1024(20k bytes)
        wf = dso.write("c1:wf? dat2")
        print("WF data : ",wf)
        #data = 50
        volt_value.append(data)
        time_value = []
        for idx in range(0,len(volt_value)):
             volt_value[idx] = volt_value[idx]/25*float(vdiv)-float(ofst)
             time_data = -(float(tdiv)*14/2)+idx*(1/sara)
             time_value.append(time_data)
        plt.figure(figsize=(9,5)) #valeur d'origine : 7,5
        plt.plot(time_value,volt_value,markersize=2,label=("Mode XY")
        print(time_value)
        print(volt_value)
        plt.legend()
        plt.grid()
        plt.show()


    except DSOConnectionError as e:
        print('ERROR: Unable to make a connection to ', connection_string)
        print(e.message)
        exit(-1)

    except DSOIOError:
        print('ERROR: Failed to communicate to the instrument')
        exit(-1)


if __name__ == '__main__':
    vicpactivedso()
