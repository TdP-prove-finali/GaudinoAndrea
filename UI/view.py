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
                ft.Tab(text="Crea"),
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
        self.mesePartenza = ft.Dropdown(label="Mese partenza", width=200)
        self.controller.fillDDMese()
        self.annoPartenza = ft.Dropdown(label="Anno partenza", width=200, options=[
                                ft.dropdown.Option(text="2024"),
                                ft.dropdown.Option(text="2025")
        ])
        #rowDatiInput = ft.Row(controls=[dataPartenza,self.textDataPartenza,  self.durataViaggio], alignment=ft.MainAxisAlignment.CENTER)

        self.ddStati = ft.Dropdown(label="Destinazione", width=250)
        self.controller.fillDDStati()
        #self.piuStati = ft.Checkbox(label="Viaggio multi-stato")
        self.ddCategoriaCosto = ft.Dropdown(label="Costo", width=200)
        self.controller.fillDDCosto()

        rowDatiInput = ft.Row(controls=[self.mesePartenza, self.annoPartenza, self.ddStati, self.ddCategoriaCosto, ft.ElevatedButton(text="Ricerca viaggi", on_click=self.controller.ricercaViaggi)], alignment=ft.MainAxisAlignment.CENTER)

        # self.rowOrdinamento = ft.Row(controls=[ft.Text("Ordina i parametri per importanza", size=18, color='blue')], alignment=ft.MainAxisAlignment.CENTER)
        # self.colonnaDraggable = ft.Column()
        # self.colonnaTarget = ft.Column()
        # btnRicercaViaggi = ft.ElevatedButton(text="Ricerca viaggi", on_click=self.controller.ricercaViaggi)
        # self.rowOrdinamento.controls = [self.colonnaDraggable, ft.Container(width=200) , self.colonnaTarget, btnRicercaViaggi]

        self.colViaggi = ft.Column(alignment=ft.MainAxisAlignment.CENTER, auto_scroll=True)

        self.contentPrenota.controls = [ft.Container(height=4), self.title_prenota, rowDatiInput, ft.Divider(height=1, thickness=2, color="blue"), self.colViaggi]
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








    def set_controller(self, controller):
        self.controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def update_page(self):
        self.page.update()

