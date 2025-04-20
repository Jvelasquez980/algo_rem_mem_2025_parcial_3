#!/usr/bin/env python
#Jeronimo Velasquez Escobar
#2025-1
#Parcial 3-Sistemas Operativos
marcos_libres = [0x0,0x1,0x2]
reqs = [ 0x00, 0x12, 0x64, 0x65, 0x8D, 0x8F, 0x19, 0x18, 0xF1, 0x0B, 0xDF, 0x0A ]
segmentos =[ ('.text', 0x00, 0x1A),
             ('.data', 0x40, 0x28),
             ('.heap', 0x80, 0x1F),
             ('.stack', 0xC0, 0x22),
            ]

PAGE_SIZE = 0x10  # Tamaño de pagina que esta definido en el parcial 

def procesar(segmentos, reqs, marcos_libres):
    tabla_paginas = {}         # clave: (segmento, pagina), valor: marco
    orden_fifo = []            # para mantener orden FIFO de carga
    resultados = []

    for req in reqs:
        segmento = None
        for nombre, base, limite in segmentos:
            if base <= req < base + limite:
                segmento = nombre
                offset = req - base
                break

        if segmento is None:
            resultados.append((req, 0x1FF, "Segmentation Fault"))
            continue

        pagina = offset // PAGE_SIZE
        desplazamiento = offset % PAGE_SIZE
        clave = (segmento, pagina)

        if clave in tabla_paginas:
            marco = tabla_paginas[clave]
            accion = "Marco ya estaba asignado"
        else:
            if len(tabla_paginas) < len(marcos_libres):
                marco = marcos_libres[len(tabla_paginas)]
                accion = "Marco libre asignado"
            else:
                viejo = orden_fifo.pop(0)
                marco = tabla_paginas.pop(viejo)
                accion = "Marco asignado"
            tabla_paginas[clave] = marco
            orden_fifo.append(clave)

        direccion_fisica = (tabla_paginas[clave] << 4) + desplazamiento
        resultados.append((req, direccion_fisica, accion))

    return resultados

    
def print_results(results):
    for result in results:
        print(f"Req: {result[0]:#0{4}x} Direccion Fisica: {result[1]:#0{4}x} Acción: {result[2]}")

if __name__ == '__main__':
    results = procesar(segmentos, reqs, marcos_libres)
    print_results(results)

