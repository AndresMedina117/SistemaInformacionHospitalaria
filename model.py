import os
import csv
import json
from unidecode import unidecode
import pymongo

hce = pymongo.MongoClient("mongodb+srv://andros2017unisinu:andros172129@cluster0.dkrxuwh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = hce.patients

def findAll():
    result = [i['id'] for i in db.patients.find()]
    return result

def infoJson2HL7(info_paciente,nombreArchivo):
    hl7_msg = []

    # Segmento MSH
    msh_segment = f"MSH|^~\&|{info_paciente['equipo']}|{info_paciente['serial']}|{info_paciente['ips']}|{info_paciente['modelo']}|{info_paciente['fecha']}||ORU^R01|{info_paciente['id']}|P|2.4"
    hl7_msg.append(msh_segment)

    # Segmento PID
    pid_segment = f"PID||{info_paciente['id']}|||{info_paciente['nombre']}^{info_paciente['apellido']}||{info_paciente['edad']}|{info_paciente['sexo']}|||||||||||||||||||"
    hl7_msg.append(pid_segment)

    # Segmento OBX (resultados del examen)
    examen = info_paciente['examen']
    for clave, valor in examen.items():
        obx_segment = f"OBX|1|NM|{clave}||{valor}||||||F"
        hl7_msg.append(obx_segment)

    # Segmento PV1 (Información de la visita)
    pv1_segment = f"PV1|1|I|{info_paciente['ingreso']}||||||{info_paciente['médico']}|{info_paciente['especialidad']}||||||||"
    hl7_msg.append(pv1_segment)

    # Segmento DG1 (Diagnóstico)
    dg1_segment = f"DG1|1|||{info_paciente['dx']}"
    hl7_msg.append(dg1_segment)

    # Segmento DG1 (Comorbilidades)
    comorbilidades = info_paciente.get('Comorbilidades', [])
    for idx, comorbilidad in enumerate(comorbilidades, start=2):
        dg1_segment = f"DG1|{idx}|||{comorbilidad}"
        hl7_msg.append(dg1_segment)

    # Convertir la lista de segmentos a una cadena de texto
    hl7_str = '\n'.join(hl7_msg)

    #Guardar el mensaje en un archivo de texto
    directory="data"
    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = os.path.join(directory, nombreArchivo+'.txt')
    if os.path.exists(filename):
        creado2= "Ya existe un archivo con ese nombre"

    elif not os.path.exists(filename):
        with open(filename, 'w') as file:
            file.write(hl7_str)
        creado2= "HL7 creado correctamente"

    return [hl7_str,creado2]

def infoCSV2HL7(info_paciente,nombreArchivo):#se le ingresa como argumentos el diccionario y el nombre del archivo txt hl7, retorna una lista, donde el primer elemento es el str hl7 y el segundo es un str que indica si se creo el nuevo txt con el hl7
    hl7_msg = []

    # Segmento MSH
    msh_segment = f"MSH|^~\&|{info_paciente['equipo']}|{info_paciente['serial']}|{info_paciente['ips']}|{info_paciente['modelo']}|{info_paciente['fecha']}||ORU^R01|{info_paciente['id']}|P|2.4"
    hl7_msg.append(msh_segment)

    # Segmento PID
    pid_segment = f"PID||{info_paciente['id']}|||{info_paciente['nombre']}^{info_paciente['apellido']}||{info_paciente['edad']}|{info_paciente['sexo']}|||||||||||||||||||"
    hl7_msg.append(pid_segment)

    # Segmento OBX (resultados de los procedimientos)
    obx_segment_tp = f"OBX|1|NM|TP||{info_paciente['proc_tp']}||||||F"
    obx_segment_ptt = f"OBX|2|NM|PTT||{info_paciente['proc_ptt']}||||||F"
    obx_segment_fib = f"OBX|3|NM|FIB||{info_paciente['proc_fib']}||||||F"
    hl7_msg.extend([obx_segment_tp, obx_segment_ptt, obx_segment_fib])

    # Segmento PV1 (Información de la visita)
    pv1_segment = f"PV1|1|I|{info_paciente['ingreso']}||||||{info_paciente['médico']}|{info_paciente['especialidad']}||||||||"
    hl7_msg.append(pv1_segment)

    # Segmento DG1 (Diagnóstico principal)
    dg1_segment_ppal = f"DG1|1|||{info_paciente['dx_ppal']}"
    hl7_msg.append(dg1_segment_ppal)

    #Segmento DG2 (Diagnostico secundario)
    dg2_segment_ppal = f"DG1|2|||{info_paciente['dx2']}"
    hl7_msg.append(dg2_segment_ppal)

    #Segmento DG3 (Diagnostico terciario)
    dg3_segment_ppal = f"DG1|3|||{info_paciente['dx3']}"
    hl7_msg.append(dg3_segment_ppal)

    #Segmento DG4 (Diagnostico cuaternario)
    dg4_segment_ppal = f"DG1|4|||{info_paciente['dx4']}"
    hl7_msg.append(dg4_segment_ppal)

    #Segmento DG5 (Diagnostico numero 5)
    dg5_segment_ppal = f"DG1|5|||{info_paciente['dx5']}"
    hl7_msg.append(dg5_segment_ppal)

    # Convertir la lista de segmentos a una cadena de texto
    hl7_str = '\n'.join(hl7_msg)

    #Guardar el mensaje en un archivo de texto
    directory="data"
    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = os.path.join(directory, nombreArchivo+'.txt')
    if os.path.exists(filename):
        creado2= "Ya existe un archivo con ese nombre"

    elif not os.path.exists(filename):
        with open(filename, 'w') as file:
            file.write(hl7_str)
        creado2= "HL7 creado correctamente"

    return [hl7_str,creado2]


def find(id):
    result = [i for i in db.patients.find({"id": {"$eq": id}})]
    if not result:
        return "No se ha encontrado el ID"
    result=result[0]
    if 'proc_tp' in result:
        C=infoCSV2HL7(result,id)
    else:
        C=infoJson2HL7(result,id)
    return result

def detectar_delimitador(archivo):
    with open(archivo, 'r', encoding='utf-8') as f:
        dialecto = csv.Sniffer().sniff(f.read(1024))  # Analizar solo una porción del archivo
        return dialecto.delimiter
    
def extraer_info_csv(nombre_archivo):
    pacientes = []
    # Ruta de la carpeta
    info_pacientes_csv = []
    ruta = nombre_archivo
    delimitador = detectar_delimitador(ruta)
    with open(ruta, encoding='utf-8') as file:
        content = csv.reader(file , delimiter=delimitador)
        for row in content:
            info_pacientes_csv.append(row)

    # Eliminar el BOM si está presente en la primera fila
    if info_pacientes_csv and info_pacientes_csv[0][0].startswith('\ufeff'):
        info_pacientes_csv[0][0] = info_pacientes_csv[0][0][1:]

    for pacient in info_pacientes_csv[1:]:
        paciente = {}
        for i in range(len(pacient)):
            paciente[info_pacientes_csv[0][i].strip()] = unidecode(pacient[i])
        pacientes.append(paciente)

    return pacientes

#AHORA PARA LA INFO DE LOS JASON
def extraer_info_json(nombre_archivo):
    # Ruta de la carpeta
    ruta = nombre_archivo
    with open(ruta, encoding='utf-8') as file:
        data = json.load(file)
        # Decodificar caracteres especiales utilizando unidecode
        data = [unidecode(item) if isinstance(item, str) else item for item in data]
    return data

def extraer_info_serial(nombre_archivo):
    # Ruta de la carpeta
    ruta =  nombre_archivo
    with open(ruta, encoding='utf8') as file:
        text = file.readlines()
    text1 = text[4].split('|')
    id, edad, nombre, apellidos, genero = text1[2],text1[4].split('^')[3],text1[12],text1[13],text1[27]
    fechaHora = text[0].split('|')[13]
    genero = genero.split('\n')[0]
    if genero == "M":
        genero = "Masculino"
    elif genero == "F":
        genero = "Femenino"
    linesOfData = [i.split('|') for i in text[6:] if fechaHora in i.split('|')]
    dic_f = {}
    data = [['{}-{}'.format(i[2].split('^')[3], i[2].split('^')[4]), i[3]] for i in linesOfData]
    dic_final = {'id': id, 'edad': edad, 'nombre': nombre, 'apellidos': apellidos, 'genero': genero}
    for j in data:
        dic_f[j[0]] = j[1]
    dic_final = {'id': id, 'edad': edad, 'nombre': nombre, 'apellidos': apellidos, 'genero': genero, 'data':dic_f}

    return [dic_final]

def create(archivos):
    # Obtener la lista de archivos en la carpeta
    error=''
    # Ruta de la carpeta
    # Clasificar los archivos por tipo
    for archivo in archivos:
        nombre, extension = os.path.splitext(archivo)
        if extension == '.txt':
            info = extraer_info_serial(archivo)
            for paciente in info:
                #print(paciente)
                if db.patients.find_one({"id" : {"$eq":paciente['id']}}) is None:
                    db.patients.insert_one(paciente)
                else:
                    error=error+'\n Ya hay un paciente con la id: '+paciente['id']
        elif extension == '.json':
            info=extraer_info_json(archivo)
            for paciente in info:
                #print(paciente)
                if db.patients.find_one({"id" : {"$eq":paciente['id']}}) is None:
                    db.patients.insert_one(paciente)
                else:
                    error=error+'\n Ya hay un paciente con la id: '+paciente['id']
        elif extension == '.csv':
            info=extraer_info_csv(archivo)
            for paciente in info:
                #print(paciente)
                if db.patients.find_one({"id" : {"$eq":paciente['id']}}) is None:
                    db.patients.insert_one(paciente)
                else:
                    error=error+' \n Ya hay un paciente con la id: '+paciente['id']
    return error

def eliminador(id):
    resultado = db.patients.delete_one({"id": id})
    if resultado.deleted_count == 1:
        return f"Se eliminó correctamente el documento con ID {id}."
    else:
        return f"No se encontró ningún documento con ID {id} para eliminar."
    
def updateDB(id, nombre, apellidos, edad, medico, ips, diagnostico, fecha, comorbilidades, examenes):
    update_data = {
        "$set": {
            "nombre": nombre,
            "apellido": apellidos,
            "edad": edad,
            "médico": medico,
            "ips": ips,
            "dx": diagnostico,
            "fecha": fecha,
            "Comorbilidades": comorbilidades,
            "examen": examenes
        }
    }
    result= db.patients.update_one({"id": id}, update_data)
    return result