import flet as ft


def main(page):
    # Crea la tab iniziale
    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(text="Tab 1", content=ft.Column(
                controls=[
                    ft.Text("Contenuto della Tab 1"),
                    ft.ElevatedButton(text="Apri Tab Nascosta", on_click=lambda e: mostra_tab_nascosta(e))
                ]
            )),
            ft.Tab(text="Tab 2", content=ft.Text("Contenuto della Tab 2")),
            # La nuova tab verrà aggiunta successivamente
        ],
    )

    # Creazione della tab nascosta
    tab_nascosta = ft.Tab(text="Tab Nascosta", content=ft.Text("Contenuto della Tab Nascosta"))


    # Funzione per mostrare la tab nascosta
    def mostra_tab_nascosta(e):
        # Seleziona la nuova tab (l'ultima aggiunta)
        tabs.tabs.append(tab_nascosta)
        tabs.selected_index = len(tabs.tabs) - 1
        page.update()

    # Aggiungi i controlli alla pagina
    page.controls.append(tabs)

    # Forza l'aggiornamento della pagina
    page.update()


# Esegui l'app
ft.app(target=main)
