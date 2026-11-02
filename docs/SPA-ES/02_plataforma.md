# 2. Plataforma y compatibilidad

## 2.1 Plataforma objetivo

La plataforma de ejecución principal es la calculadora **Casio fx-CG50**. Los módulos de `casio/` están pensados para copiarse juntos a la carpeta de Python de la calculadora.

## 2.2 Entorno Python

Durante el desarrollo se identificó el entorno Python de la fx-CG50 como una implementación basada en **MicroPython 1.9.4**. No debe suponerse que se comporta exactamente igual que una instalación completa de Python o MicroPython de PC. Algunas funciones, métodos y mecanismos de operadores pueden tener diferencias.

La compatibilidad se considera confirmada cuando la operación se prueba directamente en la calculadora.

## 2.3 Particularidades de operadores

Durante el desarrollo se observaron diferencias en el despacho automático de operadores sobre clases propias. Por ello, para las operaciones matriciales y simbólicas se recomienda utilizar las funciones explícitas del proyecto:

```python
suma(a, b)
resta(a, b)
producto(a, b)
Matriz.p_m(A, B, C)
```

Para la negación simbólica se dispone de `n(expresion)`. Esta interfaz reduce la dependencia de la sobrecarga de operadores en el intérprete de la calculadora.

## 2.4 Símbolos y texto

Los nombres simbólicos se representan preferentemente con caracteres ASCII, por ejemplo `theta1`, `alpha2`, `q1` y `L1`. El módulo `formato.py` puede abreviar nombres de manera controlada en el nivel compacto de presentación.

## 2.5 Convención angular

La convención interna es radianes. Las funciones trigonométricas numéricas utilizan radianes. Utiliza `grados()` para convertir explícitamente un valor en grados antes de pasarlo a una función que espera radianes.

## 2.6 Presentación de matrices

`Matriz.mostrar()` utiliza dos niveles de representación:

- Nivel 0: texto simbólico completo.
- Nivel 1: texto compacto con abreviaciones autocontenidas.

La constante `MAX_FILA_NIVEL0` tiene actualmente el valor 509. Si alguna fila del Nivel 0 supera ese umbral, `mostrar()` construye la representación compacta y presenta la matriz en Nivel 1. Este valor es un umbral interno de selección, no una garantía universal de longitud máxima o memoria disponible.

## 2.7 Caracterización experimental

En pruebas anteriores se observó que una fila de 509 caracteres podía construirse e imprimirse cuatro veces sin errores observables, mientras que una fila de 510 caracteres produjo un fallo en la representación utilizada en esa prueba. También se registraron expresiones de `T06` con elementos de hasta aproximadamente 180 caracteres y una fila de aproximadamente 589 caracteres.

Estos resultados describen pruebas concretas, no el límite absoluto de memoria de la calculadora. La representación se modificó posteriormente para retirar espacios de relleno y seleccionar automáticamente el nivel compacto; por tanto, el resultado histórico 509/510 no debe tratarse como una especificación universal del hardware.

## 2.8 KhiCAS/Xcas

Se exploró de forma independiente KhiCAS para fx-CG50, cuyo entorno incluye MicroPython 1.12 y el módulo `cas` para comunicarse con Xcas. Esta exploración no se encuentra integrada en el núcleo de la versión 1.2. La librería funciona sin importar `cas` ni depender de KhiCAS.

## 2.9 Pruebas por plataforma

- `testInCasio/`: script autocontenido que se ejecuta en la calculadora junto con los módulos de `casio/`. No requiere `pytest`.
- `tests/`: pruebas de escritorio que utilizan `pytest` en Python convencional.
- `.github/workflows/tests.yml`: ejecuta automáticamente la suite de PC en cada `push` y `pull_request`, y también permite iniciarla manualmente desde GitHub Actions.

Una prueba aprobada en PC no demuestra por sí sola compatibilidad con la fx-CG50; por ello se conserva la batería manual.
