# 4. Pruebas de presentación y límites observados

## 4.1 Objetivo

Este documento registra la caracterización de la salida de expresiones simbólicas en la fx-CG50 y explica el mecanismo de presentación adaptativa de `Matriz.mostrar()`.

La longitud de una cadena se utiliza como una señal práctica para decidir cuándo compactar la salida. No equivale directamente al consumo de RAM ni establece el límite total de memoria del equipo.

## 4.2 Dos niveles de presentación

La versión actual mantiene dos formatos:

- **Nivel 0:** representación simbólica completa, con separadores `, ` entre columnas y sin espacios de relleno para alinear columnas.
- **Nivel 1:** representación compacta; por ejemplo, `sin(x)` se convierte en `s(x)`, `cos(x)` en `c(x)` y algunos nombres como `theta1` pueden abreviarse como `t1` si no existe ambigüedad.

Las abreviaciones permanecen dentro de la propia expresión; no requieren variables auxiliares definidas aparte.

## 4.3 Umbral configurado

En `casio/matriz.py` está definido:

```python
MAX_FILA_NIVEL0 = 509
```

`Matriz.mostrar()` construye los textos completos y mide la longitud de cada fila. Si alguna fila supera 509 caracteres, se genera la representación compacta de la matriz y se imprime el Nivel 1. Si ninguna fila supera el umbral, se imprime el Nivel 0.

Este valor es un umbral de selección de representación. No es una garantía de memoria libre ni un límite universal del tamaño de toda expresión.

## 4.4 Caracterización experimental anterior

Durante una prueba anterior se observó que una fila de 509 caracteres podía construirse e imprimirse cuatro veces consecutivas sin errores observables, mientras que una fila de 510 caracteres produjo un fallo. También se registró una matriz simbólica `T06` con elementos de hasta aproximadamente 180 caracteres y una fila de aproximadamente 589 caracteres.

La prueba se realizó con una representación que todavía contenía espacios de relleno. Posteriormente cambió el formato para retirar esa alineación. Por eso, la observación 509/510 se conserva como antecedente experimental y no como límite físico absoluto.

## 4.5 Prueba actual de cambio de nivel

El script `testInCasio/pruebasInCasio.py` contiene un grupo que construye una fila de 70 variables `theta` y comprueba que:

- la fila completa supera el umbral del Nivel 0;
- la fila compacta queda por debajo del umbral;
- la matriz puede mostrarse en formato compacto.

El autor confirmó la ejecución de los 24 grupos de pruebas en la fx-CG50. Esta prueba verifica un caso representativo de reducción; no garantiza que todas las expresiones compactas posibles quepan en pantalla.

## 4.6 Reproducción del análisis

El archivo `testInCasio/pruebas_presentacion.py` contiene funciones de diagnóstico para medir la longitud de elementos y filas y para experimentar con cadenas de longitud controlada. Las funciones requieren una matriz creada previamente; por ejemplo, la transformación simbólica `T06`.

Estas funciones son herramientas de diagnóstico manual, no forman parte de la batería automática de `pytest`.

## 4.7 Responsabilidades de los módulos

- `syms.py`: construye, compara y simplifica objetos simbólicos.
- `formato.py`: produce la representación compacta.
- `matriz.py`: decide el nivel que se utiliza y muestra la matriz.

Esta separación permite modificar la salida para la calculadora sin mezclar las decisiones de presentación con el motor algebraico.
