# Sistema de gestión crediticia

Aplicación local para la Parte 2 del proyecto integrador. Usa Python, Streamlit y SQLite; registra clientes, créditos, cuotas y pagos, calcula operaciones financieras y genera recibos PDF.

## Requisitos

- Python 3.10 o superior
- Paquetes de `requirements.txt`

## Instalación y ejecución

Desde esta carpeta:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

La base `financiera.db` se crea automáticamente junto a `app.py`. En la primera ejecución se cargan cinco clientes ficticios de demostración. Los datos creados en la aplicación persisten localmente en SQLite.

## Flujo para la simulación en aula

1. Seleccionar **Clientes** y crear un cliente en vivo; también se puede buscar y editar un registro.
2. Abrir **Créditos**, elegir un cliente, método francés o alemán, monto, tasa anual y plazo; guardar el crédito para crear sus cuotas.
3. En **Registrar pago**, elegir crédito y cuota, indicar el monto recibido y, si aplica, el cargo manual de mora/comisión.
4. El sistema aplica el pago primero al cargo, después al interés y finalmente al capital; actualiza la cuota, saldo y estado del crédito dentro de una transacción SQLite.
5. Abrir **Recibos** para consultar el comprobante y descargar el PDF.

## Criterios y alcance

- Las tasas de los créditos se ingresan como tasas nominales anuales y se convierten a tasa mensual para el cronograma.
- La calculadora de interés permite escoger una tasa anual y períodos mensuales o anuales.
- Los identificadores DUI se validan por nueve dígitos y NIT por catorce; se acepta captura con o sin guiones.
- Los clientes iniciales y sus documentos son ficticios para demostración.
- El cargo de mora/comisión se captura manualmente porque la guía no define una tasa o regla de mora.
