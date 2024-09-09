import flet as ft
import datetime

class Controller:
    def __init__(self, view, model):
        self.view = view
        self.model = model

        self.mail_utente = None
        self.tabPrenota = None
        self.creaTab()

        # self.listaDraggable = []
        # self.listaTarget = []

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

    # def getUltimaDataPartenza(self):
    #     return self.model.getUltimaDataP()
    #
    # def getUltimaDataRitorno(self):
    #     return self.model.getUltimaDataR()

    def fillDDStati(self):
        stati = self.model.getStati()
        statiDD = list(map(lambda x: ft.dropdown.Option(text=x), stati))
        self.view.ddStati.options = statiDD
        self.view.update_page()

    def fillDDCosto(self):
        categorieCosto = self.model.getCateCosto()
        categorieCostoDD = list(map(lambda x: ft.dropdown.Option(text=x, key=x.count("$")), categorieCosto))
        self.view.ddCategoriaCosto.options.append(ft.dropdown.Option(text='Qualsiasi'))
        for i in categorieCostoDD:
            self.view.ddCategoriaCosto.options.append(i)
        self.view.ddCategoriaCosto.value = "Qualsiasi"
        self.view.update_page()

    def fillDDMese(self):
        listaMesi = [
            ("Gennaio", 1),
            ("Febbraio", 2),
            ("Marzo", 3),
            ("Aprile", 4),
            ("Maggio", 5),
            ("Giugno", 6),
            ("Luglio", 7),
            ("Agosto", 8),
            ("Settembre", 9),
            ("Ottobre", 10),
            ("Novembre", 11),
            ("Dicembre", 12),

        ]
        for r in listaMesi:
            self.view.mesePartenza.options.append(ft.dropdown.Option(text=r[0], key=r[1]))
        self.view.update_page()


    # def inviaDati(self, e):
    #     mese = int(self.view.mesePartenza.value)
    #     anno = int(self.view.annoPartenza.value)
    #     destinazionePrimaria = self.view.ddStati.value
    #     costo = self.view.ddCategoriaCosto.value
    #
    #     self.input_data = {"Data partenza": dataP, "Durata viaggio": durata, "Destinazione": destinazionePrimaria, "Costo": costo}
    #
    #     self.listaDraggable.clear()
    #     self.listaTarget.clear()
    #
    #     index = 0
    #     for key in self.input_data:
    #         if self.input_data[key] is not None and key != "Durata viaggio":
    #             draggable = ft.Draggable(
    #                 content=ft.Container(
    #                     width=250,
    #                     height=50,
    #                     border_radius=5,
    #                     bgcolor='yellow',
    #                     content=ft.Text(key, size=20),
    #                     alignment=ft.alignment.center,
    #                 ),
    #                 data=key
    #             )
    #             target = ft.DragTarget(
    #                 content=ft.Container(
    #                     width=250,
    #                     height=50,
    #                     border_radius=5,
    #                     bgcolor='lightgreen',
    #                     opacity=0.7,
    #                     content=ft.Text("", size=20),
    #                     alignment=ft.alignment.center,
    #                 ),
    #                 on_accept=lambda e, i=index: self.drag_accept(e, i)
    #             )
    #
    #             self.listaDraggable.append(draggable)
    #             self.listaTarget.append(target)
    #             index+=1
    #     self.view.colonnaDraggable.controls = self.listaDraggable
    #     self.view.colonnaTarget.controls = self.listaTarget
    #     self.view.contentPrenota.controls.append(ft.Row(controls=[ft.Text("Ordina i parametri per importanza", color='blue', size= 18)], alignment=ft.MainAxisAlignment.CENTER))
    #     self.view.contentPrenota.controls.append(self.view.rowOrdinamento)
    #     self.view.update_page()
    #
    # def drag_accept(self, e, index):
    #     # Recupera il controllo sorgente
    #     src = self.view.page.get_control(e.src_id)
    #     # Aggiorna il testo nel drag target corrispondente
    #     self.listaTarget[index].content.content.value = src.data
    #     self.view.update_page()

    def ricercaViaggi(self, e):
        mese = self.view.mesePartenza.value
        anno = self.view.annoPartenza.value
        today = datetime.date.today()
        destinazionePrimaria = self.view.ddStati.value
        costo = self.view.ddCategoriaCosto.value

        if mese is None or anno is None or destinazionePrimaria is None or costo is None:
            self.view.create_alert("Parametri mancanti!!")
            return

        meseInt = int(mese)
        annoInt = int(anno)
        if meseInt < today.month and annoInt == today.year:
            self.view.create_alert("Mese e anno selezionati antecedenti ad oggi!!")
            return

        dizio_viaggi = self.model.cercaViaggi(meseInt, annoInt, destinazionePrimaria, costo)
        lista_viaggi = list(dizio_viaggi.keys())
        if costo != 'Qualsiasi':
            lista_viaggi.sort(key=lambda x: abs(x.package_cost_category_id - int(costo)))
        else:
            lista_viaggi.sort(key=lambda x: x.package_cost_category_id)

        self.view.colViaggi.controls.clear()
        for v in lista_viaggi:
            offerte = self.model.cercaOfferteViaggio(v.trip_package_id, datetime.date.today())

            # Crea una colonna per ogni viaggio
            row = ft.Row(alignment=ft.MainAxisAlignment.CENTER)

            # Crea un'etichetta per le offerte
            label = ft.Text(value='')
            container = ft.Container(padding=10)
            if len(offerte) > 0:
                label = ft.Text("OFFERTA DISPONIBILE", size=15, color="red")
                container.border = ft.border.all(2, "red")
                container.border_radius = ft.border_radius.all(value=4.0)
            else:
                container.border = ft.border.all(2, "blue")
                container.border_radius = ft.border_radius.all(value=4.0)

            # Aggiungi le destinazioni e il costo al contenitore
            destinazioni = set(x.country for x in dizio_viaggi[v][0])
            strDestinazioni = ", ".join(map(str, destinazioni))
            rowDestinazioni = ft.Row(
                controls=[ft.Text('Destinazioni: ', weight=ft.FontWeight.BOLD), ft.Text(value=strDestinazioni)])
            costoViaggio = v.cost_attraction + v.cost_accomodation
            rowCosto = ft.Row(controls=[ft.Text('Costo: ', weight=ft.FontWeight.BOLD), ft.Text(value=str(costoViaggio))])

            rowPartenza = ft.Row(controls=[ft.Text("Data partenza: ", weight=ft.FontWeight.BOLD),ft.Text(v.trip_start.strftime("%d-%m-%Y"))])

            btnDettagli = ft.ElevatedButton(text="Dettagli viaggio", on_click=lambda e: self.dettagliViaggio(dizio_viaggi[v][0], dizio_viaggi[v][1], dizio_viaggi[v][2]))

            btnPrenota = ft.ElevatedButton(text="Prenota viaggio", on_click=lambda e: self.prenota(v))

            # Imposta il contenuto del contenitore e aggiungi alla colonna
            row.controls = [rowDestinazioni, rowCosto, rowPartenza, btnDettagli, btnPrenota]
            container.content = row

            #colonnaDaAggiungere = ft.Column(controls=[label, container])
            # Aggiungi la colonna alla pagina

            self.view.colViaggi.controls.append(ft.Column(controls=[label, container], spacing=-10))



        # Forzare l'aggiornamento della pagina
        self.view.update_page()



    def dettagliViaggio(self, destination, attraction, guide):
        citta = [x.name for x in destination]
        strCitta = ", ".join(map(str, citta))
        rowCitta = ft.Row(controls=[ft.Text("Città: ", weight=ft.FontWeight.BOLD), ft.Text(strCitta)])
        listaAttraction = []
        for a in attraction:
            if a.travel_guide_employee_AM is None:
                listaAttraction.append(f"{a.name}")
            else:
                guida = guide[a.travel_guide_employee_AM]
                nomeGuida = list(guida.keys())[0]
                lingue = guida[nomeGuida]
                strLingue = ", ".join(map(str, lingue))
                listaAttraction.append(f"{a.name} -- Guida: {nomeGuida} -- Lingue parlate: {strLingue}")
        colAttrazioni = ft.Column(controls=[ft.Text(x) for x in listaAttraction])
        rowAttraction = ft.Row(controls=[colAttrazioni])
        colonna = ft.Column(controls=[rowCitta, ft.Text("Attrazioni: ",  weight=ft.FontWeight.BOLD) , rowAttraction], height=500)
        self.dlg = ft.AlertDialog(content=colonna, actions=[ft.TextButton("Chiudi", on_click=self.chiudi_dialog)])
        self.view.page.dialog = self.dlg
        self.dlg.open = True

        self.view.update_page()

    def chiudi_dialog(self, e):
        self.dlg.open = False
        self.view.update_page()

    def prenota(self, viaggio):
        self.view.tabs.tabs.append(self.tabPrenota)
        self.view.update_page()

    def creaTab(self):
        self.tabPrenota = ft.Tab(text="Inserisci dati", content=self.creaContenutoTab())
        # Assegna la colonna come contenuto della tab
        #self.tabPrenota.content = colInput


    def autoCompila(self, email):
        if email.value is None:
            self.view.create_alert("Email non inserita")
            return
        self.traveler = self.model.autoCompila(email)
        self.view.name.value = self.traveler.name
        self.view.surname.value = self.traveler.surname
        self.view.age.value = self.traveler.age
        self.view.address.value = self.traveler.address
        self.view.phone.value = self.traveler.phone



    def creaContenutoTab(self):
        # Campo email con bottone Auto-compila in una riga
        email = ft.TextField(label="Email", width=300)
        btnAutoCompila = ft.ElevatedButton(text="Auto-compila", on_click=lambda e: self.autoCompila(email))
        emailRow = ft.Row(controls=[email, btnAutoCompila], alignment=ft.MainAxisAlignment.CENTER)

        # Altri campi di input (Nome, Cognome, Età, etc.)
        self.name = ft.TextField(label="Nome", width=200)
        self.surname = ft.TextField(label="Cognome", width=200)
        self.age = ft.TextField(label="Età", width=100)
        self.address = ft.TextField(label="Indirizzo", width=400)
        self.phone = ft.TextField(label="Telefono", width=200)

        # Dropdown per gender
        self.gender = ft.Dropdown(
            label="Genere",
            options=[
                ft.dropdown.Option(text='Uomo', key='Male'),
                ft.dropdown.Option(text='Donna', key='Female'),
                ft.dropdown.Option(text='Altro', key='Other')  # Usa 'Other' come chiave
            ],
            width=200
        )

        # Organizzazione dei campi input in righe
        row1 = ft.Row(controls=[self.name, self.surname])
        row2 = ft.Row(controls=[self.age, self.phone])
        row3 = ft.Row(controls=[self.address])
        row4 = ft.Row(controls=[self.gender])

        # Creazione della colonna che contiene tutte le righe
        colInput = ft.Column(
            controls=[ft.Container(height=4), emailRow, row1, row2, row3, row4],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20  # Aggiungi spazio tra le righe per evitare sovrapposizioni
        )

        return colInput




