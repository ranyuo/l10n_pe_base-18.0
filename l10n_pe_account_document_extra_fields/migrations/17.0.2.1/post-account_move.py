

def migrate(cr, version):
    """
    Hook que se ejecuta después de instalar el módulo.
    """
    # Ejecuta el query solo si el módulo está en proceso de actualización
    cr.execute("""
        UPDATE account_move SET id_mov = id;
    """)
    
    cr.execute("""
        UPDATE account_move_line SET id_mov = id;
    """)
    pass