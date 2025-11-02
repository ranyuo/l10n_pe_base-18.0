from odoo import api, fields, models


class MedicalDocumentType(models.Model):
    _name = "medical.document.type"
    _description = "Tipo de Documento Médico"

    name = fields.Char(required=True)
    code = fields.Char()

    _sql_constraints = [
        ("medical_document_type_name_unique", "unique(name)", "El nombre del tipo de documento debe ser único."),
    ]


class MedicalInsuranceType(models.Model):
    _name = "medical.insurance.type"
    _description = "Tipo de Seguro Médico"

    name = fields.Char(required=True)
    code = fields.Char()

    _sql_constraints = [
        ("medical_insurance_type_name_unique", "unique(name)", "El nombre del tipo de seguro debe ser único."),
    ]


class MedicalBloodGroup(models.Model):
    _name = "medical.blood.group"
    _description = "Grupo Sanguíneo"

    name = fields.Char(required=True)

    _sql_constraints = [
        ("medical_blood_group_name_unique", "unique(name)", "El grupo sanguíneo debe ser único."),
    ]


class MedicalRhFactor(models.Model):
    _name = "medical.rh.factor"
    _description = "Factor RH"

    name = fields.Char(required=True)

    _sql_constraints = [
        ("medical_rh_factor_name_unique", "unique(name)", "El factor RH debe ser único."),
    ]


class MedicalCivilStatus(models.Model):
    _name = "medical.civil.status"
    _description = "Estado Civil"

    name = fields.Char(required=True)

    _sql_constraints = [
        ("medical_civil_status_name_unique", "unique(name)", "El estado civil debe ser único."),
    ]


class MedicalEthnicity(models.Model):
    _name = "medical.ethnicity"
    _description = "Grupo Étnico"

    name = fields.Char(required=True)

    _sql_constraints = [
        ("medical_ethnicity_name_unique", "unique(name)", "El grupo étnico debe ser único."),
    ]


class MedicalEducationLevel(models.Model):
    _name = "medical.education.level"
    _description = "Grado de Instrucción"

    name = fields.Char(required=True)

    _sql_constraints = [
        ("medical_education_level_name_unique", "unique(name)", "El grado de instrucción debe ser único."),
    ]


class MedicalReligion(models.Model):
    _name = "medical.religion"
    _description = "Religión"

    name = fields.Char(required=True)

    _sql_constraints = [
        ("medical_religion_name_unique", "unique(name)", "La religión debe ser única."),
    ]


class MedicalOccupation(models.Model):
    _name = "medical.occupation"
    _description = "Ocupación"

    name = fields.Char(required=True)

    _sql_constraints = [
        ("medical_occupation_name_unique", "unique(name)", "La ocupación debe ser única."),
    ]


class MedicalLocation(models.Model):
    _name = "medical.location"
    _description = "Ubicación Geográfica"

    name = fields.Char(required=True)
    type = fields.Selection(
        selection=[
            ("department", "Departamento"),
            ("province", "Provincia"),
            ("district", "Distrito"),
        ],
        required=True,
    )
    code = fields.Char()

    _sql_constraints = [
        (
            "medical_location_name_type_unique",
            "unique(name, type)",
            "El nombre de la ubicación debe ser único para cada tipo.",
        ),
    ]


class MedicalBiologicalState(models.Model):
    _name = "medical.biological.state"
    _description = "Estado de Función Biológica"

    function = fields.Selection(
        selection=[
            ("sleep", "Sueño"),
            ("appetite", "Apetito"),
            ("thirst", "Sed"),
            ("urine", "Orina"),
            ("stool", "Deposiciones"),
        ],
        required=True,
    )
    name = fields.Char(required=True)
    description = fields.Char()

    _sql_constraints = [
        (
            "medical_biological_state_unique",
            "unique(function, name)",
            "Cada estado de función biológica debe ser único por función.",
        ),
    ]


class MedicalDiseaseCourse(models.Model):
    _name = "medical.disease.course"
    _description = "Curso de la Enfermedad"

    name = fields.Char(required=True)
    description = fields.Char()

    _sql_constraints = [
        ("medical_disease_course_unique", "unique(name)", "El curso de la enfermedad debe ser único."),
    ]


