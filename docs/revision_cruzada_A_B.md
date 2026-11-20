# Revisión cruzada A → B

- **Tarea:** T5.5
- **Fase:** 5. Pruebas
- **Revisor:** Persona A
- **Revisado:** Persona B
- **Alcance:** lexer, tokens, memoria, archivos y documentación de B
- **Estado:** Aprobado sin cambios bloqueantes

## 1. Archivos revisados

- `tokens.py`
- `lexer.py`
- `memoria.py`
- `archivos.py`
- `pruebas/test_lexer.py`
- `pruebas/test_persona_b.py`
- `docs/anexo_especificacion_lexica.md`
- `README.md`

## 2. Checklist de revisión

| Aspecto | Resultado |
|---|---|
| Solo biblioteca estándar | Correcto: `re`, `dataclasses`, `pathlib`, `unittest`, etc. |
| Sin dependencias externas | Correcto. |
| Tabla de 36 palabras reservadas | Correcta y centralizada en `tokens.py`. |
| Tokens `ID`, `NOMBRE_ARCHIVO`, `NUMERO`, `CADENA`, `IGUAL`, `FIN`, `ERROR` | Correctos. |
| Cadenas con escapes y comillas sin cerrar | Correcto: se reportan como `ERROR` sin detener el resto. |
| Línea y columna | Correctas y probadas. |
| Comentarios `#` | Correctos, incluso con `#` dentro de cadenas. |
| Memoria de 1024 MB | Correcta: reserva, rechazo por capacidad, liberación y reinicio. |
| Validación de pid/cantidad | Correcta. |
| Archivos solo en `carpeta_pruebas/` | Correcto: rechaza rutas absolutas, `..`, separadores y enlaces. |
| Nombres reservados en archivos | Rechazados correctamente. |
| Crear sin sobrescribir | Correcto: usa modo `x`. |
| Leer/modificar archivo inexistente | `FileNotFoundError` controlado. |
| Anexo léxico y README | Coherentes con lexer, tokens y parser. |
| Pruebas de B | 44 pruebas ejecutadas: correctas. |
| Integración con parser, consola y main | Correcta; la suite completa pasa. |

## 3. Evidencia de pruebas

```bash
python3 -m unittest pruebas.test_lexer pruebas.test_persona_b -v
```

Resultado: **44 tests OK**.

```bash
python3 -m unittest discover -s pruebas -v
```

Resultado: **155 tests OK**.

## 4. Observaciones

No se encontraron defectos bloqueantes. La API de archivos exige nombres
seguros y el parser restringe los comandos de archivo a nombres con extensión;
el módulo mantiene además su propia validación de rutas. No se solicitaron
cambios a B.

## 5. Conclusión

La revisión A → B queda aprobada. Para cerrar T5.5 como equipo faltan las
revisiones B → C, C → D y D → A; después C puede congelar la versión en T5.6.
