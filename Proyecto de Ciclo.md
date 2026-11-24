UNIVERSIDAD DE EL SALVADOR

FACULTAD MULTIDISCIPLINARIA DE OCCIDENTE

DEPARTAMENTO DE INGENIERÍA Y ARQUITECTURA

CÁTEDRA: INGENIERÍA ECONÓMICA

## GUÍA INSTRUCCIONAL DEL PROYECTO INTEGRADOR DE CÁTEDRA

PROYECTO: Estudio de Factibilidad Económico-Legal y Desarrollo de un Sistema Digital de Gestión Crediticia mediante IA

## 1. OBJETIVO GENERAL

Evaluar la viabilidad legal, financiera y técnica de la creación de una institución financiera en El Salvador, integrando la formulación de proyectos, la programación asistida por Inteligencia Artificial (Gemini u otra IA) para la gestión de créditos, la producción de material audiovisual explicativo y la simulación operativa en el aula.

## 2. DESGLOSE DETALLADO DE ACTIVIDADES POR PARTE

## PARTE 1: ESTUDIO DE FACTIBILIDAD FINANCIERA Y LEGAL (20% Global) 1.1 Investigación de Figuras Jurídicas en El Salvador

Los equipos analizarán y compararán las cuatro opciones de constitución financiera reguladas en el país:

Persona Natural (Prestamista Comerciante Individual): Registro directo como comerciante individual en el Registro de Comercio (CNR), operando a título personal bajo las disposiciones del Código de Comercio.

Caja de Crédito: Entidad integrada al Sistema FEDECREDITO, normada por la Ley del Sistema Financiero para Fomento del Desarrollo.

Banco Comercial: Sociedad Anónima de capital fijo o variable con el capital social mínimo fijado por la Ley de Bancos y supervisada por la Superintendencia del Sistema Financiero (SSF).

Cooperativa de Ahorro y Crédito (ACACYS): Regulada por el Instituto Salvadoreño de Fomento Cooperativo (INSAFOCOOP) y la Ley de Bancos Cooperativos y Sociedades de Ahorro y Crédito.

## 1.2 Ruta Legal de Constitución (Modelo de Referencia: Cooperativa de Ahorro y Crédito - ACACYS)

Los estudiantes desarrollarán la tramitología paso a paso tomando como modelo una de las figuras (ejemplo: Cooperativa):

- 1. Asamblea de Constitución: Celebración de la asamblea inicial para aprobación de estatutos y elección del comité provisional.

- 2. Personería Jurídica: Tramitación del reconocimiento de personería jurídica e inscripción de estatutos ante el INSAFOCOOP.

- 3. Registros Fiscales: Obtención del Número de Identificación Tributaria (NIT) y Número de Registro de Contribuyente (NRC/IVA) en el Ministerio de Hacienda.


- 4. Registro de Comercio: Inscripción de la escritura de constitución en el Centro Nacional de Registros (CNR) y obtención de la Matrícula de Empresa y Establecimiento.

- 5. Autorización Operativa: Trámite de adecuación y autorización de captación de fondos ante INSAFOCOOP o la Superintendencia del Sistema Financiero (SSF), según el volumen de activos.

## PARTE 2: BASE DE DATOS, SISTEMA INFORMÁTICO Y SIMULACIÓN (40% Global)

## 2.1 Opciones Tecnológicas de Desarrollo Asistido por Inteligencia Artificial (Gemini AI u otra)

Los equipos elegirán una de las siguientes tres arquitecturas tecnológicas para desarrollar su sistema:

