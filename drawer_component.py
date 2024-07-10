from nicegui import ui, app

class DrawerComponent:
    def render(self):
        with ui.right_drawer(fixed=True).style('background-color: #ebf1fa').props('bordered') as right_drawer:
            ui.button('shutdown', color='gray', on_click=app.shutdown)

        return right_drawer