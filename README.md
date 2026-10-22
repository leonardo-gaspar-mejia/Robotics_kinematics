# Casio Robotics Toolbox

**Versión 1.0**

Toolbox ligera de matemáticas y robótica desarrollada para la **Casio fx-CG50**, inspirada en la toolbox del Dr. César Chávez.

## Objetivo

Proporcionar una herramienta compacta para realizar operaciones matemáticas utilizadas en robótica, especialmente:

- álgebra matricial;
- transformaciones espaciales;
- rotaciones;
- traslaciones;
- transformaciones homogéneas;
- representación RPY;
- operaciones simbólicas especializadas.

La toolbox está diseñada específicamente para las restricciones de la fx-CG50 y no pretende ser un CAS general.

## Versión 1.0

La primera versión funcional incluye:

- variables simbólicas (`Syms`);
- expresiones simbólicas (`Expresion`);
- seno y coseno simbólicos;
- potencias;
- suma, resta y multiplicación simbólicas;
- simplificación algebraica y trigonométrica básica;
- evaluación numérica;
- matrices numéricas y simbólicas;
- suma y resta de matrices;
- multiplicación por escalar;
- multiplicación matricial;
- transposición;
- determinante hasta 3x3;
- rotaciones Rx, Ry y Rz;
- rotaciones 3x3;
- traslaciones homogéneas;
- composición de múltiples matrices;
- RPY mediante `Rz(phi) · Ry(theta) · Rx(psi)`;
- presentación de matrices compatible con la fx-CG50.

## Convención angular

Los ángulos se interpretan en **radianes** por defecto.

Para convertir grados a radianes:

```python
from syms import grados

angulo = grados(45)
```

## Estructura

```text
Robotics_Toolbox_MicroPython/
│
├── casio/
│   ├── syms.py
│   ├── matriz.py
│   ├── rot.py
│   ├── ejemplo_uso.py
│   └── Pruebas KhiCAS/
│       └── ejemplo_uso2.py
│
├── docs/
│   ├── 01_objetivos.md
│   ├── 02_plataforma.md
│   └── 03_arquitectura.md
│
└── README.md
```

## Plataforma

Plataforma principal:

**Casio fx-CG50**

El núcleo de la versión 1.0 está pensado para el entorno MicroPython de la calculadora.

## KhiCAS

Durante el desarrollo se realizó una prueba independiente con **KhiCAS para fx-CG50**. Su entorno MicroPython 1.12 permite acceder al motor Xcas mediante el módulo `cas` y `cas.caseval()`.

Esta integración es experimental y no forma parte del núcleo de la versión 1.0. Se mantiene separada para evaluar posteriormente el uso de Xcas como motor simbólico avanzado.

## Filosofía del proyecto

La toolbox busca ser:

- ligera;
- clara;
- modular;
- portable;
- especializada en robótica;
- compatible con las limitaciones reales de la calculadora.

No se busca implementar un CAS completo cuando una solución específica y ligera sea suficiente.

## Estado

**Versión 1.0 — núcleo funcional.**

Las futuras versiones podrán ampliar las capacidades matemáticas o incorporar una interfaz opcional con motores simbólicos externos, sin comprometer el núcleo ligero del proyecto.
