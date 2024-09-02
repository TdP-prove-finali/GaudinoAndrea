import flet as ft

class View:
    def __init__(self,page=ft.Page):
        super().__init__()
        self.page = page
        self.controller = None





    def load_interface(self):
        pass



    def set_controller(self, controller):
        self.controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def update_page(self):
        self.page.update()