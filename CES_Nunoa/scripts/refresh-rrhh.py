"""Generar el panel semanal de RRHH a partir de registros verificados y mínimos.

Uso: python scripts/refresh-rrhh.py /ruta/absoluta/hacia/verified-rrhh.json
Entrada: {verifiedAt: marca de tiempo ISO, sourceUrl: URL verificada de Drive,
        records: [{name,event,start,end,area?}]}.
Lee ingresosBeneficio y Licencias completamente antes de ejecutar. Las fechas son ISO.
No incluyas RUT, detalles médicos, contactos o campos de personal no relacionados.
"""
import json
import sys
from datetime import date, datetime, timedelta
from html import escape
from pathlib import Path
from zoneinfo import ZoneInfo

def week_bounds(day):
    # Calcula el inicio (lunes) y el fin (domingo) de la semana para una fecha dada
    start = day - timedelta(days=day.weekday())
    return start, start + timedelta(days=6)

def render(data):
    # Procesa los datos y genera el código HTML para el panel semanal de RRHH
    checked = datetime.fromisoformat(data['verifiedAt'].replace('Z', '+00:00')).astimezone(ZoneInfo('America/Santiago'))
    start, end = week_bounds(checked.date())
    records, seen = [], set()
    for record in data['records']:
        a, b = date.fromisoformat(record['start']), date.fromisoformat(record['end'])
        if b < a:
            raise ValueError('Intervalo de fecha inválido')
        key = tuple(record[k].strip() for k in ('name', 'event', 'start', 'end'))
        if a <= end and b >= start and key not in seen:
            records.append(record)
            seen.add(key)
    records.sort(key=lambda r: (max(r['start'], start.isoformat()), r['name']))
    def category(r):
        event = r['event'].strip().casefold()
        if event == 'licencia' or event.startswith('licencia mdica'):
            return 'Licencias'
        if event == 'feriado legal':
            return 'Feriados legales'
        return 'Permisos y otras ausencias'
    def fmt(d):
        return d.strftime('%d/%m/%Y')
    e = escape
    url = e(data['sourceUrl'], quote=True)
    out = f'''<!-- RRHH_WEEKLY_START -->
<section id="rrhh-semana" data-week-start="{start}" data-week-end="{end}" class="section">
<div class="exec-title"><h2>RRHH  Ausencias de la semana</h2><span>Del {fmt(start)} al {fmt(end)}  lunes a domingo</span></div>
<p class="exec-note">ltimo corte RRHH: {checked.strftime('%d/%m/%Y  %H:%M')} (Chile). Actualizacin diaria junto con los indicadores y avisos.</p>
<p id="rrhh-stale" class="cutoff" hidden>El resumen de la semana en curso est pendiente de actualizar. Consulta la planilla original para revisar las ausencias vigentes.</p>
<div id="rrhh-current-data"><div class="metrics rrhh-metrics">
<article class="metric"><h3>Personas con ausencias</h3><strong class="value">{len(set(r['name'] for r in records))}</strong><p>Personas distintas con al menos un registro durante esta semana.</p></article>'''
    for label in ['Licencias', 'Feriados legales', 'Permisos y otras ausencias']:
        count = sum(category(r) == label for r in records)
        out += f'<article class="metric"><h3>{label}</h3><strong class="value">{count}</strong><p>Registros que coinciden con esta semana.</p></article>'
    out += '</div><div class="wide table-scroll"><table class="exec-table"><caption>Detalle semanal de ausencias registradas</caption><thead><tr><th scope="col">Funcionario/a</th><th scope="col">rea</th><th scope="col">Tipo de ausencia</th><th scope="col">Fechas en esta semana</th></tr></thead><tbody>'
    for r in records:
        a, b = max(date.fromisoformat(r['start']), start), min(date.fromisoformat(r['end']), end)
        period = fmt(a) if a == b else f'{fmt(a)} al {fmt(b)}'
        out += f"<tr><th scope=\"row\">{e(r['name'])}</th><td>{e(r.get('area', 'No informada'))}</td><td>{e(r['event'])}</td><td>{period}</td></tr>"
    if not records:
        out += '<tr><td colspan="4">Sin ausencias registradas para esta semana en las fuentes verificadas.</td></tr>'
    out += '</tbody></table></div><p class="exec-note">Los permisos parciales conservan su denominacin original. Las cifras cuentan registros, no das completos de ausencia. Se incluyen perodos iniciados antes de esta semana cuando continan vigentes.</p></div>'
    out += f'<a class="source" href="{url}" target="_blank" rel="noopener noreferrer">Abrir planilla RRHH-CES ?</a>  <a class="source" href="rrhh/2026/2026.html">Ver RRHH 2026  </a></section>\n<!-- RRHH_WEEKLY_END -->'
    return out

if __name__ == '__main__':
    data = json.loads(Path(sys.argv[1]).read_text())
    path = Path(__file__).resolve().parents[1] / 'dist/index.html'
    text = path.read_text()
    panel = render(data)
    if '<!-- RRHH_WEEKLY_START -->' in text:
        left = text.index('<!-- RRHH_WEEKLY_START -->')
        right = text.index('<!-- RRHH_WEEKLY_END -->', left) + len('<!-- RRHH_WEEKLY_END -->')
        text = text[:left] + text[right:]
    text = text.replace('<section class="brief">', panel + '\n<section class="brief">', 1)
    path.write_text(text)
    print('Panel semanal de RRHH actualizado con datos verificados.')
