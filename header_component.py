from nicegui import ui, app

class HeaderComponent:
    def __init__(self):
        self.right_drawer = None

    def render(self):
        with ui.header(elevated=True).style('background-color: #dbc093').classes('items-center justify-between'):
            ui.label('USMA CV-MOOS')
            ui.button(on_click=lambda: self.right_drawer.toggle(), icon='menu').props('flat color=gray')
    


    def set_drawer(self, drawer):
        self.right_drawer = drawer