"""Modelos de datos con Pydantic.

PASO 3: crea este módulo.
- Persona(BaseModel): first_name, last_name, company_name, role_in_company,
  address, email (EmailStr), phone_number. Validar campos no vacíos.
- Solicitud(BaseModel): persona (Persona embebida), tipo_solicitud,
  fecha (date), prioridad (Literal alta/media/baja), identificador,
  descripcion, estado (Literal pendiente/en_proceso/completada).
- Validar fecha desde múltiples formatos de string.
- COLUMNAS_ARCHIVO: lista de las 13 columnas esperadas del archivo.
"""


class Persona:
    """Datos personales mapeables al formulario web. Implementar."""


class Solicitud:
    """Solicitud completa: persona + datos de negocio. Implementar."""
