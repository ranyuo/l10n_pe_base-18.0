# L10N PE EDI Doc - Facturación Electrónica Peruana

## Descripción

Este módulo proporciona una solución completa para la **Facturación Electrónica Peruana**, implementando la generación de documentos XML en formato UBL (Universal Business Language) 2.1 y métodos de recuperación de CDR (Constancia de Recepción) para cumplir con los estándares de SUNAT.

## Características Principales

### 📄 Documentos Electrónicos Soportados
- **Facturas Electrónicas** (Tipo 01)
- **Boletas de Venta** (Tipo 03)
- **Notas de Crédito** (Tipo 07)
- **Notas de Débito** (Tipo 08)
- **Guías de Remisión Electrónicas** (Tipo 09)
- **Documentos de Anulación**
- **Resúmenes Diarios**

### 🏛️ Cumplimiento SUNAT
- **UBL 2.1**: Generación completa de XML en formato UBL
- **Códigos de Impuestos**: Soporte para todos los códigos tributarios peruanos
- **Validaciones**: Cumplimiento estricto de reglas SUNAT
- **CDR**: Recuperación de Constancias de Recepción
- **Catálogos SUNAT**: Implementación de todos los catálogos oficiales

### 💰 Sistema Tributario Peruano
- **IGV** (Impuesto General a las Ventas)
- **ISC** (Impuesto Selectivo al Consumo)
- **ICBPER** (Impuesto a las Bolsas de Plástico)
- **Detracción** (Sistema de Pago de Obligaciones Tributarias)
- **Retención** y **Percepción**
- **Operaciones Gratuitas**

## Estructura del Módulo

### Modelos Principales

#### `account_edi_xml_ubl_pe.py`
- **Función**: Generador principal de XML UBL para documentos electrónicos
- **Características**:
  - Cálculo automático de totales monetarios
  - Manejo de anticipos y propinas
  - Procesamiento de notas con sanitización de caracteres
  - Generación de estructura UBL completa

#### `account_move.py`
- **Función**: Extensión de facturas con funcionalidades peruanas
- **Características**:
  - Validación de RUC para facturas
  - Cálculo de montos por tipo de operación (Gravado, Exonerado, Inafecto, etc.)
  - Vinculación automática con guías de remisión
  - Sistema de detracción completo

#### `stock_picking.py`
- **Función**: Guías de remisión electrónicas
- **Características**:
  - Validación de datos requeridos para GRE
  - Motivos de traslado extendidos
  - Asociación con facturas relacionadas
  - Cumplimiento de formatos SUNAT

### Utilidades

#### `utils/operations.py`
- Validación de RUC peruano
- Operaciones matemáticas básicas
- Utilidades de cálculo

## Dependencias

```python
"depends": [
    "base",
    "base_setup", 
    "sale",
    "account",
    "product",
    "account_edi",
    "l10n_latam_invoice_document",
    "l10n_pe",
    "l10n_pe_edi",
    "l10n_pe_edi_stock",
    "l10n_pe_reports",
    "l10n_pe_reports_stock",
    "l10n_pe_reports_stock_extend",
    "account_edi_ubl_cii",
]
```

## Instalación

1. Asegúrate de tener instalados todos los módulos de dependencia
2. Instala el módulo desde Apps → Localización → Peru
3. Configura los datos de tu empresa (RUC, dirección fiscal)
4. Configura las secuencias de documentos electrónicos

## Configuración

### Configuración de Empresa
1. **Configuración → Empresas → Tu Empresa**
   - RUC (obligatorio)
   - Razón Social
   - Nombre Comercial
   - Dirección Fiscal Completa

### Configuración de Impuestos
1. **Contabilidad → Configuración → Impuestos**
   - Configurar códigos de impuestos SUNAT
   - Definir cuentas contables correspondientes

### Configuración de Productos
1. **Inventario → Productos**
   - Código de producto SUNAT
   - Unidad de medida SUNAT
   - Código de detracción (si aplica)

## Uso

### Generación de Facturas Electrónicas

1. **Crear Factura**:
   ```
   Contabilidad → Clientes → Facturas
   ```

2. **Validaciones Automáticas**:
   - Validación de RUC del cliente (para facturas)
   - Verificación de datos obligatorios
   - Cálculo automático de impuestos

