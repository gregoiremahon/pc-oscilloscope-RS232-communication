from lecroydso.errors import DSOConnectionError, DSOIOError
from lecroydso  import ActiveDSO, LeCroyDSO
import pyvisa as visa
import pylab as pylab
import matplotlib.pyplot as plt
connection_string = 'COM4:19200,8,N,1'


def vicpactivedso():
    try:
        
        print('Trying to make a connection to ', connection_string)
        dso = LeCroyDSO(ActiveDSO(connection_string))
        print(dso.query('*IDN?'))

        dso.set_default_state()
       

        # send VBS style command
        dso.write_vbs('app.Acquisition.C1.VerScale=0.01')

        # query the value
        response = dso.query('C1:VDIV?').replace("E","e")
        print(response)

        # query it VBS style
        vbs_response = dso.query_vbs('app.Acquisition.C1.VerScale')
       

    except DSOConnectionError as e:
        print('ERROR: Unable to make a connection to ', connection_string)
        print(e.message)
        exit(-1)

    except DSOIOError:
        print('ERROR: Failed to communicate to the instrument')
        exit(-1)



    dso.write("chdr off")
    vdiv = dso.query("c1:vdiv?").replace("E","e")
    print(vdiv)
    dso.get_waveform('C1')
    ofst = dso.query("c1:ofst?").replace("E","e")
    print(ofst)
    tdiv = dso.query("tdiv?")
    #sara = dso.query("sara?")
    sara ="250000"
    sara_unit = {'G':1e9,'M':1e6,'k':1e3}
    for unit in sara_unit.keys():
        if sara.find(unit)!=-1:
           sara = sara.split(unit)
           sara = float(sara[0])*sara_unit[unit]
        break
    sara = float(sara)
    dso.timeout = 30000 #default value is 2000(2s)
    dso.chunk_size = 20*1024*1024 #default value is 20*1024(20k bytes)
    dso.write("c1:wf? dat2")
    recv = list(dso._conn.read_raw(300))
    print(len(recv))
    recv.pop()
    recv.pop()
    volt_value = []
    for data in recv:
        if data > 127:
            data = data - 255
        else:
            pass
        volt_value.append(data)
        print("data",data)
    time_value = []
    for idx in range(0,len(volt_value)):
        volt_value[idx] = volt_value[idx]/25*float(vdiv)-float(ofst)
        time_data = -(float(tdiv)*14/2)+idx*(1/sara)
        time_value.append(time_data)
    plt.figure(figsize=(7,5))
    plt.plot(time_value,volt_value,markersize=2,label=u"Y-T")
    print(volt_value)
    print(time_value)
    plt.legend()
    plt.grid()
    plt.show()
    
if __name__=='__main__':
    vicpactivedso()
