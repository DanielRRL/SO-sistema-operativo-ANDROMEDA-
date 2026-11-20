"""Despacho de ordenes de la consola hacia los modulos del simulador (T4.1)."""

import archivos
import estadisticas
import hilos_sync
import memoria
import mensajes
import planificador
import procesos
from lexer import tokenizar
from parser import Orden
from procesos import EstadoProceso
from tokens import buscar_definicion, listar_definiciones
from planificador import ResultadoPlanificacion


_COMANDOS_PRINCIPALES = (
    "crear",
    "listar",
    "consultar",
    "finalizar",
    "planificar",
    "estadisticas",
    "concurrencia",
    "mensaje",
    "memoria",
    "archivo",
    "ejemplo",
    "ayuda",
    "tokens",
    "limpiar",
    "salir",
)

_ultimo_resultado: ResultadoPlanificacion | None = None


def _error(error: Exception) -> str:
    """Convierte una excepcion en un mensaje [ERROR] sin datos tecnicos."""
    texto = str(error).strip()
    return f"[ERROR] {texto or 'No se pudo completar la operacion.'}"


def _tabla_procesos(lista: list[procesos.Proceso]) -> str:
    lineas = [
        f"{'PID':>4} {'Nombre':<12} {'Llegada':>7} {'CPU':>4} "
        f"{'Prioridad':>9} {'Memoria':>8} {'Estado':<10}"
    ]
    for proceso in lista:
        lineas.append(
            f"{proceso.pid:>4} {proceso.nombre:<12} {proceso.llegada:>7} "
            f"{proceso.cpu:>4} {proceso.prioridad:>9} {proceso.memoria:>8} "
            f"{proceso.estado.value:<10}"
        )
    return "\n".join(lineas)


def _gantt(resultado: ResultadoPlanificacion) -> str:
    """Arma el Gantt y rellena los huecos de CPU con '(libre)'."""
    partes = []
    tiempo = 0
    for ejecucion in resultado.ejecuciones:
        if ejecucion.inicio > tiempo:
            partes.append(f"[{tiempo}-{ejecucion.inicio}] (libre)")
        partes.append(
            f"[{ejecucion.inicio}-{ejecucion.fin}] {ejecucion.nombre}"
        )
        tiempo = ejecucion.fin
    return "   ".join(partes)


def _comando_crear(orden: Orden) -> str:
    try:
        proceso = procesos.crear_proceso(
            str(orden.argumentos[0]), **orden.atributos
        )
    except ValueError as error:
        return _error(error)

    if proceso.estado is EstadoProceso.RECHAZADO:
        return (
            f"[ERROR] No hay memoria suficiente para el proceso "
            f"'{proceso.nombre}' ({proceso.memoria} MB); quedo Rechazado."
        )
    return (
        f"[OK] Proceso {proceso.pid} '{proceso.nombre}' creado "
        f"en estado {proceso.estado.value}."
    )


def _comando_listar(orden: Orden) -> str:
    lista = procesos.listar_procesos()
    if not lista:
        return "[OK] No hay procesos registrados."
    return "[OK] Procesos registrados:\n" + _tabla_procesos(lista)


def _comando_consultar(orden: Orden) -> str:
    pid = int(orden.argumentos[0])
    proceso = procesos.consultar_proceso(pid)
    if proceso is None:
        return f"[ERROR] No existe el proceso {pid}."
    return f"[OK] Proceso {pid}:\n" + _tabla_procesos([proceso])


def _comando_finalizar(orden: Orden) -> str:
    pid = int(orden.argumentos[0])
    try:
        proceso = procesos.finalizar_proceso(pid)
    except ValueError as error:
        return _error(error)
    if proceso is None:
        return f"[ERROR] No existe el proceso {pid}."
    return f"[OK] Proceso {pid} '{proceso.nombre}' finalizado; memoria liberada."


def _comando_planificar(orden: Orden) -> str:
    global _ultimo_resultado

    quantum = int(orden.atributos.get("quantum", 3))
    try:
        resultado = planificador.planificar(
            procesos.listar_procesos(), str(orden.subcomando), quantum
        )
    except ValueError as error:
        return _error(error)

    _ultimo_resultado = resultado
    if not resultado.ejecuciones:
        return "[OK] No hay procesos en estado LISTO para planificar."

    titulo = f"Gantt {resultado.algoritmo}"
    if resultado.quantum is not None:
        titulo += f" (quantum={resultado.quantum})"
    return (
        f"{titulo}:\n{_gantt(resultado)}\n"
        f"Promedio retorno: {resultado.promedio_retorno:.2f}\n"
        f"Promedio espera:  {resultado.promedio_espera:.2f}"
    )


