"""
questo file gestisce il file 'allUser.csv'
"""
from asyncio import Lock

# Creare un lock globale per evitare concorrenza durante la scrittura del file
lock_allPic = Lock()


async def update_all_pic(name: str, photo_id: str, override=False) -> bool:
    """
    aggiorna il file all pic

    :param name: nome della photo per essere impostata
    :type name: str
    :param photo_id: file id univoco per riusare il file
    :type photo_id: str
    :param override: sovrascrive la photo se esiste già il name
    :type override: bool
    :return: true se il caption è nuovo e valido
    :rtype: bool
    """
    import csv

    # Acquisire il lock prima di accedere al file
    async with lock_allPic:
        # Apri il file CSV in modalità lettura
        with open("../database/allPic.csv", mode='r', newline='', encoding='utf-8') as file:
            # Leggi il file CSV
            reader = csv.DictReader(file, delimiter=';')
            # Inizializza una lista per contenere tutte le righe del CSV
            rows = list(reader)

    if override:
        # elimina il vecchio nome se presente
        for row in rows:
            # Se l'ID utente è presente
            rname = str(row['name'])
            if rname == name:
                del row['name']
                break
    else:
        # Itera attraverso le righe del CSV
        for row in rows:
            # Se l'ID utente è presente
            rname = str(row['name'])
            if rname == name:
                return False

    # Se il caption è nuovo o da sovrascrivere, aggiungi una nuova riga
    nuova_riga = {'name': name, 'id': photo_id}
    rows.append(nuova_riga)

    # Acquisire il lock prima di accedere al file
    async with lock_allPic:
        # Scrivi nel file CSV aggiornato
        with open("../database/allPic.csv", mode='w', newline='', encoding='utf-8') as file:
            # Scrivi le righe aggiornate nel file
            writer = csv.DictWriter(file, fieldnames=['name', 'id'], delimiter=';')
            writer.writeheader()
            writer.writerows(rows)

    return True
