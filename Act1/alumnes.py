def alumne_schema(alumne) -> dict:
    return {
        
        "Id": alumne[0],
        "Nomalumne": alumne[1],
        "Cicle": alumne[2],
        "Curs": alumne[3],
        "Grup": alumne[4],
        "IdAula": alumne[5],
        "CreatedAt": alumne[6],
        "UpdatedAt": alumne[7]
    }


def alumnes_schema(alumnes) -> list:
    return [alumne_schema(alumne) for alumne in alumnes]

#Este codigo convierte el registro en un diccionario legible