import datetime

import flet as ft


class View:
    def __init__(self,page=ft.Page):
        super().__init__()
        self.page = page
        self.controller = None





    def load_interface(self):
        self.titolo = ft.Row([ft.Text("Agenzia viaggi VOYAGE", color='blue', size=28)], alignment=ft.MainAxisAlignment.CENTER )
        self.tabs = ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(text="Prenota", content=self.content_prenota(),icon = ft.icons.EVENT),
                ft.Tab(text="Valuta", content=self.content_valuta(), icon=ft.icons.STAR),

            ],
        )

        self.page.controls = [self.titolo, self.tabs]



        self.update_page()


    def content_prenota(self):
        self.contentPrenota = ft.Column(spacing=30)
        #Titolo
        self.title_prenota = ft.Row([ft.Text("Prenota il tuo viaggio!!!", color='blue', size=24)], alignment=ft.MainAxisAlignment.CENTER)

        #Riga
        dataPartenza = ft.ElevatedButton(text='Scegli data', on_click= lambda e: self.page.open(
            ft.DatePicker(first_date=datetime.datetime.today(), last_date=self.controller.getUltimaDataPartenza(), on_change=self.riempiDataPartenza),))
        self.textDataPartenza = ft.TextField(label="Data partenza", border_color='red', border_width=2, width=200, read_only=True)
        self.dataRitorno = ft.ElevatedButton(text="Scegli data", disabled=True, on_click= lambda e: self.page.open(
            ft.DatePicker(first_date=datetime.datetime.strptime(self.textDataPartenza.value, "%d-%m-%Y")+datetime.timedelta(days=1), last_date=self.controller.getUltimaDataRitorno(), on_change=self.riempiDataRitorno),
        ))
        self.textDataRitorno = ft.TextField(label="Data ritorno", width=200, read_only=True)
        self.dateFlessibili = ft.Checkbox(label="Date flessibili")
        rowDatiInput = ft.Row(controls=[self.textDataPartenza, dataPartenza, self.textDataRitorno, self.dataRitorno, self.dateFlessibili], alignment=ft.MainAxisAlignment.CENTER)

        self.ddStati = ft.Dropdown(label="Destinazione")
        self.controller.fillDDStati()
        self.piuStati = ft.Checkbox(label="Viaggio multi-stato")
        self.ddCategoriaCosto = ft.Dropdown(label="Costo")
        self.controller.fillDDCosto()

        rowDatiInput2 = ft.Row(controls=[self.ddStati, self.piuStati, self.ddCategoriaCosto, ft.ElevatedButton(text="Invia dati", on_click=self.controller.inviaDati)], alignment=ft.MainAxisAlignment.CENTER)

        self.rowOrdinamento = ft.Row(controls=[ft.Text("Ordina i parametri per importanza", size=18, color='blue')], alignment=ft.MainAxisAlignment.CENTER)
        self.colonnaDraggable = ft.Column()
        self.colonnaTarget = ft.Column()
        btnInviaDati = ft.ElevatedButton(text="Ricerca viaggi", on_click=self.controller.ricercaViaggi)
        self.rowOrdinamento.controls = [self.colonnaDraggable, ft.Container(width=200) , self.colonnaTarget, btnInviaDati]

        self.contentPrenota.controls = [self.title_prenota, rowDatiInput, rowDatiInput2]
        return self.contentPrenota

    def content_valuta(self):
        self.contentValuta = ft.Column(spacing=30)
        #Titolo
        self.title_valuta = ft.Text("Valuta il tuo viaggio!!!", color='blue', size=24)
        rowTitle = ft.Row([self.title_valuta], alignment=ft.MainAxisAlignment.CENTER
                            )



        self.mail_utente = ft.TextField(label="Inserisci la tua email")
        rowMail = ft.Row(controls=[self.mail_utente, ft.ElevatedButton(text="Cerca i tuoi viaggi", on_click=self.controller.cercaViaggiUtente)]
                         , alignment=ft.MainAxisAlignment.CENTER)

        self.rowValutazione = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
        self.ddViaggi = ft.Dropdown(label="Scegli un viaggio", width=500)
        self.ddVoti = ft.Dropdown(label="Voto")
        btnValuta = ft.ElevatedButton(text="Valuta", on_click=self.controller.valutaViaggio)
        self.rowValutazione = ft.Row([self.ddViaggi, self.ddVoti, btnValuta],alignment=ft.MainAxisAlignment.CENTER)


        self.contentValuta.controls = [ft.Container(height=4),rowTitle, rowMail]

        return self.contentValuta






    def riempiDataPartenza(self, e):
        data =  e.data
        data_ora = datetime.datetime.strptime(data, "%Y-%m-%dT%H:%M:%S.%f")
        data_formattata = data_ora.strftime("%d-%m-%Y")
        self.textDataPartenza.value = data_formattata
        self.dataRitorno.disabled = False
        self.update_page()


    def riempiDataRitorno(self, e):
        data = e.data
        data_ora = datetime.datetime.strptime(data, "%Y-%m-%dT%H:%M:%S.%f")
        data_formattata = data_ora.strftime("%d-%m-%Y")
        self.textDataRitorno.value = data_formattata
        self.update_page()





    def set_controller(self, controller):
        self.controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def update_page(self):
        self.page.update()