| Opción | Arquitectura Base | Generación de Código con Gemini AI | Módulo de Recibos y Salidas |
| --- | --- | --- | --- |
| Opción 1 | Web App Ligera: Google Sheets (BD) + Google Apps Script | Prompts para generar funciones de lógica bancaria (P, i, n), cálculo de tablas y frontend en HTML/CSS mediante Html Service. | Conversión dinámica de plantillas en Google Docs hacia PDF para descarga directa o envío automático por correo. |
| Opción 2 | Plataforma No- Code: Google Sheets (BD) + AppSheet | Prompts para estructurar expresiones en AppSheet (fórmulas de amortización, validaciones de campos y relaciones entre tablas). | Automatización nativa mediante Bots de AppSheet que renderizan recibos en PDF basados en plantillas de Google Docs. |
| Opción 3 | Full-Stack Local / Cloud: SQLite o Supabase (BD) + Python (Streamlit o Flask) | Prompts para construir el código Python completo: conexión a BD, formularios de interfaz visual y motor de cálculo financiero. | Generación de comprobantes PDF dinámicos utilizando librerías Python como ReportLab o pdfkit. |

## 2.2 Módulos Financieros Obligatorios del Sistema

Módulo de Clientes: Captura, modificación y validación de datos (DUI, NIT, dirección, ingresos, perfil crediticio).

## Motor de Cálculos Financieros:

- o Cálculo de operaciones a Interés Simple.

- o Cálculo de operaciones a Interés Compuesto.

- o Generación automatizada de tablas de amortización bajo el Sistema Francés (cuota fija) y Sistema Alemán (amortización constante a capital sobre saldos insolutos).

- Módulo de Comprobantes de Pago (Recibos): Emisión instantánea en pantalla/PDF del comprobante al registrar un pago, detallando: N° de recibo, fecha, cliente, abono a capital, pago de interés, mora/comisión y saldo insoluto restante.

## 2.3 Metodología de la Simulación en el Aula

El día de la entrega, cada alumno instalará o desplegará su sistema en el aula. El docente o el alumno ingresará datos de clientes y solicitudes de crédito (un estimado de 5 clientes) en tiempo real para verificar la capacidad operativa, precisión de cálculos y generación de recibos al instante. Además, se simulará el pago de los clientes


y la generación del correspondiente recibo de pago, lo que conllevará al respectivo descuento en los pagos pendientes del cliente. Esto se debe reflejar en la base de datos de la financiera.

Se recomienda haber ingresado otros clientes de prueba que ya vengan en la base de datos de la financiera.

## PARTE 3: VIDEO DEMOSTRATIVO DE CREACIÓN Y PROGRAMACIÓN CON IA (40% Global)

El alumno grabará un video explicativo en pantalla donde demuestre detalladamente cómo utilizó la Inteligencia Artificial (Gemini u otra IA) y otras herramientas informáticas para construir la base de datos y el software.

## 3.1 Estructura Narrativa del Video

- 1. Presentación (10% del video): Introducción de los integrantes del equipo, materia, proyecto e indicación de la opción tecnológica elegida.

- 2. Explicación del Proceso Técnico (80% del video):

- o Muestra de los prompts iniciales enviados a Gemini AI para crear el esquema de la base de datos y las funciones financieras.

- o Demostración de las iteraciones, errores del código inicial y la depuración con Gemini hasta llegar al código definitivo.

- o Conexión de la interfaz gráfica con la base de datos y prueba de los cálculos de Interés Simple, Compuesto y Amortizaciones.

- 3. Cierre (10% del video): Demostración acelerada de la generación de un recibo y conclusiones técnicas de la integración con IA.

## 3. RÚBRICAS DE EVALUACIÓN DETALLADAS

## PARTE 1: DOCUMENTO DE FACTIBILIDAD Y MEMORIA TÉCNICA (20% Global)

| Criterio | Ponderación Interna | Exigencias Técnicas y Forma de Calificación |
| --- | --- | --- |
| Contenido | 50% | Profundidad técnica en estudio de mercado, marco legal salvadoreño (Persona Natural, Caja de Crédito, Banco, Cooperativa ACACYS), ruta de constitución, corrida financiera a 5 y 10 años (TMAR, VAN, TIR, Periodo de recuperación) y análisis de riesgo. |
| Entrega del Documento | 10% | Puntualidad y entrega en la plataforma oficial en el día y hora programados. (Nota: Si no se entrega el documento, la nota de este rubro es 0% del total, perdiéndose el 20% global). |
| Edición | 20% | Redacción académica formal, coherencia sintáctica, ausencia de errores ortográficos, tipografía uniforme y formato profesional de tablas e ilustraciones. |
| Orden y Estructura | 20% | Requisitos estrictos de presentación: • Mínimo de páginas: 75 páginas de contenido total. • Índices obligatorios: General, de Tablas y de Figuras. |


