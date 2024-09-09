import flet as ft

def main(page: ft.Page):

    # Funzione per aprire il dialog
    def apri_dialog(e):
        dialog.open = True  # Apri il dialog
        page.update()  # Aggiorna la pagina per mostrare il dialog

    # Funzione per chiudere il dialog
    def chiudi_dialog(e):
        dialog.open = False  # Chiudi il dialog
        page.update()  # Aggiorna la pagina per nascondere il dialog

    # Crea il contenuto del dialog
    dialog = ft.AlertDialog(
        title=ft.Text("Attenzione"),
        content=ft.Text("Sei sicuro di voler continuare?"),
        actions=[
            ft.TextButton("Annulla", on_click=chiudi_dialog),
            ft.TextButton("Continua", on_click=chiudi_dialog)
        ],
        actions_alignment=ft.MainAxisAlignment.END,  # Pulsanti allineati a destra
    )

    # Aggiungi un pulsante per aprire il dialog
    page.add(ft.ElevatedButton("Mostra dialog", on_click=apri_dialog))

    # Aggiungi il dialog alla pagina
    page.dialog = dialog

ft.app(target=main)
