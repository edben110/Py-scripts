import pandas as pd
import numpy as np
import zipfile
import os
import shutil
import re

CERTIFICADO_BASE = "20250528-1140264218-LUISESTEBANCASTILLOPEDROZA.docx"
ASISTENCIA_FILE = "lista.xlsx"
DATOS_FILE = "Proceso Inscripciones II Seminario Nacional de Ingenieria de Software (1).xls"

OUTPUT_DIR = "certificados_generados"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === FUNCIÓN REEMPLAZO DIRECTO EN XML (incluye cuadros de texto) ===
def reemplazar_en_docx(base_docx, salida_docx, nombre, cedula):
    import random
    import time
    
    # Crear carpeta temporal única para evitar conflictos
    temp_folder = f"temp_docx_{int(time.time() * 1000)}_{random.randint(1000, 9999)}"
    os.makedirs(temp_folder, exist_ok=True)

    # extraer docx como zip
    with zipfile.ZipFile(base_docx, "r") as zip_ref:
        zip_ref.extractall(temp_folder)

    # Valores base en la plantilla
    nombre_base_parte1 = "LUIS "
    nombre_base_parte2 = "ESTEBAN CASTILLO PEDROZA"
    cedula_base = "1140264218"
    
    # Convertir nombre a mayúsculas
    nombre_mayus = nombre.upper()
    
    archivos_modificados = []

    # Buscar y reemplazar en TODOS los archivos XML del documento
    word_folder = os.path.join(temp_folder, "word")
    
    # Procesar todos los archivos XML en la carpeta word/
    for root, dirs, files in os.walk(word_folder):
        for filename in files:
            if filename.endswith(".xml") or filename.endswith(".rels"):
                file_path = os.path.join(root, filename)
                
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        xml_content = f.read()
                    
                    # Guardar contenido original para comparar
                    original_content = xml_content
                    
                    # ESTRATEGIA 1: Reemplazar el patrón fragmentado específico detectado
                    # Patrón: <w:t>LUIS </w:t></w:r><w:r ...><w:t>ESTEBAN CASTILLO PEDROZA</w:t>
                    patron_especifico = r'(<w:t[^>]*>)LUIS\s*(</w:t></w:r><w:r[^>]*><w:rPr>[^<]*</w:rPr><w:t>)ESTEBAN\s+CASTILLO\s+PEDROZA(</w:t>)'
                    
                    def reemplazar_nombre_completo(match):
                        # Colocar todo el nombre en la primera parte y vaciar la segunda
                        return f'{match.group(1)}{nombre_mayus}{match.group(2)}{match.group(3)}'
                    
                    xml_content = re.sub(patron_especifico, reemplazar_nombre_completo, xml_content, flags=re.IGNORECASE)
                    
                    # ESTRATEGIA 2: Patrón más simple para el nombre fragmentado
                    xml_content = re.sub(
                        r'(<w:t[^>]*>)LUIS\s*(</w:t>)',
                        rf'\g<1>{nombre_mayus}\g<2>',
                        xml_content,
                        count=1
                    )
                    
                    # Después de poner el nombre completo, eliminar la segunda parte
                    xml_content = re.sub(
                        r'(<w:t[^>]*>)ESTEBAN\s+CASTILLO\s+PEDROZA(</w:t>)',
                        r'\g<1>\g<2>',
                        xml_content,
                        count=1
                    )
                    
                    # ESTRATEGIA 3: Reemplazar cédula fragmentada
                    # Patrón: <w:t>1140</w:t></w:r><w:r ...><w:t>264218</w:t>
                    patron_cedula = r'(<w:t[^>]*>)1140(</w:t></w:r><w:r[^>]*>[^<]*<w:rPr>[^<]*</w:rPr><w:t>)264218(</w:t>)'
                    
                    def reemplazar_cedula(match):
                        # Poner toda la cédula en la primera parte y vaciar la segunda
                        return f'{match.group(1)}{cedula}{match.group(2)}{match.group(3)}'
                    
                    xml_content = re.sub(patron_cedula, reemplazar_cedula, xml_content)
                    
                    # También reemplazar cada parte por separado
                    xml_content = re.sub(
                        r'(<w:t[^>]*>)1140(</w:t>)',
                        rf'\g<1>{cedula}\g<2>',
                        xml_content,
                        count=1
                    )
                    xml_content = re.sub(
                        r'(<w:t[^>]*>)264218(</w:t>)',
                        r'\g<1>\g<2>',
                        xml_content,
                        count=1
                    )
                    
                    # Solo escribir si hubo cambios
                    if xml_content != original_content:
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(xml_content)
                        archivos_modificados.append(filename)
                
                except Exception as e:
                    # Algunos archivos pueden no ser UTF-8, ignorar errores
                    pass
    
    if archivos_modificados:
        print(f"  ✓ Archivos modificados: {', '.join(set(archivos_modificados))}")
    else:
        print(f"  ⚠️  ADVERTENCIA: No se modificó ningún archivo XML")

    # Verificar si el archivo de salida existe y está bloqueado
    archivo_bloqueado = False
    if os.path.exists(salida_docx):
        try:
            # Intentar abrir el archivo para verificar si está bloqueado
            with open(salida_docx, 'a'):
                pass
            os.remove(salida_docx)
        except Exception as e:
            print(f"  ⚠️  Archivo bloqueado (probablemente abierto en Word): {os.path.basename(salida_docx)}")
            print(f"      Omitiendo este certificado. Cierra el archivo e intenta de nuevo.")
            archivo_bloqueado = True

    # Solo continuar si el archivo no está bloqueado
    if not archivo_bloqueado:
        try:
            # Usar nombre único para el archivo zip temporal
            zip_name = f"tmp_output_{int(time.time() * 1000)}"
            shutil.make_archive(zip_name, "zip", temp_folder)
            shutil.move(f"{zip_name}.zip", salida_docx)
            print(f"  ✅ Certificado generado exitosamente")
        except Exception as e:
            print(f"  ❌ Error al crear el archivo: {e}")
    
    # Siempre limpiar la carpeta temporal
    if os.path.exists(temp_folder):
        try:
            shutil.rmtree(temp_folder)
        except:
            pass