| Criterio | Ponderación Interna | Exigencias Técnicas y Forma de Calificación |
| --- | --- | --- |
|   |   | • Numeración de páginas: Correlativa con formato académico. • Referencias Bibliográficas: Formato APA (mínimo 15 fuentes regulatorias o académicas). |

## PARTE 2: BASE DE DATOS, SISTEMA INFORMÁTICO Y SIMULACIÓN EN AULA (40% Global)

| Criterio | Ponderación Interna | Exigencias Técnicas y Forma de Calificación |
| --- | --- | --- |
| Documento de Seguimiento de Creación | 20% | Entregable de documento que contenga: 1. Prompts e instrucciones iniciales y finales enviadas a Gemini AI (u otra IA). 2. Código fuente inicial generado vs. Código final depurado. 3. Capturas de pantalla de los modales/formularios creados. 4. Capturas de pantalla del flujo de emisión de recibos. |
| Entrega o Realización | 10% | Presencia del alumno y disposición inmediata del sistema para la simulación en el aula. (Nota: 0% en este rubro si el grupo no realiza la prueba en vivo). |
| Funcionalidad y Recibos | 30% | Operatividad sin fallas durante la simulación en vivo: alta de clientes, asignación de préstamos, persistencia de datos y generación automática e impecable de recibos/comprobantes de pago. |
| Interfaz o Ambiente Gráfico | 20% | Calidad UX/UI: formularios web o modales limpios, navegación intuitiva, validaciones visuales de entrada (DUI, NIT, montos) y usabilidad bancaria profesional. |
| Multifuncionalidad de Cálculos Financieros | 20% | Precisión matemática del sistema en cálculos de Interés Simple, Interés Compuesto y generación de tablas de amortización |


*PARTE 3: VIDEO DEMOSTRATIVO DE CREACIÓN DE BASE DE DATOS Y SISTEMA (40% Global)*

| Criterio | Ponderación Interna | Exigencias Técnicas y Forma de Calificación |
| --- | --- | --- |
| Edición del Video | 30% | Calidad de producción técnica: • Captura de pantalla limpia en alta resolución (mínimo 720p/1080p). • Audio claro, voz nítida, ecualizada y sin ruidos de fondo. • Edición fluida: uso de cortes para eliminar silencios muertes, transiciones dinámicas, acercamientos (zooms) a las líneas de código/prompts clave y textos explicativos en pantalla. |
| Duración del Video | 15% | Mínimo estricto de 8 minutos continuos. (Nota: Videos con duración menor a 8:00 minutos recibirán un descuento proporcional automático en esta casilla). |
| Contenido del Video | 30% | Estructura narrativa requerida: 1. Presentación: Integrante, materia, proyecto y arquitectura elegida. 2. Explicación: Proceso paso a paso de diseño de BD, prompts a Gemini, código generado, errores resueltos y conexión de módulos. 3. Cierre: Prueba de salida funcional (recibo) y conclusiones del desarrollo asistido por IA. |
| Dominio de la Temática y Explicación | 25% | Capacidad expositiva: Fluidez verbal, manejo adecuado de terminología técnica (Ingeniería Económica, estructuras de datos, prompts, amortizaciones), claridad conceptual y solvencia al explicar la integración entre la IA y el código. |

NOTA: Es INDISPENSABLE LA ENTREGA DEL VIDEO para dar validez a las otras partes del proyecto. En caso de no entregarlo, le quedaría un 0% de ponderación a las otras partes.
