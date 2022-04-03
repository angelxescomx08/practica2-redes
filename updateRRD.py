import time
import rrdtool
from getSNMP import consultaSNMP

def actualizarRRD(ip:str, comunidad:str,puerto:int,inicio:str,fin:str):
    horasInicio = int(inicio.strip('\n').split(" ")[1].split(":")[0])
    minutosInicio = int(inicio.strip('\n').split(" ")[1].split(":")[1])

    horasFin= int(fin.strip('\n').split(" ")[1].split(":")[0])
    minutosFin= int(fin.strip('\n').split(" ")[1].split(":")[1])

    horas = horasFin - horasInicio
    minutos = minutosFin - minutosInicio

    tiempo = (horas*60*60) + (minutos*60)

    tiempoInicio = time.time()
    while 1:
        inOctets = consultaSNMP(comunidad, ip,'1.3.6.1.2.1.6.10.0',puerto)
        outOctets = consultaSNMP(comunidad, ip,'1.3.6.1.2.1.6.11.0',puerto)

        valor = "N:" + str(inOctets) + ":" + str(outOctets)
        print(valor)
        rrdtool.update('base_datos.rrd', valor)
        # rrdtool.dump('practica1.rrd','practica1.xml')
        time.sleep(1)
        tiempoTranscurrido = time.time() - tiempoInicio
        if(tiempoTranscurrido >= tiempo):
            break

    # if ret:
    #    print (rrdtool.error())
    #    time.sleep(300)