# === CARGAR EXCEL ===
asistencia = pd.read_excel(ASISTENCIA_FILE, header=None)
datos = pd.read_excel(DATOS_FILE, header=None)

col_asistencia = 0   # columna A
col_datos = 29        # columna AD

inscritos = datos.merge(asistencia, left_on=col_datos, right_on=col_asistencia, how="inner")

print(f"Total certificados a generar: {len(inscritos)}")

for _, row in inscritos.iterrows():

    # Manejar valores NaN convirtiéndolos a cadenas vacías
    primer_apellido = str(row[11]).strip() if pd.notna(row[11]) else ''
    segundo_apellido = str(row[12]).strip() if pd.notna(row[12]) else ''
    primer_nombre = str(row[13]).strip() if pd.notna(row[13]) else ''
    segundo_nombre = str(row[14]).strip() if pd.notna(row[14]) else ''
    cedula = str(row[9]).strip() if pd.notna(row[9]) else ''
    
    # Si no hay cédula, saltar este registro
    if not cedula or cedula == 'nan':
        print(f"⚠️  Registro sin cédula válida, omitido")
        continue

    # Construir nombre completo eliminando partes vacías
    partes_nombre = [primer_nombre, segundo_nombre, primer_apellido, segundo_apellido]
    partes_nombre = [p for p in partes_nombre if p and p != 'nan']
    nombre = " ".join(partes_nombre).strip()
    
    # Limpiar espacios dobles
    nombre = " ".join(nombre.split())
    
    if not nombre:
        print(f"⚠️  Registro con cédula {cedula} sin nombre válido, omitido")
        continue

    # Nombre del archivo: con espacios entre los nombres
    nombre_archivo = nombre.upper()
    nombre_salida = f"20250528-{cedula}-{nombre_archivo}.docx"
    path_salida = os.path.join(OUTPUT_DIR, nombre_salida)

    print(f"\n{'='*60}")
    print(f"Generando certificado para:")
    print(f"  Nombre: {nombre.upper()}")
    print(f"  Cédula: {cedula}")
    print(f"  Archivo: {nombre_salida}")
    print(f"{'='*60}")
    
    # REEMPLAZO PROFUNDO QUE FUNCIONA INCLUSO EN CUADROS DE TEXTO
    reemplazar_en_docx(
        CERTIFICADO_BASE,
        path_salida,
        nombre,
        cedula
    )

print("Certificados generados correctamente con Mammoth.")
