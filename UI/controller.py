import flet as ft
import datetime

from model.traveler import Traveler


class Controller:
    def __init__(self, view, model):
        self.view = view
        self.model = model

        self.mail_utente = None
        self.tabPrenota = None
        self.creaTab()
        self.traveler = None

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

    def valutaViaggio(self, listaP):
        try:
            trip_id = int(self.view.ddViaggi.value)
            voto = int(self.view.ddVoti.value)

            if not self.model.valutaViaggio(trip_id, voto, self.mail_utente):
                self.view.create_alert("Viaggio già valutato!")
            else:
                self.rigaRisultato = ft.Row(controls=[ft.Text("Valutazione registrata correttamente", color="blue", size=16)], alignment=ft.MainAxisAlignment.CENTER)
                self.view.contentValuta.controls.append(self.rigaRisultato)
                listaP.append(self.rigaRisultato)
                self.svuotaParametri(listaP)
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
    def fillDDStatiCrea(self):
        stati = self.model.getStati()
        statiDD = list(map(lambda x: ft.dropdown.Option(text=x), stati))
        self.view.ddCountry1.options = statiDD
        self.view.ddCountry2.options = statiDD
        self.view.ddCountry3.options = statiDD
        self.view.update_page()

    def fillDDLingue(self):
        lingue = self.model.getLingue()
        lingueDD = list(map(lambda x: ft.dropdown.Option(text=x[1], key=x[0]), lingue))
        self.view.ddLingue.options = lingueDD
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




        if mese is None or anno is None or destinazionePrimaria is None or costo is None\
                or mese=="" or anno == '' or destinazionePrimaria == '' or costo == '':
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
        self.view.rowVaiACrea.controls.clear()
        self.view.update_page()
        self.view.contentPrenota.controls.append(self.view.rowVaiACrea)

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

            btnPrenota = ft.ElevatedButton(text="Prenota viaggio", on_click=lambda e: self.prenota(v, [self.view.mesePartenza, self.view.annoPartenza, self.view.ddStati, self.view.ddCategoriaCosto, self.view.colViaggi]))

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

    def prenota(self, viaggio, listaP):
        self.view.tabs.tabs.append(self.tabPrenota)
        self.view.tabs.selected_index = len(self.view.tabs.tabs) -1
        self.tripScelto = viaggio
        self.svuotaParametri(listaP)
        self.view.update_page()

    def creaTab(self):
        self.tabPrenota = ft.Tab(text="Inserisci dati", content=self.creaContenutoTab())



    def autoCompila(self, email):
        if email.value is None or email.value == "":
            self.view.create_alert("Email non inserita")
            return
        campoTraveler = self.model.autoCompila(email.value)
        if len(campoTraveler) > 0:
            self.traveler = campoTraveler[0]
        else:
            self.view.create_alert("Email non presente nel database, compilare a mano")
            return
        self.name.value = self.traveler.name
        self.surname.value = self.traveler.surname
        self.age.value = self.traveler.age
        self.address.value = self.traveler.address
        self.phone.value = self.traveler.phone
        self.gender.value = self.traveler.gender
        self.view.update_page()



    def creaContenutoTab(self):
        # Campo email con bottone Auto-compila in una riga
        self.email = ft.TextField(label="Email", width=300)
        btnAutoCompila = ft.ElevatedButton(text="Auto-compila", on_click=lambda e: self.autoCompila(self.email))
        emailRow = ft.Row(controls=[self.email], alignment=ft.MainAxisAlignment.CENTER)
        autoCompilaRow = ft.Row(controls=[ft.Text("Se hai già prenotato viaggi clicca su \"Auto-compila\" per l'autocompletamento dei dati", color='blue' , size=15) ,btnAutoCompila],
                                alignment=ft.MainAxisAlignment.CENTER)

        # Altri campi di input (Nome, Cognome, Età, etc.)
        self.name = ft.TextField(label="Nome", width=200)
        self.surname = ft.TextField(label="Cognome", width=200)
        self.age = ft.TextField(label="Età", width=100)
        self.studente = ft.Checkbox(label='Studente')
        self.address = ft.TextField(label="Indirizzo", width=400)
        self.phone = ft.TextField(label="Telefono", width=200)

        # Dropdown per gender
        self.gender = ft.Dropdown(
            label="Genere",
            options=[
                ft.dropdown.Option(text='Uomo', key='male'),
                ft.dropdown.Option(text='Donna', key='female'),
                ft.dropdown.Option(text='Altro', key='other')
            ],
            width=200
        )

        # Organizzazione dei campi input in righe
        row1 = ft.Row(controls=[self.name, self.surname], alignment=ft.MainAxisAlignment.CENTER)
        row2 = ft.Row(controls=[self.age, self.studente], alignment=ft.MainAxisAlignment.CENTER)
        row3 = ft.Row(controls=[self.address, self.phone], alignment=ft.MainAxisAlignment.CENTER)
        row4 = ft.Row(controls=[self.gender], alignment=ft.MainAxisAlignment.CENTER)
        row5 = ft.Row(controls=[ft.ElevatedButton(text="Prenota", on_click=lambda e:self.prenotaViaggio([self.email, self.name, self.surname, self.phone, self.address, self.age, self.gender]))], alignment=ft.MainAxisAlignment.CENTER)

        # Creazione della colonna che contiene tutte le righe
        colInput = ft.Column(
            controls=[ft.Container(height=4), emailRow, autoCompilaRow, row1, row2, row3, row4, row5],
            alignment=ft.MainAxisAlignment.START,
            spacing=20  # Aggiungi spazio tra le righe per evitare sovrapposizioni
        )

        return colInput




    def prenotaViaggio(self, listaParametri):
        utentePrenotante = Traveler(self.name.value, self.surname.value, int(self.age.value), self.address.value, self.phone.value, self.email.value, self.gender.value)

        travelerRicercato = self.model.autoCompila(utentePrenotante.email)
        if not travelerRicercato:
            self.model.aggiungiTraveler(self.name.value, self.surname.value, int(self.age.value), self.address.value,
                                       self.phone.value, self.email.value, self.gender.value)


        offerte = self.model.cercaOfferteViaggio(self.tripScelto.trip_package_id, datetime.date.today())
        bestOfferta = None
        if len(offerte)>0:
            offerte.sort(key = lambda x: x.cost)
            if offerte[0].offer_info_category == 'student' and self.studente:
                bestOfferta = offerte[0].offer_id
            elif offerte[0].offer_info_category == 'student' and not self.studente:
                bestOfferta = offerte[1].offer_id
            else:
                bestOfferta = offerte[0].offer_id
        self.dlgPrenotazione = ft.AlertDialog(actions=[ft.TextButton("Chiudi", on_click= self.chiudi_dialog_prenotazione)])

        if self.model.reservation(self.tripScelto.trip_package_id, self.email.value, bestOfferta, self.name.value, self.surname.value, int(self.age.value), self.address.value, self.phone.value, self.gender.value):
            self.dlgPrenotazione.content = ft.Text("Prenotazione avvenuta correttamente!!")
            self.view.page.dialog = self.dlgPrenotazione
            self.dlgPrenotazione.open = True
            self.svuotaParametri(listaParametri)
            self.view.update_page()
        else:
            self.dlgPrenotazione.content = ft.Text("Prenotazione non riuscita!!")
            self.view.page.dialog = self.dlgPrenotazione
            self.dlgPrenotazione.open = True
            self.view.update_page()



    def chiudi_dialog_prenotazione(self, e):
        self.dlgPrenotazione.open = False
        self.view.tabs.selected_index = 0
        self.view.tabs.tabs.pop()

        self.view.update_page()

    def creaViaggio(self, e):
        data = self.view.textDataP.value
        stato1 = self.view.ddCountry1.value
        stato2 = self.view.ddCountry2.value
        stato3 = self.view.ddCountry3.value
        numeroAttr = self.view.numeroAttrazioniMax.value
        lingua = self.view.ddLingue.value
        costoAccomodation = self.view.ddCategoriaCostoCrea.value

        if data == '':
            self.view.create_alert('Data mancante!')
            return
        if stato1 is None:
            self.view.create_alert('Stato 1 mancante!')
            return
        if numeroAttr == '':
            self.view.create_alert('Numero massimo di attrazioni mancante!')
            return
        if lingua is None:
            self.view.create_alert('Lingua visite guidate mancante!')
            return
        if costoAccomodation is None or costoAccomodation == '':
            self.view.create_alert('Costo accomodations mancante!')
            return
        costoAccomodation = int(costoAccomodation)*300

        solBest, costo = self.model.creaViaggio(stato1, stato2, stato3, numeroAttr)
        self.view.colRisultati.controls.clear()
        self.view.update_page()
        destinazioni = list(set(x.nameDest for x in solBest))
        strDestinazioni = ", ".join(destinazioni)
        # attrazioni = [x.nameAtt for x in solBest]
        container = ft.Container(border=ft.border.all(2, "blue"))

        content = ft.Column()
        # Prima riga centrata
        content.controls.append(ft.Row(
            controls=[
                ft.Text("Costo attrazioni: ", weight=ft.FontWeight.BOLD),
                ft.Text(str(costo) + "€"),
                ft.Text("Costo accomodations: ", weight=ft.FontWeight.BOLD),
                ft.Text(str(costoAccomodation) + "€"),
                ft.Text("Destinazioni: ", weight=ft.FontWeight.BOLD),
                ft.Text(strDestinazioni)
            ], alignment=ft.MainAxisAlignment.CENTER))

        # Creazione della colonna per le attrazioni
        colAttraction = ft.Column()
        listaCheckbox = []
        for i in solBest:
            checkBox = ft.Checkbox(label="Visita guidata")
            listaCheckbox.append(checkBox)
            # Righe centrate anche per le attrazioni
            colAttraction.controls.append(ft.Row(
                controls=[ft.Text(i.nameAtt), checkBox], alignment=ft.MainAxisAlignment.CENTER))

        # Aggiunta della colonna delle attrazioni alla riga centrata
        content.controls.append(ft.Row(
            controls=[colAttraction], alignment=ft.MainAxisAlignment.CENTER))

        # Aggiunta del pulsante "Prenota" con riga centrata
        content.controls.append(ft.Row(
            controls=[ft.ElevatedButton(text='Prenota',
                                        on_click=lambda e: self.prenotaViaggioCreato(listaCheckbox, solBest, lingua, costoAccomodation, data))],
            alignment=ft.MainAxisAlignment.CENTER))

        # Aggiunta del container alla view
        container.content = content
        self.view.contentCrea.controls.append(container)

        self.view.update_page()


    def prenotaViaggioCreato(self, listaCheckbox, solBest, lingua, costoAccomodation, data):
        dizioAttrazioni = {}
        costoAttraction = 0
        for i, attr in enumerate(solBest):
            if listaCheckbox[i].value is True:
                resultGuida = self.model.getGuidaLingua(int(lingua))
                costoAttraction += attr.cost * (1+round(int(resultGuida[1]), 2))
            else:
                costoAttraction += attr.cost
        campiData = data.split("-")
        nuovaData = datetime.date(int(campiData[2]), int(campiData[1]), int(campiData[0]))
        id = self.model.creaTripPackage(nuovaData, costoAttraction, costoAccomodation, int(costoAccomodation/300))
        if id is None:
            self.view.create_alert('Inserimento nuovo trip package fallito!!')
            return
        self.prenota(id)


    def svuotaParametri(self, listaParametri):
        for p in listaParametri:
            if isinstance(p, ft.Dropdown):
                p.value = None
            elif isinstance(p, ft.Text) or isinstance(p, ft.TextField):
                p.value = ''
            elif isinstance(p, ft.Column) or isinstance(p, ft.Row):
                p.controls.clear()
        self.view.update_page()

