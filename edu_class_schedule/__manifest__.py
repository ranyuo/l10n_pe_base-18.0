{
    'name': 'Registro de horarios de clases',
    'version': '1.0',
    'description': 'Registra horarios de clases para mostrarlos en el sitio web',
    'summary': '',
    'author': 'Christian Bravo',
    'website': '',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'website'
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/edu_academic_period_views.xml",
        "views/edu_career_views.xml",
        "views/edu_class_schedule_views.xml",
        "views/edu_classroom_views.xml",
        "views/edu_course_views.xml",
        "views/menuitem.xml",
        "templates/edu_class_schedule.xml"
    ],
    'auto_install': False,
    'application': False,
    # 'assets': {
        
    # }
}