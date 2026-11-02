from database.DB_connect import get_connection
from model.strumento import Strumento
from model.prestito import Prestito

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        self._nome = nome
        self._responsabile = responsabile

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        self._nome = nome

    @property
    def responsabile(self):
        return self._responsabile

    @responsabile.setter
    def responsabile(self, responsabile):
        self._responsabile = responsabile

    def get_strumenti(self) -> list[Strumento] | None: #deve recuperare tutti i record dalla tabella strumento del database e restituire una lista di istanze di tipo Strumento (oppure None se si verifica un errore)
        """
            Funzione che legge tutti gli strumenti nel database
            :return: una lista con tutti gli strumenti presenti oppure None
        """
        cnx = get_connection()
        if cnx is None:
            return None

        cursor = None
        strumenti = []
        try:
            cursor = cnx.cursor(dictionary=True)
            query = "SELECT codice, tipo, marca, anno_acquisto, valore, disponibile FROM strumento"
            cursor.execute(query)

            for row in cursor.fetchall():
                strumento = Strumento(
                    codice=row["codice"],
                    tipo=row["tipo"],
                    marca=row["marca"],
                    anno_acquisto=row["anno_acquisto"],
                    valore=float(row["valore"]),
                    disponibile=bool(row["disponibile"])
                )
                strumenti.append(strumento)
            return strumenti
        except Exception as e:
            print(f"Errore nella lettura degli strumenti: {e}")
            return None
        finally:
            if cursor is not None:
                cursor.close()
            cnx.close()

    def cerca_strumenti_per_tipo(self, tipo) -> list[Strumento] | None: #deve filtrare gli strumenti per tipo e restituire la lista corrispondente (oppure None se la connessione fallisce)
        """
            Funzione che recupera una lista con tutti gli strumenti presenti nel database di un certo tipo
            :param tipo: il tipo dello strumento (es. "Chitarra")
            :return: una lista con tutti gli strumenti del tipo indicato oppure None
        """
        cnx = get_connection()
        if cnx is None:
            return None

        cursor = None
        strumenti = []
        try:
            cursor = cnx.cursor(dictionary=True)
            query = "SELECT codice, tipo, marca, anno_acquisto, valore, disponibile FROM strumento WHERE LOWER(tipo) = LOWER(%s)"
            cursor.execute(query, (tipo.strip(),)) # uso query parametrizzata (%s)

            for row in cursor.fetchall():
                strumento = Strumento(
                    codice=row["codice"],
                    tipo=row["tipo"],
                    marca=row["marca"],
                    anno_acquisto=row["anno_acquisto"],
                    valore=float(row["valore"]),
                    disponibile=bool(row["disponibile"])
                )
                strumenti.append(strumento)
            return strumenti
        except Exception as e:
            print(f"Errore nella ricerca per tipo: {e}")
            return None
        finally:
            if cursor is not None:
                cursor.close()
            cnx.close()
