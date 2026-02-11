import json
import re

path = r'c:\Users\manue\OneDrive\Documentos\proyectos portafolio\Analisis de datos\Impacto economico\ProyectoImpactoEconomico.ipynb'
with open(path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

manual_map = {
    'min_max_values_values': 'min_max_values',
    '# Mostrar también la cantidad de estudiantes por semestre en forma de tabla': '# Show student count per semester as a table',
    'Student Count por semestre:': 'Student Count by Semester:',
    '# Añadir los valores y la cantidad de estudiantes sobre las barras': '# Add values and student count over the bars',
    '# Añadir los valores y la cantidad de estudiantes': '# Add values and student count',
    '# 1. Gráfico para Trabajo': '# 1. Work Chart',
    '# 2. Gráfico para Emprendimiento': '# 2. Entrepreneurship Chart',
    '# 1. Gráfico de cajas (Boxplot)': '# 1. Boxplot',
    '# 2. Gráfico de barras con promedio por semestre': '# 2. Bar chart with average per semester',
    '# Añadir los valores sobre las barras': '# Add values above the bars',
    'Promedio por semestre': 'Average per semester',
    'Resumen de Estadísticas': 'Statistics Summary',
    'Total de registros:': 'Total records:',
    'Error procesando el valor:': 'Error processing value:'
}

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        for k, v in manual_map.items():
            source = source.replace(k, v)
        
        # Fixing the logic for the parser just in case
        source = source.replace("min_max_values_values", "min_max_values")
        
        cell['source'] = [line + '\n' for line in source.splitlines()]
        if cell['source']: cell['source'][-1] = cell['source'][-1].rstrip('\n')

with open(path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
