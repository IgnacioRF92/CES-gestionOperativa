import os
import re

base_dir = r'c:\Users\CES\Desktop\gestion CES\Codigo_CES_Nunoa_v34\CES_Nunoa\dist'
global_css_path = os.path.join(base_dir, 'global.css')

# Encontrar el primer archivo HTML para extraer los estilos
index_file = os.path.join(base_dir, 'index.html')
with open(index_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Extraer todos los bloques de estilo de index.html
style_blocks = re.findall(r'(<style[^>]*>)(.*?)</style>', content, re.DOTALL)

# Combinar el contenido CSS
combined_css = ""
for tag, css in style_blocks:
    combined_css += f"/* Extraído de {tag} */\n{css.strip()}\n\n"

# Escribir a global.css
with open(global_css_path, 'w', encoding='utf-8') as f:
    f.write(combined_css)

print(f"global.css creado con {len(style_blocks)} bloques de estilo.")

# Ahora iterar sobre todos los archivos HTML y reemplazar estilos en línea con la etiqueta link
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Calcular ruta relativa a global.css
            rel_path = os.path.relpath(global_css_path, root)
            rel_path = rel_path.replace(os.sep, '/')
            
            # La etiqueta <link>
            link_tag = f'<link rel="stylesheet" href="{rel_path}" />'
            
            # Solo insertar la etiqueta link una vez por archivo si hay alguna etiqueta style
            if '<style' in html_content:
                # Reemplazar el primer bloque style con la etiqueta link
                html_content = re.sub(r'<style[^>]*>.*?</style>', link_tag, html_content, count=1, flags=re.DOTALL)
                # Remover bloques style subsiguientes
                html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                print(f"Actualizado {filepath} con {link_tag}")
