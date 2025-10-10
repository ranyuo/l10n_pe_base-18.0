from odoo import http, fields
from odoo.http import request
from datetime import datetime, time
import pytz
import math

class WebsiteClassSchedule(http.Controller):

    @http.route(['/class-schedule', '/class-schedule/page/<int:page>'], type='http', auth="public", website=True)
    def schedule_page(self, page=1, **kwargs):
        # filtros recibidos (pueden ser YYYY-MM-DD o DD/MM/YYYY)
        course_id = kwargs.get('course_id')
        career_id = kwargs.get('career_id')
        date_start = kwargs.get('date_start', '')  # podría llegar '2025-10-09' o '09/10/2025'
        date_end = kwargs.get('date_end', '')

        domain = []
        if course_id:
            try:
                domain.append(('course_id', '=', int(course_id)))
            except Exception:
                pass
        if career_id:
            try:
                domain.append(('career_id', '=', int(career_id)))
            except Exception:
                pass

        # helper: parsear YYYY-MM-DD o DD/MM/YYYY -> datetime.date
        def _parse_to_date(s):
            if not s:
                return None
            for fmt in ('%Y-%m-%d', '%d/%m/%Y'):
                try:
                    return datetime.strptime(s, fmt).date()
                except Exception:
                    continue
            return None

        start_date_obj = _parse_to_date(date_start)
        end_date_obj = _parse_to_date(date_end)

        # Zona horaria del usuario
        user = request.env.user
        user_tz = user.tz or 'UTC'

        if start_date_obj:
            tz = pytz.timezone(user_tz)
            local_start = tz.localize(datetime.combine(start_date_obj, time.min))
            utc_start = local_start.astimezone(pytz.UTC)
            domain.append(('start_class', '>=', fields.Datetime.to_string(utc_start)))

        if end_date_obj:
            tz = pytz.timezone(user_tz)
            local_end = tz.localize(datetime.combine(end_date_obj, time.max))
            utc_end = local_end.astimezone(pytz.UTC)
            domain.append(('start_class', '<=', fields.Datetime.to_string(utc_end)))

        Schedule = request.env['edu.class.schedule'].sudo()
        Course = request.env['edu.course'].sudo()
        Career = request.env['edu.career'].sudo()

        # paginación
        page_size = 10
        total = Schedule.search_count(domain)
        pages = max(1, math.ceil(total / page_size))
        offset = max(0, (page - 1) * page_size)

        schedules = Schedule.search(domain, limit=page_size, offset=offset, order='start_class asc')

        # Formatear resultados: convertir cada datetime a TZ del usuario y formatear dd/mm/yyyy HH:MM
        formatted_schedules = []
        for s in schedules:
            local_start = None
            local_end = None
            try:
                local_start = fields.Datetime.context_timestamp(user, s.start_class)
            except Exception:
                local_start = None
            try:
                local_end = fields.Datetime.context_timestamp(user, s.end_class)
            except Exception:
                local_end = None

            formatted_schedules.append({
                'id': s.id,
                'career': s.career_id.name or '',
                'course': s.course_id.name or '',
                'period': s.academic_period_id.name or '',
                'partner': s.partner_id.name or '',
                'type': s.class_type or '',
                'classroom': s.classroom_id.name or '',
                'link': s.link,
                'start_datetime': local_start.strftime('%d/%m/%Y %H:%M') if local_start else '',
                'end_datetime': local_end.strftime('%d/%m/%Y %H:%M') if local_end else '',
                'duration': s.duration or 0,
                'break': s.break_time or 0
            })

        return request.render("edu_class_schedule.schedule_page", {
            'schedules': formatted_schedules,
            'courses': Course.search([]),
            'careers': Career.search([]),
            'course_id': int(course_id) if course_id else False,
            'career_id': int(career_id) if career_id else False,
            # dejamos los valores tal como llegaron (serán normalizados por JS si es necesario)
            'date_start': date_start or '',
            'date_end': date_end or '',
            'page': page,
            'pages': pages,
            'total': total,
        })
