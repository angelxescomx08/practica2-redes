from pysnmp.hlapi import *

def consultaSNMP(comunidad,host,oid,puerto):
    resultado = ''
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(comunidad),
               UdpTransportTarget((host, puerto)),
               ContextData(),
               ObjectType(ObjectIdentity(oid))))

    if errorIndication:
        #print(errorIndication)
        return 'timeout'
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            resultado = ''
            varB= (' = '.join([x.prettyPrint() for x in varBind]))
            #print(varB)
            resultado=  varB.split()[2]
            if((len(varB.split("Software")) > 1) | (resultado == 'Linux')):
                resultado = varB.split("=")[1]
            
            
    return resultado