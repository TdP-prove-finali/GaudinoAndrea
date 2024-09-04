import flet as ft
from datetime import datetime

class Controller:
    def __init__(self, view, model):
        self.view = view
        self.model = model

        self.mail_utente = None


        self.listaDraggable = []
        self.listaTarget = []

    def cercaViaggiUtente(self, e):
        self.mail_utente = self.view.mail_utente.value
        if self.mail_utente != "":
            #dropdown viaggi
            dizio = self.model.getViaggiUtente(self.mail_utente)
            if len(dizio) != 0:
                lista_opzioni = []
                for trip in dizio:
                    data = dizio[trip][0][1]
                    destinazioni = [x[0] for x in dizio[trip]]
                    stringa_destinazioni = ", ".join(destinazioni) + " -- " + str(data)
                    lista_opzioni.append(ft.dropdown.Option(key=trip, text=stringa_destinazioni))
                self.view.ddViaggi.options = lista_opzioni

                #dropdown voto
                lista_voti = []
                for i in range(1, 6):
                    lista_voti.append(ft.dropdown.Option(key=i, text=i*'★'))
                self.view.ddVoti.options = lista_voti
                self.view.contentValuta.controls.append(self.view.rowValutazione)
            else:
                self.view.create_alert(f"Nessun viaggio trovato per l'indirizzo mail: {self.mail_utente}")
        else:
            self.view.create_alert("Email non inserita!!")

        self.view.update_page()

    def valutaViaggio(self, e):
        try:
            trip_id = int(self.view.ddViaggi.value)
            voto = int(self.view.ddVoti.value)

            if not self.model.valutaViaggio(trip_id, voto, self.mail_utente):
                self.view.create_alert("Viaggio già valutato!")
            else:
                rigaRisultato = ft.Row(controls=[ft.Text("Valutazione registrata correttamente", color="blue", size=16)], alignment=ft.MainAxisAlignment.CENTER)
                self.view.contentValuta.controls.append(rigaRisultato)
        except TypeError:
            self.view.create_alert("Viaggio o valutazione non selezionati!!")
        self.view.update_page()

    def getUltimaDataPartenza(self):
        return self.model.getUltimaDataP()

    def getUltimaDataRitorno(self):
        return self.model.getUltimaDataR()

    def fillDDStati(self):
        stati = self.model.getStati()
        statiDD = list(map(lambda x: ft.dropdown.Option(text=x), stati))
        self.view.ddStati.options = statiDD
        self.view.update_page()

    def fillDDCosto(self):
        categorieCosto = self.model.getCateCosto()
        categorieCostoDD = list(map(lambda x: ft.dropdown.Option(text=x, key=x.count("$")), categorieCosto))
        self.view.ddCategoriaCosto.options = categorieCostoDD
        self.view.update_page()

    def inviaDati(self, e):
        if self.view.textDataPartenza.value == "":
            self.view.create_alert("Data di partenza non selezionata")
            return

        dataP = datetime.strptime(self.view.textDataPartenza.value, "%d-%m-%Y")
        dataR = None
        if self.view.textDataRitorno.value != "":
            dataR = datetime.strptime(self.view.textDataRitorno.value, "%d-%m-%Y")
        dateFlessibili = self.view.dateFlessibili.value
        destinazionePrimaria = self.view.ddStati.value
        multiStato = self.view.piuStati.value
        costo = self.view.ddCategoriaCosto.value

        input_data = {"Data partenza": dataP, "Data ritorno": dataR, "Destinazione": destinazionePrimaria, "Costo": costo}

        self.listaDraggable.clear()
        self.listaTarget.clear()

        for index, key in enumerate(input_data):
            if input_data[key] is not None:
                draggable = ft.Draggable(
                    content=ft.Container(
                        width=250,
                        height=50,
                        border_radius=5,
                        bgcolor='yellow',
                        content=ft.Text(key, size=20),
                        alignment=ft.alignment.center,
                    ),
                    data=key
                )
                target = ft.DragTarget(
                    content=ft.Container(
                        width=250,
                        height=50,
                        border_radius=5,
                        bgcolor='lightgreen',
                        content=ft.Text("", size=20),
                        alignment=ft.alignment.center,
                    ),
                    on_accept=lambda e, i=index: self.drag_accept(e, i)
                )

                self.listaDraggable.append(draggable)
                self.listaTarget.append(target)

        self.view.colonnaDraggable.controls = self.listaDraggable
        self.view.colonnaTarget.controls = self.listaTarget
        self.view.contentPrenota.controls.append(self.view.rowOrdinamento)
        self.view.update_page()

    def drag_accept(self, e, index):
        # Recupera il controllo sorgente
        src = self.view.page.get_control(e.src_id)
        # Aggiorna il testo nel drag target corrispondente
        self.listaTarget[index].content.content.value = src.data
        self.view.update_page()

    def ricercaViaggi(self, e):
        pass