def _comando_estadisticas(orden: Orden) -> str:
    if _ultimo_resultado is None:
        return "[ERROR] Primero ejecuta 'planificar' para tener estadisticas."
    datos = estadisticas.calcular_estadisticas(_ultimo_resultado)
    return estadisticas.formatear_estadisticas(datos)


def _comando_ejemplo(orden: Orden) -> str:
    global _ultimo_resultado

    lista = procesos.cargar_ejemplo()
    _ultimo_resultado = None
    return (
        f"[OK] Cargados {len(lista)} procesos de ejemplo:\n"
        + _tabla_procesos(lista)
    )


def _comando_memoria(orden: Orden) -> str:
    accion = orden.subcomando
    try:
        if accion == "estado":
            estado = memoria.estado_memoria()
            lineas = [
                f"[OK] Memoria: {estado.total} MB totales, "
                f"{estado.usada} MB usadas, {estado.libre} MB libres."
            ]
            if estado.asignaciones:
                lineas.append("Asignaciones:")
                for pid in sorted(estado.asignaciones):
                    lineas.append(f"  Proceso {pid}: {estado.asignaciones[pid]} MB")
            else:
                lineas.append("Sin asignaciones.")
            return "\n".join(lineas)

        if accion == "asignar":
            pid, mb = int(orden.argumentos[0]), int(orden.argumentos[1])
            if not memoria.reservar(pid, mb):
                return (
                    f"[ERROR] No se pudieron asignar {mb} MB al proceso {pid} "
                    f"(capacidad total {memoria.CAPACIDAD_TOTAL} MB)."
                )
            return f"[OK] Asignados {mb} MB al proceso {pid}."

        if accion == "liberar":
            pid = int(orden.argumentos[0])
            liberados = memoria.liberar(pid)
            if liberados == 0:
                return f"[ERROR] El proceso {pid} no tiene memoria asignada."
            return f"[OK] Liberados {liberados} MB del proceso {pid}."
    except ValueError as error:
        return _error(error)

    return f"[ERROR] Accion de memoria desconocida '{accion}'."


def _comando_archivo(orden: Orden) -> str:
    accion = orden.subcomando
    try:
        if accion == "crear":
            nombre = str(orden.argumentos[0])
            contenido = str(orden.argumentos[1]) if len(orden.argumentos) > 1 else ""
            if archivos.existe_archivo(nombre):
                return (
                    f"[ERROR] Ya existe el archivo '{nombre}'; "
                    "usa 'archivo modificar' para agregar contenido."
                )
            info = archivos.crear_archivo(nombre, contenido)
            return f"[OK] Archivo '{info.nombre}' creado ({info.tamano} bytes)."

        if accion == "listar":
            lista = archivos.listar_archivos()
            if not lista:
                return "[OK] carpeta_pruebas esta vacia."
            lineas = [f"{'Nombre':<24} {'Tamano':>8}"]
            for info in lista:
                lineas.append(f"{info.nombre:<24} {info.tamano:>8}")
            return "[OK] Archivos en carpeta_pruebas:\n" + "\n".join(lineas)

        if accion == "leer":
            nombre = str(orden.argumentos[0])
            contenido = archivos.leer_archivo(nombre)
            if not contenido:
                return f"[OK] El archivo '{nombre}' esta vacio."
            return f"[OK] Contenido de '{nombre}':\n{contenido}"

        if accion == "modificar":
            nombre = str(orden.argumentos[0])
            contenido = str(orden.argumentos[1])
            info = archivos.modificar_archivo(nombre, contenido)
            return f"[OK] Archivo '{info.nombre}' modificado ({info.tamano} bytes)."

        if accion == "eliminar":
            nombre = str(orden.argumentos[0])
            if not archivos.eliminar_archivo(nombre):
                return f"[ERROR] No existe el archivo '{nombre}'."
            return f"[OK] Archivo '{nombre}' eliminado."
    except FileNotFoundError:
        nombre = str(orden.argumentos[0]) if orden.argumentos else "?"
        return f"[ERROR] No existe el archivo '{nombre}'."
    except PermissionError:
        nombre = str(orden.argumentos[0]) if orden.argumentos else "?"
        return f"[ERROR] No hay permisos para operar sobre '{nombre}'."
    except OSError:
        return "[ERROR] No se pudo completar la operacion de archivo."
    except ValueError as error:
        return _error(error)

    return f"[ERROR] Accion de archivo desconocida '{accion}'."


