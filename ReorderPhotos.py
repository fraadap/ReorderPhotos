import os
import shutil
import re
from datetime import datetime
import tkinter as tk
from tkinter import filedialog


def filtro_data(data1):
    """
    Funzione per formattare la data nel formato YYYYMM
    """
    d = data1[:10]
    d = d.replace("-", "")
    d = d.replace("_", "")
    return d[:6]


def seleziona_cartella():
    """
    Funzione per selezionare la cartella da esplorare tramite interfaccia grafica
    """
    root = tk.Tk()
    root.withdraw()
    cartella = filedialog.askdirectory()
    return cartella


def sposta_file(cartella, f):
    """
    Funzione per spostare il file nella sottocartella corretta
    """
    try:
        # Estraggo la data dal nome del file
        if f.startswith("VID_") or f.startswith("IMG_"):
            anno = f.split("_")[1][:4]
            mese = f.split("_")[1][4:6]
            data = anno + mese
        else:
            # Estraggo la data di creazione del file
            data1 = datetime.fromtimestamp(os.path.getctime(os.path.join(cartella, f)))
            data = filtro_data(str(data1))

        # Se la cartella dell'anno/mese non esiste, la creo
        if not os.path.exists(os.path.join(cartella, data[:4], data[4:6])):
            os.makedirs(os.path.join(cartella, data[:4], data[4:6]))

        # Sposto il file nella sottocartella corretta
        shutil.move(os.path.join(cartella, f), os.path.join(cartella, data[:4], data[4:6], f))
        print(f"Spostato il file {f} in {os.path.join(cartella, data[:4], data[4:6], f)}")
    except Exception as e:
        print(f"Errore durante lo spostamento del file {f}: {e}")


def esplora_cartella(cartella):
    """
    Funzione per esplorare la cartella e spostare i file nella sottocartella corretta
    """
    print(f"Esplorazione della cartella {cartella}...")
    for root, dirs, files in os.walk(cartella):
        for f in files:
            # Se il file ha come nome un anno o un mese, lo salto
            if re.match(r"^\d{4}$", f) or re.match(r"^\d{2}$", f):
                continue
            else:
                sposta_file(root, f)


# Main
if __name__ == '__main__':
    # Seleziono la cartella da esplorare tramite interfaccia grafica
    cartella = seleziona_cartella()
    # Esploro la cartella e sposto i file nella sottocartella corretta
    esplora_cartella(cartella)
    print("Operazione completata.")
