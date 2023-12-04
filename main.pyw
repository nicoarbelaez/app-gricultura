from tkinter import Button, Frame, Label, Entry, Tk
from PIL import ImageTk, Image
import serial, time
from api import *

class Aplicacion(Frame):

    def __init__(self, master):
        super().__init__(master)

        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=20)
        self.master.rowconfigure(1, weight=1)
        # Marco de pronostico actual y boton
        self.frame = Frame(self.master, bg="#3C3C3C")
        self.frame.grid(columnspan=2, row=0, sticky='nsew', padx=5, pady=5)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=10)
        self.frame.rowconfigure(0, weight=1)
        # Marco de pronostico dias y recomendaciones
        self.frame2 = Frame(self.master, bg="#3C3C3C")
        self.frame2.grid(columnspan=2, row=1, sticky='nsew', padx=5, pady=5)
        self.frame2.columnconfigure(0, weight=1)
        self.frame2.rowconfigure(0, weight=1)
        self.frame2.rowconfigure(1, weight=1)
        self.frame2.rowconfigure(2, weight=1)
        
        self.ps = 'C:\\Users\\arbel\\OneDrive\\Escritorio\\App Argicultura\\imagenes\\'
        self.imagen_icono = ImageTk.PhotoImage(Image.open(f'{self.ps}icono.png'))
        self.imagen_lluvia = ImageTk.PhotoImage(Image.open(f'{self.ps}lluvia.png').resize((50, 50)))
        self.imagen_lluvia_sol = ImageTk.PhotoImage(Image.open(f'{self.ps}lluvia_sol.png').resize((50, 50)))
        self.imagen_neblina = ImageTk.PhotoImage(Image.open(f'{self.ps}neblina.png').resize((50, 50)))
        self.imagen_nublado = ImageTk.PhotoImage(Image.open(f'{self.ps}nublado.png').resize((50, 50)))
        self.imagen_parcialmente_nublado = ImageTk.PhotoImage(Image.open(f'{self.ps}parcialmente_nublado.png').resize((50, 50)))
        self.imagen_soleado = ImageTk.PhotoImage(Image.open(f'{self.ps}soleado.png').resize((50, 50)))
        self.imagen_temp = ImageTk.PhotoImage(Image.open(f'{self.ps}temp.png').resize((50, 50)))
        self.imagen_tormenta = ImageTk.PhotoImage(Image.open(f'{self.ps}tormenta.png').resize((50, 50)))

        self.pronosticos = API()

        puerto = 'COM3'
        # self.sistema()
        try:
            self.arduino = serial.Serial(puerto, 9600)
            self.sistema()
        except:
            texto_error = f"Reconecte el arduino en el puerto {puerto}, y reinicie."
            frame_sistema = Frame(self.frame, bg="#606060")
            frame_sistema.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
            arduino_off = Label(frame_sistema, text=texto_error, bg="red", font="Helvetica 18", fg="white")
            arduino_off.pack()

        self.pronostico_actual()
        self.pronosticos_dias()
    
    def crear_imagenes(self, codigo):
        codigo = int(codigo)
                
        if codigo == 2:            
            return self.imagen_lluvia
        
        elif codigo == 176 or codigo == 353:            
            return self.imagen_lluvia_sol
        
        elif codigo == 2:
            return self.imagen_neblina
        
        elif codigo == 2:
            return self.imagen_nublado
        
        elif codigo == 116:
            return self.imagen_parcialmente_nublado
        
        elif codigo == 113:
            return self.imagen_soleado
        
        elif codigo == 2:
            return self.imagen_temp
        
        else:
            return self.imagen_tormenta
        
    def sistema(self):
        def encender():
            self.arduino.write(b'1')
            time.sleep(1)

        def apagar():
            self.arduino.write(b'0')
            time.sleep(1)
        
        def ciclos():
            # Tiempo
            try: 
                tiempo = int(entrada_tiempo.get()) - 1
            except:
                tiempo = 5
            # Espera
            try:
                espera = int(entrada_espera.get()) - 1
            except:
                espera = 1
            # Ciclos
            try:
                ciclo = int(entrada_ciclos.get())
            except:
                ciclo = 1
            
            i = 1
            
            while True:
                encender()
                time.sleep(tiempo)
                print(f"=====\nTiempo: {tiempo}")
                apagar()

                if ciclo > 1 and i <= ciclo:
                    print(f"Espera: {espera}")
                    print(f"Ciclos: {i}/{ciclo}")
                    i += 1

                    if i == ciclo + 1:
                        print("Salir")
                        break
                    time.sleep(espera)
                else:
                    break                    

        frame_sistema = Frame(self.frame, bg="#606060")
        frame_sistema.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        frame_sistema.columnconfigure(0, weight=1)
        frame_sistema.columnconfigure(1, weight=1)
        frame_sistema.rowconfigure(0, weight=1)
        frame_sistema.rowconfigure(1, weight=1)
        frame_sistema.rowconfigure(2, weight=1)
        frame_sistema.rowconfigure(3, weight=1)
        frame_sistema.rowconfigure(4, weight=1)
        # Tiempo que permanece abierto
        Label(frame_sistema, text="Tiempo (s):  ", font="Helvetica 14", fg="white", bg='#606060', relief='flat').grid(row=0, column=0, sticky='e')
        entrada_tiempo = Entry(frame_sistema)
        entrada_tiempo.grid(row=0, column=1, sticky='w')
        # Tiempo de espera por ciclo
        Label(frame_sistema, text="Espera (s):  ", font="Helvetica 14", fg="white", bg='#606060', relief='flat').grid(row=1, column=0, sticky='e')
        entrada_espera = Entry(frame_sistema)
        entrada_espera.grid(row=1, column=1, sticky='w')
        # Cantidad de ciclos
        Label(frame_sistema, text="Ciclos:  ", font="Helvetica 14", fg="white", bg='#606060', relief='flat').grid(row=2, column=0, sticky='e')
        entrada_ciclos = Entry(frame_sistema)
        entrada_ciclos.grid(row=2, column=1, sticky='w')

        boton_iniciar = Button(frame_sistema, text="Iniciar", font="Helvetica 11", height=2, width=15, command= ciclos)
        boton_iniciar.grid(row=3, column=0, sticky='e')
        boton_parar = Button(frame_sistema, text="Parar", font="Helvetica 11", height=2, width=15, command= apagar)
        boton_parar.grid(row=3, column=1, sticky='w')

        boton_on = Button(frame_sistema, text="Prender", font="Helvetica 11", height=5, width=20, command= encender)
        boton_on.grid(row=4, column=0)
        boton_off = Button(frame_sistema, text="Apagar", font="Helvetica 11", height=5, width=20, command= apagar)
        boton_off.grid(row=4, column=1)

    def pronostico_actual(self):
        print("Mostar pronostico actual")       
        clima, codigo = self.pronosticos.pronostico_actual()
        
        def actualizar_pronostico():
            print("Actualizando...")
            self.pronosticos = API()
            self.pronostico_actual()
            self.pronosticos_dias()

        frame_pronos_actual = Frame(self.frame, bg="#606060")
        frame_pronos_actual.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        frame_pronos_actual.columnconfigure(0, weight=1)
        frame_pronos_actual.columnconfigure(1, weight=1)
        frame_pronos_actual.rowconfigure(0, weight=1)
        frame_pronos_actual.rowconfigure(1, weight=1)
        frame_pronos_actual.rowconfigure(2, weight=1)

        ubicacion_fecha = Label(frame_pronos_actual, text=self.pronosticos.fecha(), bg="#606060", font="Helvetica 11", fg="white")
        ubicacion_fecha.grid(row=0, column=0, sticky='nw', ipadx=2, ipady=2, padx=15, pady=15)
        
        pronostico_actual = Label(frame_pronos_actual, text=clima, bg="#606060", font="Helvetica 12", fg="white")
        pronostico_actual.grid(row=2, column=0, columnspan=2, sticky='n', padx=5, pady=5)
        
        imagen_pronostico = Label(frame_pronos_actual, image=self.crear_imagenes(codigo), bg="#606060")
        imagen_pronostico.grid(row=1, column=0, columnspan=2, sticky='s')

        self.boton_actualizar = Button(frame_pronos_actual, text="ACTUAIZAR", font="Helvetica 10", command=actualizar_pronostico)
        self.boton_actualizar.grid(row=0, column=1, sticky='ne', ipadx=2, ipady=2, padx=15, pady=15)

    def pronosticos_dias(self):
        print("Mostar pronostico de dias")

        for i in range(3):
            frame_dia = Frame(self.frame2, bg="#606060")
            frame_dia.grid(column=0, row=i, sticky='nsew', padx=5, pady=5)
            frame_dia.rowconfigure(0, weight=1)
            frame_dia.rowconfigure(1, weight=8)

            dias = Label(frame_dia, text=self.pronosticos.fecha(i), bg="#606060", font=("Helvetica 8 bold"), fg="white")
            dias.grid(row=0, columnspan=4, sticky='n')

            pos_pronos = 0

            for j in range(3, 8):
                if j != 5:
                    clima, codigo = self.pronosticos.pronostico_dia(i, j)

                    frame_dia.columnconfigure(pos_pronos, weight=1)                    

                    frame_pronosticos = Frame(frame_dia, bg="#606060")
                    frame_pronosticos.grid(column=pos_pronos, row=1, sticky='nsew', padx=3, pady=5)
                    frame_pronosticos.columnconfigure(0, weight=1)
                    frame_pronosticos.columnconfigure(1, weight=1)
                    frame_pronosticos.rowconfigure(0, weight=1)
                    
                    pronostico_hora = Label(frame_pronosticos, text=clima, font=("Helvetica 8"), bg="#606060", fg="white")
                    pronostico_hora.grid(column=1, row=0, sticky='w')

                    imagen_hora = Label(frame_pronosticos, image=self.crear_imagenes(codigo), bg="#606060")
                    imagen_hora.grid(column=0, row=0, sticky='e')

                    pos_pronos += 1

if __name__ == "__main__":
    ventana = Tk()
    ventana.title("Sistema de riego y recolección de agua lluvia")
    ventana.iconbitmap(r'C:\Users\arbel\OneDrive\Escritorio\App Argicultura\icon.ico')
    ventana.configure(bg="#3C3C3C")    
    ventana.minsize(height=600, width=1000)
    ventana.resizable(0, 0)
    # ventana.geometry("1280x650")
    ventana.state("zoomed")
    app = Aplicacion(ventana)
    app.mainloop()
