import json
import re

path = r'c:\Users\manue\OneDrive\Documentos\proyectos portafolio\Analisis de datos\Impacto economico\ProyectoImpactoEconomico.ipynb'
with open(path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

map_text = {
    'get_presupuesto_medio': 'get_average_budget',
    'rango': 'budget_range',
    'min_max': 'min_max_values',
    'genero_counts': 'gender_counts',
    'promedio_por_semestre': 'avg_per_semester',
    'trabajo_stats': 'work_stats',
    'emprendimiento_stats': 'entrepreneurship_stats',
    'Género': 'Gender',
    'Semestre cursado': 'Semester',
    'Presupuesto mensual': 'Monthly budget',
    'Trabajo y estudio': 'Work and study',
    'Emprendimientos': 'Entrepreneurship',
    'Presupuesto_medio': 'Average_budget',
    'Cantidad de estudiantes': 'Student Count',
    'Promedio': 'Average',
    'Mínimo': 'Minimum',
    'Máximo': 'Maximum',
    'Total de estudiantes:': 'Total students:',
    'Estadísticas por semestre:': 'Statistics by Semester:',
    'Estadísticas según situación laboral:': 'Statistics by Labor Situation:',
    'Estadísticas según emprendimiento:': 'Statistics by Entrepreneurship:',
    'Estadísticas combinadas (Trabajo y Emprendimiento):': 'Combined Statistics (Work & Entrepreneurship):',
    'No trabaja': 'Does not work',
    'Sí trabaja': 'Works',
    'No tiene': 'Does not have',
    'Sí tiene': 'Has',
    'Presupuesto Promedio según Situación Laboral': 'Average Budget by Labor Situation',
    'Presupuesto Promedio según Emprendimiento': 'Average Budget by Entrepreneurship',
    'Distribución de Presupuestos por Semestre': 'Budget Distribution by Semester',
    'Presupuesto Promedio por Semestre': 'Average Budget by Semester',
    'Presupuesto (COP)': 'Budget (COP)',
    'Presupuesto Promedio (COP)': 'Average Budget (COP)',
    'Semestre': 'Semester',
    '# Leer el archivo': '# Read the file',
    '# Limpiamos el string y obtenemos los números': '# Clean string and extract numbers',
    '# Convertimos los presupuestos a valores numéricos': '# Convert budgets to numeric values',
    '# Crear una figura con dos subplots': '# Create a figure with two subplots',
    '# Ajustar el diseño': '# Adjust layout',
    '# Calcular y mostrar estadísticas': '# Calculate and show statistics'
}

robust_parser = """def get_average_budget(budget_range):
    if pd.isna(budget_range): return None
    try:
        clean_str = str(budget_range).replace('.', '').replace("'", '').replace(' ', '').replace(',', '')
        if '+' in clean_str:
            val = float(clean_str.replace('+', ''))
            return val * 1.1
        if '-' in clean_str:
            min_max_values = clean_str.split('-')
            return (float(min_max_values[0]) + float(min_max_values[1])) / 2
        return float(clean_str)
    except:
        return None"""

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        if 'def get_presupuesto_medio' in source:
            source = re.sub(r'def get_presupuesto_medio\(rango\):.*?return None', robust_parser, source, flags=re.DOTALL)
        for k in sorted(map_text.keys(), key=len, reverse=True):
            source = source.replace(k, map_text[k])
        cell['source'] = [line + '\n' for line in source.splitlines()]
        if cell['source']: cell['source'][-1] = cell['source'][-1].rstrip('\n')

with open(path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
