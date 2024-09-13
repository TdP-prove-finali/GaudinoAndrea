import copy
import datetime

import flet as ft


class View:
    def __init__(self,page=ft.Page):
        super().__init__()
        self.page = page
        self.controller = None
        self.page.scroll = 'adaptive'





    def load_interface(self):
        self.titolo = ft.Row([ft.Text("Agenzia viaggi VOYAGE", color='blue', size=28)], alignment=ft.MainAxisAlignment.CENTER )
        self.tabs = ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(text="Prenota", content=self.content_prenota(),icon = ft.icons.EVENT),
                ft.Tab(text="Crea", icon = ft.icons.MAP, content=self.content_crea()),
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
        self.ddCategoriaCosto = ft.Dropdown(label="Costo accomodation", width=200)
        self.controller.fillDDCosto()

        rowDatiInput = ft.Row(controls=[self.mesePartenza, self.annoPartenza, self.ddStati, self.ddCategoriaCosto, ft.ElevatedButton(text="Ricerca viaggi", on_click=self.controller.ricercaViaggi)], alignment=ft.MainAxisAlignment.CENTER)

        # self.rowOrdinamento = ft.Row(controls=[ft.Text("Ordina i parametri per importanza", size=18, color='blue')], alignment=ft.MainAxisAlignment.CENTER)
        # self.colonnaDraggable = ft.Column()
        # self.colonnaTarget = ft.Column()
        # btnRicercaViaggi = ft.ElevatedButton(text="Ricerca viaggi", on_click=self.controller.ricercaViaggi)
        # self.rowOrdinamento.controls = [self.colonnaDraggable, ft.Container(width=200) , self.colonnaTarget, btnRicercaViaggi]

        self.colViaggi = ft.Column(alignment=ft.MainAxisAlignment.CENTER, auto_scroll=True)
        btnVaiACreaPagina = ft.ElevatedButton(text='Crea il tuo viaggio', on_click=lambda e:self.vaiACrea([self.colViaggi,self.mesePartenza, self.annoPartenza, self.ddStati, self.ddCategoriaCosto ]))
        self.rowVaiACrea = ft.Row(controls=[ft.Text("Non trovi un viaggio che ti piaccia?", color='blue', size=16), btnVaiACreaPagina], alignment=ft.MainAxisAlignment.CENTER)

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
        self.ddViaggi = ft.Dropdown(label="Scegli un viaggio", width=700)
        self.ddVoti = ft.Dropdown(label="Voto")
        btnValuta = ft.ElevatedButton(text="Valuta", on_click=lambda e: self.controller.valutaViaggio([self.ddViaggi, self.ddVoti]))
        self.rowValutazione = ft.Row([self.ddViaggi, self.ddVoti, btnValuta],alignment=ft.MainAxisAlignment.CENTER)


        self.contentValuta.controls = [ft.Container(height=4),rowTitle, rowMail]

        return self.contentValuta

    def content_crea(self):
        self.contentCrea = ft.Column(spacing=30)
        titleCrea = ft.Row(controls=[ft.Text("Componi il tuo viaggio", color='blue', size=24)], alignment=ft.MainAxisAlignment.CENTER)
        self.textDataP = ft.TextField(label="Data partenza", read_only=True, width=150)
        #datePicker = ft.DatePicker(first_date=datetime.datetime.today(), on_change=self.rempiDataP)
        btnData = ft.ElevatedButton(text='Scegli data', on_click=lambda e: self.page.open(
            ft.DatePicker(first_date=datetime.datetime.today(),
                          on_change=self.riempiDataP)))
        # rowData = ft.Row(controls=[btnData, self.textDataP], alignment=ft.MainAxisAlignment.CENTER)
        self.ddCountry1 = ft.Dropdown(label='Scegli uno stato', on_change=self.abilitaCountry2)
        self.ddCountry2 = ft.Dropdown(label='Scegli uno stato', disabled=True, disabled_hint_content=ft.Text("Seleziona il primo stato!"), on_change=self.abilitaCountry3)
        self.ddCountry3 = ft.Dropdown(label='Scegli uno stato', disabled=True, disabled_hint_content=ft.Text("Seleziona il primo stato!"))
        self.numeroAttrazioniMax = ft.TextField(label="Numero attrazioni", width=100)
        rowStati = ft.Row(controls=[self.ddCountry1, self.ddCountry2, self.ddCountry3], alignment=ft.MainAxisAlignment.CENTER)
        self.controller.fillDDStatiCrea()
        self.ddLingue = ft.Dropdown(label='Lingua per le visite guidate')
        self.controller.fillDDLingue()
        self.ddCategoriaCostoCrea = copy.deepcopy(self.ddCategoriaCosto)
        self.ddCategoriaCostoCrea.options.pop(0)
        self.ddCategoriaCostoCrea.value = None
        rowUltimeCose = ft.Row(controls=[btnData, self.textDataP, self.numeroAttrazioniMax, self.ddLingue, self.ddCategoriaCostoCrea], alignment=ft.MainAxisAlignment.CENTER)
        rowInvia = ft.Row(controls=[ft.ElevatedButton(text='Crea viaggio', on_click=self.controller.creaViaggio)], alignment=ft.MainAxisAlignment.CENTER)
        self.colRisultati = ft.Column()
        self.contentCrea.controls = [ft.Container(height=4), titleCrea, ft.Row([ft.Text("Scegli da 1 a 3 stati per il tuo viaggio")], alignment=ft.MainAxisAlignment.CENTER),  rowStati, rowUltimeCose, rowInvia, ft.Divider(height=1, thickness=2, color="blue"), ft.Row(controls=[self.colRisultati], alignment=ft.MainAxisAlignment.CENTER)]

        return self.contentCrea


    def riempiDataP(self, e):
        data = e.data
        data_ora = datetime.datetime.strptime(data, "%Y-%m-%dT%H:%M:%S.%f")
        data_formattata = data_ora.strftime("%d-%m-%Y")
        self.textDataP.value = data_formattata
        self.update_page()



    def vaiACrea(self, listaP):
        self.tabs.selected_index = 1
        self.controller.svuotaParametri(listaP)
        self.update_page()



    def abilitaCountry2(self, e):
        self.ddCountry2.disabled = False
        self.ddCountry3.disabled_hint_content = ft.Text("Seleziona il secondo stato!")
        self.update_page()



    def abilitaCountry3(self, e):
        self.ddCountry3.disabled = False
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

