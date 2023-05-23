from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# carpeta a monitorear:
PATH = "/poner/path/aca"

# Clase creada desde FileSystemEventHandler
# aplico herencia, para sobrescribir el método on_any_event
# así, según el evento, hago alguna acción


def get_filename(path: str) -> str:
    """
    desde un path completo devuelve el nombre del archivo
    """
    return path.split("/")[-1]


class DriveFolderEventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            # si cambios son contra una carpeta y no un archivo, no hago nada:
            return

        if event.event_type == "created":
            print(f"Archivo creado: {get_filename(event.src_path)}")
        elif event.event_type == "modified":
            print(f"Archivo modificado: {get_filename(event.src_path)}")
        elif event.event_type == "deleted":
            print(f"Archivo eliminado: {get_filename(event.src_path)}")


def main():
    # creo instancia de Observer pa el EventHandler
    observer = Observer()
    # creo una instancia de la clase event handler.
    event_handler = DriveFolderEventHandler()

    # acá le digo al observer que asocie el event_handler para ese PATH
    observer.schedule(event_handler, PATH, recursive=True)

    # empiezo a "observar":
    observer.start()

    try:
        # bucle infinito pa mantener la ejecución del programa
        while True:
            sleep(1)  # espera 1 segundo para pasar a la siguiente iteración
    except KeyboardInterrupt:
        # Detiene el observador (cuando presionas Ctrl+C)
        observer.stop()

    # espera a que el observador finalizce por completo:
    observer.join()


if __name__ == "__main__":
    main()
