# Ventas - Campo Vendedor

## Descripción

Este módulo agrega funcionalidad para gestionar un campo de vendedor personalizado en las órdenes de venta y facturas de Odoo. Permite asignar un vendedor específico a cada transacción comercial y facilita el seguimiento y reporting de ventas por vendedor.

## Características

### 🚀 Funcionalidades Principales

- **Campo Vendedor en Órdenes de Venta**: Agrega un campo `salesman_id` en las órdenes de venta para asignar un vendedor específico
- **Campo Vendedor en Facturas**: Extiende las facturas (`account.move`) con el mismo campo de vendedor
- **Integración con Reportes**: Los datos del vendedor se incluyen automáticamente en los reportes mediante el método `data_report()`
- **Validación de Dominio**: Solo permite seleccionar contactos marcados como vendedores (`is_salesman = True`)

### 📋 Modelos Extendidos

- **`sale.order`**: Orden de Venta
- **`account.move`**: Factura/Asiento Contable
- **`res.partner`**: Contacto (para gestionar vendedores)

### 🎨 Vistas Personalizadas

- Formulario de orden de venta con campo vendedor
- Formulario de factura con campo vendedor  
- Vista de contacto con opciones de vendedor

## Instalación

### Dependencias

Este módulo requiere los siguientes módulos de Odoo:

- `base` - Módulo base de Odoo
- `sale` - Gestión de ventas
- `sale_management` - Gestión avanzada de ventas
- `external_layout_header_compact` - Layout compacto para reportes

### Pasos de Instalación

1. Copiar el módulo en el directorio de addons de Odoo
2. Actualizar la lista de módulos disponibles
3. Instalar el módulo desde la interfaz de Odoo o mediante línea de comandos

```bash
# Actualizar lista de módulos
odoo-bin -u all -d nombre_base_datos

# Instalar módulo
odoo-bin -i sale_salesman -d nombre_base_datos
```

## Configuración

### Configurar Vendedores

1. Ir a **Contactos** > **Contactos**
2. Seleccionar o crear un contacto
3. Marcar la casilla **"Es Vendedor"** en la configuración del contacto
4. Guardar los cambios

### Asignar Vendedores

#### En Órdenes de Venta:
1. Crear o editar una orden de venta
2. En la sección **"Detalles del Pedido"**, seleccionar el vendedor en el campo **"Vendedor"**
3. Solo aparecerán contactos marcados como vendedores

#### En Facturas:
1. Crear o editar una factura
2. Seleccionar el vendedor correspondiente en el campo **"Vendedor"**

## Uso

### Datos Disponibles en Reportes

El módulo proporciona los siguientes datos del vendedor en los reportes:

- `salesman_name`: Nombre del vendedor
- `salesman_email`: Email del vendedor
- `salesman_mobile`: Teléfono móvil del vendedor

### Ejemplo de Uso en Reportes

```python
# Los datos están disponibles automáticamente en data_report()
def custom_report_data(self):
    data = self.data_report()
    vendedor = data.get('salesman_name', 'Sin asignar')
    email = data.get('salesman_email', '')
    telefono = data.get('salesman_mobile', '')
```

## Estructura del Módulo

```
sale_salesman/
├── __init__.py
├── __manifest__.py
├── README.md
├── models/
│   ├── __init__.py
│   ├── sale_order.py      # Extensión del modelo de órdenes de venta
│   ├── account_move.py    # Extensión del modelo de facturas
│   └── res_partner.py     # Extensión del modelo de contactos
└── views/
    ├── sale_order.xml     # Vista del formulario de orden de venta
    ├── account_move.xml   # Vista del formulario de factura
    └── res_partner.xml    # Vista del formulario de contacto
```

## Compatibilidad

- **Versión de Odoo**: 18.0
- **Python**: 3.8+
- **Base de Datos**: PostgreSQL

## Soporte

Para soporte técnico o reportar problemas:

- **Autor**: Daniel Moreno
- **Email**: daniel@codlan.com
- **Empresa**: Codlan Labs

## Licencia

Este módulo se distribuye bajo la licencia LGPL-3.

---

**Desarrollado por [Codlan Labs](mailto:daniel@codlan.com)**
