# Actividad 1 - Taller de Lenguajes Python (UNLP)

# Columnas de la EPH con tipos y porcentaje de completitud
columnas_eph = {
    "PONDERA": {"tipo": "int", "completitud": 100.0},
    "ESTADO": {"tipo": "int", "completitud": 100.0},
    "CAT_OCUP": {"tipo": "int", "completitud": 64.5},
    "EDAD": {"tipo": "int", "completitud": 100.0},
    "REGION": {"tipo": "int", "completitud": 100.0},
    "AGLOMERADO": {"tipo": "int", "completitud": 100.0},
    "MAS_500": {"tipo": "string", "completitud": 100.0},
    "ANO4": {"tipo": "int", "completitud": 100.0},
    "TRIMESTRE": {"tipo": "int", "completitud": 100.0},
    "ITF": {"tipo": "int", "completitud": 88.2},
    "GDECCFR": {"tipo": "int", "completitud": 85.0},
}

# Configuración de los roles
tipos_roles = {
    "docente": {
        "columnas_de_interes": ("PONDERA", "ANO4", "GDECCFR"),
        "criterio": "completitud",
        "forma": "B",  # B: descendente
        "completitud_minima": 70.0,
    },
    "investigador": {
        "columnas_de_interes": ("REGION", "AGLOMERADO", "CAT_OCUP"),
        "criterio": "nombre",
        "forma": "A",  # A: ascendente
        "completitud_minima": 80.0,
    },
    "analista": {
        "columnas_de_interes": ("MAS_500", "TRIMESTRE", "ITF"),
        "criterio": "completitud",
        "forma": "A",  # A: ascendente
        "completitud_minima": None,  # opcional: no tiene umbral
    },
}


def filtrar_por_completitud(columnas, minimo=None, datos_eph=columnas_eph):
    """
    Filtra las columnas según el porcentaje mínimo.
    Si no hay mínimo configurado, devuelve la lista completa.
    """
    if minimo is not None:
        def cumple_minimo(columna):
            return datos_eph[columna]["completitud"] >= minimo

        return list(filter(cumple_minimo, columnas))

    return list(columnas)


def generar_informe(rol=None, columnas=columnas_eph, roles=tipos_roles):
    """
    Arma y muestra el informe según el rol que se le pase.
    Si no se pasa ningún rol, muestra todas las columnas de mayor a menor completitud.
    """
    if rol is not None and rol in roles:
        datos_del_rol = roles[rol]
        columnas_interes = datos_del_rol["columnas_de_interes"]
        minimo = datos_del_rol["completitud_minima"]
        criterio = datos_del_rol["criterio"]
        forma = datos_del_rol["forma"]

        # Filtro las columnas si hay un porcentaje mínimo
        columnas_filtradas = filtrar_por_completitud(columnas_interes, minimo, columnas)

        # Si la forma es 'B' ordeno descendente, si es 'A' ascendente
        es_descendente = (forma == "B")

        # Ordeno según el criterio configurado para ese rol
        if criterio == "completitud":
            columnas_ordenadas = sorted(
                columnas_filtradas,
                key=lambda col: columnas[col]["completitud"],
                reverse=es_descendente
            )
        else:
            columnas_ordenadas = sorted(
                columnas_filtradas,
                reverse=es_descendente
            )

        print(f"\n--- Informe para el rol: {rol.upper()} ---")
        print(f"Criterio: {criterio} | Forma: {'Descendente (B)' if es_descendente else 'Ascendente (A)'}")
        if minimo is not None:
            print(f"Filtro aplicado: Completitud mínima >= {minimo}%")
        print("-" * 55)

    else:
        # Si se ingresó un rol pero no existe en el diccionario
        if rol is not None:
            print(f"\nRol '{rol}' no identificado. Se muestran las columnas por defecto:")
        else:
            print("\n--- Informe General: Todas las columnas (Completitud Descendente) ---")
        print("-" * 55)

        # Caso por defecto: ordeno todas las columnas de mayor a menor completitud
        todas_las_columnas = list(columnas.keys())
        columnas_ordenadas = sorted(
            todas_las_columnas,
            key=lambda col: columnas[col]["completitud"],
            reverse=True
        )

    # Imprimo las columnas
    if not columnas_ordenadas:
        print("Ninguna columna cumplió con el porcentaje mínimo requerido.")
    else:
        for col in columnas_ordenadas:
            tipo = columnas[col]["tipo"]
            comp = columnas[col]["completitud"]
            print(f"Columna: {col:<12} | Tipo: {tipo:<7} | Completitud: {comp}%")

    return columnas_ordenadas


# pido que se ingrese el rol por teclado para generar el informe 
if __name__ == "__main__":
    entrada = input("Ingresá un rol (docente, investigador, analista) o presioná Enter para ver todas: ").strip().lower()
    generar_informe(entrada if entrada else None)
