import re


def normalizar_nombre_propio(name):
    """
    str -> str
    Función que transforma un texto a las normas
    del español de forma correcta para un nombre propio.
    >>>>normalizar_nombre_propio(" rigoberto   villalta   ")
    'Rigoberto Vilalta'
    >>>>normalizar_nombre_propio("Rigoberto  villalta   ")
    'Rigoberto Vilalta'
    >>>>normalizar_nombre_propio(" rigoberto Villalta.")
    'Rigoberto Vilalta'
    >>>>normalizar_nombre_propio(" María De Los   Ángeles ")
    'María de los Ángeles'
    >>>>normalizar_nombre_propio("Rosa Del Carmen")
    'Rosa del Carmen'
    >>>>normalizar_nombre_propio(" ernesto de la cruz.")
    'Ernesto de la Cruz'
    """
    nombre_normalizado = " ".join(name.strip().title().split())
    while " De " in nombre_normalizado:
        nombre_normalizado = nombre_normalizado.replace(" De ", " de ")
    while " Del " in nombre_normalizado:
        nombre_normalizado = nombre_normalizado.replace(" Del ", " del ")
    while " La " in nombre_normalizado:
        nombre_normalizado = nombre_normalizado.replace(" La ", " la ")
    while " Los " in nombre_normalizado:
        nombre_normalizado = nombre_normalizado.replace(" Los ", " los ")
    while "." in nombre_normalizado:
        nombre_normalizado = nombre_normalizado.replace(".", "")
    return nombre_normalizado


def verificador_dui_el_salvador(dui: str) -> bool:
    """
    función que verifica si una cdena ingresada corresponde a un número válido
    de un documento único de identidad de El Salvador incluyendo una expresión
    regular para verificar el formato y la operación del número verificador
    que es el último dígito.
    """
    if re.fullmatch("^\d{8}-\d$", dui):
        multiplicador = 9
        verificador = 0
        for digito in dui[:8]:
            verificador += int(digito) * multiplicador
            multiplicador -= 1
        if 10 - verificador % 10 == int(dui[-1]):
            return True
    return False
