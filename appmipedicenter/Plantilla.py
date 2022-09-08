from datetime import *
from appmipedicenter import db
from appmipedicenter.models import Empleado, Hora, Turno, Cliente

class Plantilla:
    def __init__(self, dia):
        self.date = dia
        self.date_str = self.date.strftime("%Y-%m-%d")
        self.cant_col = 1 + 2*(Empleado.query.filter_by(id_tipo=1).count())
        self.cant_fila = 1 + Hora.query.count()
        self.matriz = [] # Matriz 
        self.matriz_podologo = []
        # Seteo de la matriz vacia
        for i in range(0, self.cant_fila):
            self.matriz.append([])
            for j in range(0, self.cant_col):
                self.matriz[i].append([])

        self.matriz[0][0] = "Hora"

        self.__cargar_info()
    
    # Muestra por pantalla toda la informacion almacenada en la matriz
    def mostrar(self):
        for r in range(0, self.cant_fila):
            print(self.matriz[r])

    # Carga la matriz con su respectiva informacion relacionada a la tabla de Hora de la base de datos
    def __cargar_horarios(self):
        lista_horarios = Hora.query.all()
        for i in range(0, Hora.query.count()):
            self.matriz[i+1][0] = lista_horarios[i].hora

    # Carga la matriz con su respectiva informacion relacionada a la tabla Empleado de la base de datos
    def __cargar_podologos(self):
        lista_empleados = Empleado.query.filter_by(id_tipo=1).all() # Empleados que son podologos
        j = 1
        for i in range(0, Empleado.query.filter_by(id_tipo=1).count()):
            self.matriz[0][j] = lista_empleados[i]
            self.matriz[0][j+1] = "Atendido"
            j = j+2

    # Carga la matriz con su respectiva informacion relacionada a la tabla Cliente de la base de datos
    def __cargar_clientes(self):
        lista_turnos_dia = Turno.query.filter_by(date = self.date).all()
        for i in range(0, Turno.query.filter_by(date = self.date).count()):
            
            # Obtener la columna del podologo en espefico
            emp = Empleado.query.filter_by(id = lista_turnos_dia[i].id_empleado).first()
            for j in range(0, self.cant_col):
                if(self.matriz[0][j] == emp):
                    columna = j
            
            # Obtener la fila del horario
            hora = Hora.query.filter_by(id_hora = lista_turnos_dia[i].id_hora).first()
            for j in range(1, self.cant_fila):
                if(self.matriz[j][0] == hora.hora):
                    fila = j

            # Ingresar cliente en su respectivo lugar
            if (lista_turnos_dia[i].disponible == False):
                cliente = "No disponible"
            elif (lista_turnos_dia[i].id_cliente == None):
                self.matriz[fila][columna+1] = ""
                cliente = ""
            else: 
                cliente = Cliente.query.filter_by(id_cliente = lista_turnos_dia[i].id_cliente).first()
                if(lista_turnos_dia[i].atendido):
                    self.matriz[fila][columna+1] = "Si"
                else: 
                    self.matriz[fila][columna+1] = "No"
            
            self.matriz[fila][columna] = cliente

    def __crear_turnos_restantes(self):
        lista_podologos = Empleado.query.filter_by(id_tipo=1).all()
        cant_podologos = Empleado.query.filter_by(id_tipo=1).count()
        cant_horarios =  Hora.query.count()
        for j in range(1, cant_horarios+1):
            for i in range(0, cant_podologos):
                if(Turno.query.filter_by(id_hora = j, id_empleado = lista_podologos[i].id, date = self.date).first() == None):
                    turno = Turno(date = self.date,
                        disponible = True,
                        atendido = False,
                        id_hora = j,
                        id_empleado = lista_podologos[i].id
                        )
                    db.session.add(turno)
                    db.session.commit()
    
    def crear_matriz_podologo(self, podologo):
        # Creacion de matriz podologo
        for i in range(0, self.cant_fila):
            self.matriz_podologo.append([])
            for j in range(0, 3):
                self.matriz_podologo[i].append([])

        # Cargas estaticas
        self.matriz_podologo[0][0] = "Hora"
        self.matriz_podologo[0][1] = podologo
        self.matriz_podologo[0][2] = "Atendido"

        # Carga de horario
        lista_horarios = Hora.query.all()
        for i in range(1, Hora.query.count()+1):
            self.matriz_podologo[i][0] = lista_horarios[i-1].hora

        # Carga de turnos no existentes
        for i in range(1, self.cant_fila):
            if(Turno.query.filter_by(id_hora = i, id_empleado = podologo.id, date = self.date).first() == None):
                turno = Turno(date = self.date,
                    disponible = True,
                    atendido = False,
                    id_hora = i,
                    id_empleado = podologo.id
                )
                db.session.add(turno)
                db.session.commit()

        # Carga de pacientes
        for i in range(1, self.cant_fila):
            turno = Turno.query.filter_by(id_empleado = podologo.id, date = self.date, id_hora = i).first()
            if turno.disponible == False:
                self.matriz_podologo[i][1] = "No disponible"
            elif turno.id_cliente == None:
                self.matriz_podologo[i][1] = ""
                self.matriz_podologo[i][2] = ""
            else:
                cliente = Cliente.query.filter_by(id_cliente = turno.id_cliente).first()
                self.matriz_podologo[i][1] = cliente
                if(turno.atendido):
                    self.matriz_podologo[i][2] = "Si"
                else: 
                    self.matriz_podologo[i][2] = "No"

    #Utiliza las tres funciones anteriores, para setear la matriz con los datos necesarios.
    def __cargar_info(self):
        self.__crear_turnos_restantes()
        self.__cargar_podologos()
        self.__cargar_horarios()
        self.__cargar_clientes()