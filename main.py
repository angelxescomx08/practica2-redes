import os
import time
import sys

import rrdtool

from getSNMP import consultaSNMP
from CreateRRD import crearRRD  
from updateRRD import actualizarRRD

def generarReporte(comunidad:str,ip:str,puerto:int,entrada:str,salida:str,fechaInicio:str,fechaFin:str):
    reporte = open('reporte.txt','w')

    #nombre del agente
    nombreSistema = consultaSNMP(comunidad,ip,'1.3.6.1.2.1.1.5.0',puerto)
    reporte.write('device: {sistema} \n'.format(sistema=nombreSistema))

    #descripcion
    descripcion = consultaSNMP(comunidad,ip,'1.3.6.1.2.1.1.1.0',puerto)
    reporte.write('description: {descripcion} \n'.format(descripcion=descripcion))

    #fecha
    reporte.write('date: {fecha} \n'.format(fecha=fechaInicio))

    #protocolo
    reporte.write('defaultProtocol: radius \n\n')

    #r fecha
    reporte.write('rdate: {fecha} \n'.format(fecha=fechaFin))

    #ip
    reporte.write('#NAS-IP-Address \n')
    reporte.write('{ip} \n'.format(ip=ip))

    #puerto
    reporte.write('#NAS-Port \n')
    reporte.write('{puerto} \n'.format(puerto=puerto))

    #usuario
    usuario = consultaSNMP(comunidad,ip,'1.3.6.1.2.1.1.4.0',puerto)
    reporte.write('#User-Name \n')
    reporte.write('{usuario} \n'.format(usuario=usuario))

    #octetos de entrada
    reporte.write('#Acct-Input-Octets \n')
    reporte.write('{entrada} \n'.format(entrada=entrada))

    #octetos de salida
    reporte.write('#Acct-Output-Octets \n')
    reporte.write('{salida} \n'.format(salida=salida))

    reporte.close()

def menu():
    ip = '192.168.0.2'
    comunidad = 'comunidadASR'
    puerto = 161
    crearRRD('base_datos')
    print("Ingresa la fecha y hora de inicio (DD-MM-AAAA HH:MM)")
    inicio = input()
    inicioFormateado =time.mktime(time.strptime(inicio,"%d-%m-%Y %H:%M"))
    print("Ingresa la fecha y hora de termino (DD-MM-AAAA HH:MM)")
    fin = input()
    finFormateado =time.mktime(time.strptime(fin,"%d-%m-%Y %H:%M"))
    actualizarRRD(ip,comunidad,puerto,inicio,fin)
    last_update = rrdtool.lastupdate('base_datos.rrd')
    tiempo_inicial = int(last_update['date'].timestamp())-120
    resultado = rrdtool.fetch('base_datos.rrd','-s '+str(tiempo_inicial),'LAST')
    entrada = ''
    salida = ''
    for row in resultado[2]:
        print(row)
        entrada = row[0]
        salida = row[1]
        break
    generarReporte(comunidad,ip,puerto,entrada,salida,inicio,fin)

menu()