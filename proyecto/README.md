# Sistema de gestión crediticia

Aplicación local para la Parte 2 del proyecto integrador. Usa Python, Streamlit y SQLite; registra clientes, créditos, cuotas y pagos, calcula operaciones financieras y genera recibos en pantalla y en PDF.

## Requisitos

- Python 3.10 o superior
- Paquetes: `streamlit` y `reportlab` (listados en `requirements.txt`)

## Instalación y ejecución

Desde esta carpeta:

```bash
python -m venv .venv
# Windows (PowerShell): .venv\Scripts\Activate.ps1
# Windows (cmd):        .venv\Scripts\activate.bat
# Linux/macOS:
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

La base `financiera.db` se crea automáticamente junto a `app.py`. En la primera ejecución se cargan cinco clientes ficticios de demostración (con DUI válidos). Los datos creados en la aplicación persisten localmente en SQLite.

> Si ya tenía una base creada con una versión anterior, no hace falta borrarla: al iniciar, la aplicación corrige automáticamente los tres DUI de demostración antiguos y conserva sus créditos y pagos.

## Estructura

| Archivo | Responsabilidad |
|---|---|
| `app.py` | Interfaz Streamlit: Inicio, Clientes, Calculadora, Créditos, Registrar pago y Recibos |
| `finance.py` | Motor financiero (interés simple y compuesto, amortización francesa y alemana) y validación de DUI, NIT y teléfono |
| `db.py` | Esquema SQLite, datos de demostración y operaciones transaccionales (clientes, créditos, pagos) |
| `receipts.py` | Generación del recibo en PDF (ReportLab) |

## Flujo para la simulación en aula

1. Seleccionar **Clientes** y crear un cliente en vivo; también se puede buscar y editar un registro. Debajo de DUI, NIT y teléfono aparece una validación visual (✔ válido / ✖ motivo) al pulsar Enter o salir del campo.
2. Abrir **Créditos**, elegir un cliente, método francés o alemán, monto, tasa anual y plazo; revisar la vista previa del cronograma y guardar el crédito para crear sus cuotas.
3. En **Registrar pago**, elegir el crédito. La pantalla muestra la próxima cuota a pagar; indicar el monto recibido y, si aplica, el cargo de mora/comisión incluido en ese monto.
4. El sistema aplica el pago primero al cargo, después al interés y finalmente al capital; actualiza la cuota, el saldo y el estado del crédito dentro de una transacción SQLite.
5. El recibo aparece de inmediato en pantalla (N.º de recibo, fecha, cliente, abono a capital, interés, mora/comisión, total recibido y saldo insoluto restante) con botón para descargar el PDF. También puede consultarse después en **Recibos**.

## Validaciones

- **DUI:** 9 dígitos con dígito verificador válido (módulo 10, pesos 9 a 2 sobre los 8 primeros dígitos). Se acepta con o sin guion; no se admiten letras.
- **NIT:** 14 dígitos; los 6 centrales deben ser una fecha real (DDMMAA). Se acepta con o sin guiones. No se verifica el último dígito.
- **Teléfono:** 8 dígitos (formato `7000-0000`).
- **Cliente:** nombre de al menos 3 caracteres, dirección de al menos 5 e ingresos mensuales mayores que cero (máximo $1,000,000). DUI y NIT son únicos.
- **Créditos y calculadora:** tasa entre 0 % y 100 %, capital hasta $10,000,000 y plazo de 1 a 360 meses.
- **Pagos:** el monto debe ser positivo; la mora/comisión no puede superar el monto recibido; el pago no puede exceder el saldo de la cuota; la fecha no puede ser futura; las cuotas se pagan en orden (no se puede pagar una cuota si hay otra anterior pendiente).
- Los errores de datos y de base de datos se muestran como mensajes en pantalla, no como trazas.

## Criterios financieros

- Las tasas de los créditos se ingresan como tasas nominales anuales y se convierten a tasa mensual (`tasa anual / 12`) para el cronograma.
- **Interés simple:** `I = P · i · n`, con `i = tasa anual / períodos por año`.
- **Interés compuesto:** `F = P · (1 + i)^n`, con la misma `i` (capitalización por período). El número de períodos debe ser entero.
- **Sistema francés:** cuota fija `C = P · i / (1 − (1 + i)^−n)`; el interés de cada cuota se calcula sobre el saldo insoluto.
- **Sistema alemán:** amortización constante a capital (`P / n`) con interés sobre el saldo insoluto, por lo que la cuota decrece.
- Todos los cálculos usan `Decimal` y se redondean al centavo (mitad hacia arriba); la última cuota cancela el saldo exacto y absorbe el residuo de redondeo. Los montos se almacenan en centavos (enteros).
- La calculadora permite escoger tasa anual y períodos mensuales o anuales.

## Pagos y base de datos

- Cada pago se registra en una transacción con bloqueo de escritura (`BEGIN IMMEDIATE`): dos sesiones no pueden aplicar el mismo saldo dos veces.
- El N.º de recibo tiene el formato `REC-AAAAMMDD-#####` y se deriva del identificador del pago, por lo que es único.
- El crédito pasa a estado **Cancelado** cuando no queda capital ni interés pendiente.
- Al crear un crédito se verifica que el cronograma coincida con el plazo y que la suma de capital cuadre con el monto.

## Alcance y limitaciones

- Los clientes iniciales y sus documentos son ficticios para demostración.
- El cargo de mora/comisión se captura manualmente porque la guía no define una tasa o regla de mora; no se calcula automáticamente ni existe un estado "En mora".
- El interés de cada cuota es el del cronograma original: no se recalcula por pagos anticipados o tardíos, y no se admite abonar un excedente a cuotas posteriores en el mismo pago.
- El PDF usa Helvetica (Latin-1): soporta acentos y ñ, pero no caracteres fuera de ese conjunto.
- Aplicación de un solo usuario con almacenamiento local en SQLite; no incluye autenticación.