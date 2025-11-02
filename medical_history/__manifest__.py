{
    "name": "Medical Clinical History",
    "summary": "Gestión de historias clínicas con formularios detallados de hospitalización",
    "version": "18.0.1.0.0",
    "category": "Medical",
    "license": "LGPL-3",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/medical_history_views.xml",
        "views/medical_history_menus.xml",
    ],
    "installable": True,
    "application": True,
}