class MedicalClinicalHistory(models.Model):
    _name = "medical.clinical.history"
    _description = "Historia Clínica"

    name = fields.Char(compute="_compute_name", store=True)
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Compañía",
        required=True,
        default=lambda self: self.env.company.id,
    )

    paternal_last_name = fields.Char(string="Apellido Paterno", required=True)
    maternal_last_name = fields.Char(string="Apellido Materno", required=True)
    given_names = fields.Char(string="Nombres", required=True)
    document_type_id = fields.Many2one(
        comodel_name="medical.document.type",
        string="Tipo de Documento",
        required=True,
    )
    document_number = fields.Char(string="Nº de Documento", required=True)
    insurance_type_id = fields.Many2one(
        comodel_name="medical.insurance.type",
        string="Tipo de Seguro",
    )
    insurance_number = fields.Char(string="Nº de Seguro")
    blood_group_id = fields.Many2one(
        comodel_name="medical.blood.group",
        string="Grupo Sanguíneo",
    )
    rh_factor_id = fields.Many2one(
        comodel_name="medical.rh.factor",
        string="Factor RH",
    )
    evaluation_date = fields.Date(string="Fecha de Evaluación")
    evaluation_time = fields.Float(string="Hora", help="Registre la hora en formato 24 horas (por ejemplo 13.5 para 13:30).")
    birth_date = fields.Date(string="Fecha de Nacimiento")
    age_years = fields.Integer(string="Edad (Años)")
    age_months = fields.Integer(string="Edad (Meses)")
    age_days = fields.Integer(string="Edad (Días)")
    sex = fields.Selection(
        selection=[
            ("male", "Masculino"),
            ("female", "Femenino"),
            ("other", "Otro"),
        ],
        string="Sexo",
    )
    civil_status_id = fields.Many2one("medical.civil.status", string="Estado Civil")
    ethnicity_id = fields.Many2one("medical.ethnicity", string="Raza / Grupo Étnico")
    education_level_id = fields.Many2one("medical.education.level", string="Grado de Instrucción")
    religion_id = fields.Many2one("medical.religion", string="Religión")
    occupation_id = fields.Many2one("medical.occupation", string="Ocupación")
    birth_department_id = fields.Many2one(
        "medical.location",
        string="Departamento de Nacimiento",
        domain="[('type', '=', 'department')]",
    )
    birth_province_id = fields.Many2one(
        "medical.location",
        string="Provincia de Nacimiento",
        domain="[('type', '=', 'province')]",
    )
    birth_district_id = fields.Many2one(
        "medical.location",
        string="Distrito de Nacimiento",
        domain="[('type', '=', 'district')]",
    )
    residence_department_id = fields.Many2one(
        "medical.location",
        string="Departamento de Residencia",
        domain="[('type', '=', 'department')]",
    )
    residence_province_id = fields.Many2one(
        "medical.location",
        string="Provincia de Residencia",
        domain="[('type', '=', 'province')]",
    )
    residence_district_id = fields.Many2one(
        "medical.location",
        string="Distrito de Residencia",
        domain="[('type', '=', 'district')]",
    )
    address = fields.Char(string="Dirección")
    phone = fields.Char(string="Teléfono")
    mobile = fields.Char(string="Celular")

    father_name = fields.Char(string="Nombre del Padre")
    father_age = fields.Integer(string="Edad del Padre")
    father_education_level_id = fields.Many2one(
        "medical.education.level",
        string="Grado de Instrucción del Padre",
    )
    father_occupation_id = fields.Many2one(
        "medical.occupation",
        string="Ocupación del Padre",
    )
    mother_name = fields.Char(string="Nombre de la Madre")
    mother_age = fields.Integer(string="Edad de la Madre")
    mother_education_level_id = fields.Many2one(
        "medical.education.level",
        string="Grado de Instrucción de la Madre",
    )
    mother_occupation_id = fields.Many2one(
        "medical.occupation",
        string="Ocupación de la Madre",
    )
    spouse_name = fields.Char(string="Nombre del Cónyuge")
    spouse_age = fields.Integer(string="Edad del Cónyuge")
    spouse_education_level_id = fields.Many2one(
        "medical.education.level",
        string="Grado de Instrucción del Cónyuge",
    )
    spouse_occupation_id = fields.Many2one(
        "medical.occupation",
        string="Ocupación del Cónyuge",
    )
    responsible_name = fields.Char(string="Nombre del Responsable")
    responsible_document = fields.Char(string="Documento del Responsable")
    responsible_phone = fields.Char(string="Teléfono del Responsable")

    disease_duration = fields.Char(string="Tiempo de Enfermedad")
    disease_course_id = fields.Many2one(
        "medical.disease.course",
        string="Curso",
    )
    main_symptoms = fields.Text(string="Signos y Síntomas Principales")
    related_story = fields.Text(string="Relato (Descripción del problema actual)")
    previous_auxiliary_tests = fields.Text(string="Exámenes Auxiliares Previos")
    previous_auxiliary_results = fields.Text(string="Resultados de Exámenes Previos")
    previous_treatment = fields.Text(string="Tratamiento Recibido")

    sleep_state_id = fields.Many2one(
        "medical.biological.state",
        string="Sueño",
        domain="[('function', '=', 'sleep')]",
    )
    appetite_state_id = fields.Many2one(
        "medical.biological.state",
        string="Apetito",
        domain="[('function', '=', 'appetite')]",
    )
    thirst_state_id = fields.Many2one(
        "medical.biological.state",
        string="Sed",
        domain="[('function', '=', 'thirst')]",
    )
    urine_state_id = fields.Many2one(
        "medical.biological.state",
        string="Orina",
        domain="[('function', '=', 'urine')]",
    )
    stool_state_id = fields.Many2one(
        "medical.biological.state",
        string="Deposiciones",
        domain="[('function', '=', 'stool')]",
    )
    notes = fields.Text(string="Observaciones")

    @api.depends("paternal_last_name", "maternal_last_name", "given_names")
    def _compute_name(self):
        for record in self:
            parts = [record.paternal_last_name or "", record.maternal_last_name or "", record.given_names or ""]
            record.name = " ".join(filter(None, (part.strip() for part in parts)))

    @api.onchange("birth_date")
    def _onchange_birth_date(self):
        for record in self:
            if record.birth_date and record.evaluation_date:
                record._compute_age()

    @api.onchange("evaluation_date")
    def _onchange_evaluation_date(self):
        for record in self:
            if record.birth_date and record.evaluation_date:
                record._compute_age()

    def _compute_age(self):
        for record in self:
            if not record.birth_date or not record.evaluation_date:
                continue
            birth = fields.Date.to_date(record.birth_date)
            evaluation = fields.Date.to_date(record.evaluation_date)
            delta = evaluation - birth
            if delta.days < 0:
                record.age_years = record.age_months = record.age_days = 0
                continue
            years = delta.days // 365
            remaining_days = delta.days % 365
            months = remaining_days // 30
            days = remaining_days % 30
            record.age_years = years
            record.age_months = months
            record.age_days = days
