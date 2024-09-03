import flet as ft


class Controller:
    def __init__(self, view, model):
        self.view = view
        self.model = model

        self.mail_utente = None



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
                    stringa_destinazioni = ", ".join(destinazioni)+" -- "+str(data)
                    lista_opzioni.append(ft.dropdown.Option(key=trip, text=stringa_destinazioni))
                self.view.ddViaggi.options = lista_opzioni



                #dropdown voto
                lista_voti = []
                for i in range(1,6):
                    lista_voti.append(ft.dropdown.Option(key=i, text=i*'★'))
                self.view.ddVoti.options = lista_voti
                self.view.contentValuta.controls.append(self.view.rowValutazione)
            else:
                self.view.create_alert(f"Nessun viaggio trovato per l'indirizzo mail: {self.mail_utente}")
        else:
            self.view.create_alert("Email non inserita!!")

        self.view.update_page()

    def valutaViaggio(self,e):
        try:
            trip_id = int(self.view.ddViaggi.value)
            voto = int(self.view.ddVoti.value)

            if not self.model.valutaViaggio(trip_id, voto, self.mail_utente):
                self.view.create_alert("Viaggio già valutato!")
            else:
                rigaRisultato = ft.Row(controls=[ft.Text("Valutazione registrata correttamente", color="blue", size=16 )], alignment=ft.MainAxisAlignment.CENTER)
                self.view.contentValuta.controls.append(rigaRisultato)
        except TypeError:
            self.view.create_alert("Viaggio o valutazione non selezionati!!")
        self.view.update_page()