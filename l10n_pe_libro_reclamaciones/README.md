# Libro de Reclamaciones para Odoo

Este módulo implementa un sistema completo de Libro de Reclamaciones para Odoo, cumpliendo con la normativa peruana. Permite a los clientes registrar reclamos y quejas a través del sitio web, y a la empresa gestionar y dar seguimiento a estos registros desde el backend.

## Características principales

- **Formulario web público** para que los consumidores registren reclamos o quejas, con campos dinámicos según el tipo de consumidor (persona natural, empresa, menor de edad).
- **Gestión interna** de reclamos desde el backend de Odoo: listado, kanban, formulario y búsqueda avanzada.
- **Secuencia automática** para numerar los reclamos.
- **Notificación automática por correo** al consumidor al registrar un reclamo.
- **Configuración desde Ajustes**: secuencia, responsable, mensajes previos y posteriores, plazo de atención.
- **Reporte PDF** del reclamo en formato oficial.
- **Automatización** para el envío de correos de constancia.
- **Soporte multi-compañía** y reglas de acceso para usuarios y público.

## Instalación

1. Copia la carpeta `l10n_pe_libro_reclamaciones` en tu directorio de addons.
2. Instala el módulo desde Apps en Odoo.
3. Configura la secuencia, responsable y mensajes desde Ajustes > Sitio Web > Libro de Reclamaciones.

## Uso

- Los clientes pueden acceder al formulario desde `/libro-reclamaciones` en el sitio web.
- Al enviar el formulario, se valida la información y se crea un registro en Odoo.
- El consumidor recibe un correo de confirmación automáticamente.
- El equipo puede gestionar los reclamos desde el menú **Libro de Reclamaciones** en el backend, cambiando el estado (Nuevo, En proceso, Cancelado, Resuelto) y enviando notificaciones adicionales si es necesario.
- Se puede descargar un PDF oficial del reclamo desde el backend.

## Archivos principales

- `models/libro_reclamaciones.py`: Modelo principal y lógica de negocio.
- `controllers/controllers.py`: Controladores web y validaciones del formulario.
- `templates/libro_reclamaciones.xml`: Plantillas del formulario web y confirmación.
- `report/libro_reclamaciones_template.xml`: Plantilla del reporte PDF.
- `data/mail_template.xml`: Plantilla de correo de confirmación.
- `static/src/js/libro_reclamacion.js`: Lógica JS para campos dependientes en el formulario web.
- `views/views.xml`: Vistas backend (kanban, árbol, formulario, búsqueda).
- `views/res_config_settings.xml`: Configuración en Ajustes.

## Seguridad

- Acceso completo para el grupo "Admin Libro Reclamaciones".
- Acceso de solo lectura y creación para usuarios públicos en el formulario web.
- Reglas multi-compañía incluidas.

## Créditos

Desarrollado por Codlan (Daniel Moreno)