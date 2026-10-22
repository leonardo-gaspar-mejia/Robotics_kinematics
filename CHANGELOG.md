Changelog

[1.0] - 2026-09-14

Primera versión funcional del núcleo de la Casio Robotics Toolbox.

Añadido

Motor simbólico ligero.

Variables simbólicas mediante Syms.

Expresiones mediante Expresion.

Funciones Sin y Cos.

Clase Potencia.

Suma, resta y multiplicación simbólicas.

Simplificación algebraica básica.

Simplificaciones trigonométricas especializadas.

Evaluación numérica de expresiones.

Clase Matriz.

Suma y resta matricial.

Multiplicación por escalar.

Multiplicación matricial.

Transposición.

Determinante hasta 3x3.

Evaluación numérica de matrices.

Composición mediante Matriz.p_m().

Rotaciones homogéneas Rx, Ry y Rz.

Rotaciones 3x3.

Traslaciones homogéneas.

Composición RPY.

Convención RPY Rz(phi) · Ry(theta) · Rx(psi).

Convención angular en radianes.

Conversión explícita de grados mediante grados().

Presentación matricial sin utilizar str.rjust().

Compatibilidad

Adaptaciones específicas para las limitaciones observadas en la fx-CG50.

Uso de funciones auxiliares para reducir la dependencia del despacho automático de operadores.

Experimental

Pruebas iniciales de integración con KhiCAS MicroPython 1.12.

Acceso experimental al motor Xcas mediante cas.caseval().

La integración con KhiCAS permanece fuera del núcleo estable de la versión 1.0.

[1.1] - 2026-09-26

Segunda versión orientada a mejorar la presentación de matrices simbólicas en la Casio fx-CG50, manteniendo el núcleo matemático de la versión 1.0.

Añadido

Separación de la lógica de presentación simbólica en un módulo independiente formato.py.

Funciones de formato compacto:

_nombre_compacto()

_agregar_nombre_simbolico()

_recoger_nombres_simbolicos()

crear_mapa_compacto()

_compacto_parentesis_suma()

_unir_productos_compactos()

texto_compacto()

Selección automática entre dos niveles de presentación en Matriz.mostrar().

Nivel 0: representación simbólica completa.

Nivel 1: representación simbólica compacta cuando una fila supera el límite de presentación del Nivel 0.

Compactación de funciones trigonométricas:

cos(x) → c(x)

sin(x) → s(x)

Compactación de nombres simbólicos cuando la abreviación es inequívoca, por ejemplo:

theta1 → t1

alpha2 → a2

Protección contra abreviaciones ambiguas.

Eliminación de espacios de relleno y alineación artificial entre columnas para la salida destinada a la Casio, con el objetivo de reducir el ancho horizontal ocupado y evitar desplazamientos innecesarios.

Pruebas específicas para la selección entre Nivel 0 y Nivel 1.

Evidencia experimental

Durante la caracterización de la salida anterior se observó que una fila de 509 caracteres podía ser construida e impresa correctamente.

La misma impresión de 509 caracteres se realizó cuatro veces consecutivas sin errores observables.

Una fila de 510 caracteres produjo un fallo.

Este resultado se conserva como evidencia experimental de la arquitectura previa.

Debido al cambio de formato de salida en la versión 1.1, el umbral de 509 caracteres debe volver a validarse directamente en la fx-CG50 para la nueva representación sin espacios de relleno.

La caracterización previa de T06 registró elementos de hasta aproximadamente 180 caracteres y filas de hasta aproximadamente 589 caracteres en la representación completa anterior.

Arquitectura de presentación

La versión 1.1 mantiene únicamente dos niveles de presentación:

Nivel 0: expresión completa.

Nivel 1: expresión compacta.

No se implementa un tercer nivel de compactación en esta versión. Su necesidad se evaluará únicamente a partir de pruebas reales de uso de la librería en la Casio fx-CG50.

Compatibilidad y diseño

syms.py permanece dedicado al motor simbólico y no contiene la lógica de formato compacto.

matriz.py conserva las operaciones matriciales y decide qué nivel de presentación utilizar.

formato.py concentra las transformaciones necesarias exclusivamente para la representación compacta.

La versión 1.1 mantiene como base las funcionalidades documentadas en la versión 1.0.