3. **Generación de XML**:
   - Al confirmar la factura se genera automáticamente el XML UBL
   - Estructura completa compatible con SUNAT

### Guías de Remisión Electrónicas

1. **Crear GRE**:
   ```
   Inventario → Operaciones → Transferencias
   ```

2. **Datos Requeridos**:
   - Motivo de traslado
   - Datos del transportista
   - Punto de partida y llegada
   - Documentos relacionados

### Notas de Crédito/Débito

1. **Crear Nota**:
   ```
   Contabilidad → Clientes → Notas de Crédito
   ```

2. **Configuración**:
   - Seleccionar documento de referencia
   - Especificar motivo según catálogo SUNAT
   - Validación automática de datos

## Códigos de Impuestos SUNAT

| Código | Descripción | Uso |
|--------|-------------|-----|
| 1000 | IGV | Operaciones gravadas |
| 9996 | Gratuita | Operaciones gratuitas |
| 9997 | Exonerado | Operaciones exoneradas |
| 9998 | Inafecto | Operaciones inafectas |
| 2000 | ISC | Impuesto selectivo |
| 7152 | ICBPER | Impuesto bolsas plástico |

## Motivos de Traslado (GRE)

- **01**: Venta
- **02**: Compra
- **04**: Traslado entre establecimientos
- **08**: Importación
- **09**: Exportación
- **13**: Otros
- **14**: Venta sujeta a confirmación
- **18**: Traslado emisor itinerante

## Validaciones Implementadas

### Documentos
- ✅ Formato de RUC (11 dígitos)
- ✅ Secuencias de documentos
- ✅ Datos obligatorios SUNAT
- ✅ Límites de caracteres en notas

### Impuestos
- ✅ Códigos de impuestos válidos
- ✅ Cálculos según normativa
- ✅ Detracción por producto/servicio

### UBL
- ✅ Estructura XML válida
- ✅ Esquemas XSD 2.1
- ✅ Catálogos SUNAT actualizados

## Testing y Validación

El módulo incluye herramientas de testing:

### Archivos de Validación
```
tests/
├── ValidaExprRegFactura.xsl
├── test_validacion_factura.py
├── test_validation_invoice_base.py
└── sunat_archivos/
    └── Esquemas XSD y catálogos SUNAT
```

### Ejecutar Tests
```bash
# Tests unitarios
python -m pytest tests/

# Validación XML
python tests/test_validacion_factura.py
```

## Integración con Otros Módulos

### Módulos Compatibles
- **l10n_pe_edi_nubefact**: Envío a Nubefact OSE
- **l10n_pe_pos_base**: Facturación desde POS
- **purchase_report_imports**: Reportes de importación

### APIs Externas
- **SUNAT**: Envío directo (requiere certificado digital)
- **OSE**: Operadores de Servicios Electrónicos
- **API MIGO**: Consulta de contribuyentes

## Resolución de Problemas

### Errores Comunes

1. **Error de RUC Inválido**
   - Verificar formato: 11 dígitos numéricos
   - Validar dígito verificador

2. **XML No Válido**
   - Revisar catálogos SUNAT actualizados
   - Verificar estructura UBL 2.1

3. **Impuestos Incorrectos**
   - Configurar códigos SUNAT correctos
   - Verificar cuentas contables

### Log de Errores
```
Configuración → Técnico → Base de datos → Logging
```

## Soporte

- **Autor**: Daniel Moreno <daniel@codlan.com>
- **Website**: https://www.codlan.com
- **Versión**: 1.0
- **Licencia**: OPL-1

## Contribución

Para contribuir al desarrollo:

1. Fork del repositorio
2. Crear rama de feature
3. Commit de cambios
4. Push a la rama
5. Crear Pull Request

## Changelog

### v1.0
- ✅ Implementación inicial
- ✅ Soporte UBL 2.1
- ✅ Todos los documentos electrónicos
- ✅ Validaciones SUNAT completas
- ✅ Sistema de detracción
- ✅ Guías de remisión electrónicas

---

**Nota**: Este módulo está diseñado específicamente para el mercado peruano y cumple con todas las regulaciones vigentes de SUNAT al momento de su desarrollo.