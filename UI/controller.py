import flet as ft
from UI.view import View
from model.model import DepositoStrumenti

'''
    CONTROLLER:
    - Funziona da intermediario tra MODELLO e VIEW
    - Gestisce la logica del flusso dell'applicazione
'''

class Controller:
    def __init__(self, view: View, model: DepositoStrumenti):
        self._model = model
        self._view = view

    def get_nome(self):
        return self._model.nome

    def get_responsabile(self):
        return self._model.responsabile

    def set_responsabile(self, responsabile):
        self._model.responsabile = responsabile

    def conferma_responsabile(self, e):
        self._model.responsabile = self._view.input_responsabile.value
        self._view.txt_responsabile.value = f"Responsabile: {self._model.responsabile}"
        self._view.update()

    # Altre Funzioni Event Handler
    def mostra_strumenti(self, e): #gestisce il click sul pulsante 'Mostra' per elencare tutti gli strumenti
        self._view.lista_strumenti.controls.clear() #svuota la self._view.lista_strumenti.controls per non duplicare elementi in caso di click multipli
        strumenti = self._model.get_strumenti()

        if strumenti is None:
            self._view.show_alert("Errore durante la connessione al database o il recupero dei dati!")
            self._view.update()
            return

        if len(strumenti) == 0:
            self._view.lista_strumenti.controls.append(ft.Text("Nessuno strumento presente nel deposito."))
        else:
            for strumento in strumenti:
                self._view.lista_strumenti.controls.append(ft.Text(str(strumento)))

        self._view.update()

    def cerca_strumenti(self, e): #gestisce il click sul pulsante 'Cerca' per filtrare gli strumenti per tipo
        self._view.lista_strumenti_ricerca.controls.clear() #svuota self._view.lista_strumenti_ricerca.controls
        tipo_cercato = self._view.input_tipo_strumento.value #legge il valore digitato in self._view.input_tipo_strumento.value

        if not tipo_cercato or tipo_cercato.strip() == "":
            self._view.show_alert("Inserisci un tipo di strumento prima di avviare la ricerca!")
            self._view.update()
            return

        strumenti = self._model.cerca_strumenti_per_tipo(tipo_cercato.strip())

        if strumenti is None:
            self._view.show_alert("Errore durante la ricerca nel database!")
            self._view.update()
            return

        if len(strumenti) == 0: #se la lista restituita è vuota
            self._view.lista_strumenti_ricerca.controls.append(
                ft.Text(f"Nessuno strumento trovato per il tipo: '{tipo_cercato}'.")
            )
        else:
            for strumento in strumenti:
                self._view.lista_strumenti_ricerca.controls.append(ft.Text(str(strumento)))

        self._view.update()