def _comando_concurrencia(orden: Orden) -> str:
    try:
        resultado = hilos_sync.ejecutar_concurrencia(str(orden.subcomando))
    except ValueError as error:
        return _error(error)
    return hilos_sync.formatear_resultado(resultado)


def _comando_mensaje(orden: Orden) -> str:
    if orden.subcomando == "enviar":
        mensajes.enviar(str(orden.argumentos[0]))
        return f"[OK] Mensaje enviado ({mensajes.cantidad()} en cola)."

    texto = mensajes.recibir()
    if texto is None:
        return "[ERROR] No hay mensajes en la cola."
    return f"[OK] Mensaje recibido: {texto}"


def _comando_sin_accion(orden: Orden) -> str:
    if orden.comando == "salir":
        return "[OK] Hasta luego."
    return ""


def ayuda(palabra: str | None = None) -> str:
    """Devuelve la ayuda general o la definicion y ejemplo de una palabra."""
    if palabra is None:
        lineas = ["[OK] Comandos disponibles:"]
        for comando in _COMANDOS_PRINCIPALES:
            definicion = buscar_definicion(comando)
            if definicion is not None:
                lineas.append(
                    f"- {definicion.palabra}: {definicion.definicion} "
                    f"Ejemplo: {definicion.ejemplo}"
                )
        return "\n".join(lineas)

    palabra = palabra.strip()
    definicion = buscar_definicion(palabra)
    if definicion is None:
        return f"[ERROR] No hay ayuda disponible para '{palabra}'."

    return (
        f"[OK] {definicion.palabra} ({definicion.tipo}): "
        f"{definicion.definicion}\n"
        f"Ejemplo: {definicion.ejemplo}"
    )


def mostrar_tokens(texto: str | None = None) -> str:
    """Muestra la tabla de terminales o los tokens de un texto de entrada."""
    if texto is None or not texto.strip():
        lineas = ["[OK] Terminales reconocidos por el lexer:"]
        for definicion in listar_definiciones():
            lineas.append(
                f"{definicion.tipo:<16} {definicion.palabra:<16} "
                f"{definicion.definicion} Ejemplo: {definicion.ejemplo}"
            )
        return "\n".join(lineas)

    reconocidos = tokenizar(texto)
    tiene_error = any(token.tipo == "ERROR" for token in reconocidos)
    prefijo = (
        "[ERROR] Se encontraron caracteres no reconocidos:"
        if tiene_error
        else "[OK] Tokens reconocidos:"
    )
    lineas = [prefijo]
    for token in reconocidos:
        lineas.append(
            f"{token.tipo:<16} {token.lexema!r:<24} "
            f"línea {token.linea}, columna {token.columna}"
        )
    return "\n".join(lineas)


def despachar(orden: Orden) -> str:
    """Ejecuta la orden en el modulo correspondiente y devuelve el texto."""
    comando = orden.comando.lower()

    if comando == "ayuda":
        if len(orden.argumentos) > 1:
            return "[ERROR] Uso: ayuda [comando]."
        palabra = str(orden.argumentos[0]) if orden.argumentos else None
        return ayuda(palabra)

    if comando == "tokens":
        texto = " ".join(str(argumento) for argumento in orden.argumentos)
        return mostrar_tokens(texto)

    manejadores = {
        "crear": _comando_crear,
        "listar": _comando_listar,
        "consultar": _comando_consultar,
        "finalizar": _comando_finalizar,
        "planificar": _comando_planificar,
        "estadisticas": _comando_estadisticas,
        "ejemplo": _comando_ejemplo,
        "memoria": _comando_memoria,
        "archivo": _comando_archivo,
        "concurrencia": _comando_concurrencia,
        "mensaje": _comando_mensaje,
        "limpiar": _comando_sin_accion,
        "salir": _comando_sin_accion,
    }

    manejador = manejadores.get(comando)
    if manejador is None:
        return f"[ERROR] Despacho pendiente para el comando '{orden.comando}'."

    try:
        return manejador(orden)
    except (ValueError, OSError) as error:
        return _error(error)


__all__ = ["ayuda", "despachar", "mostrar_tokens"]
