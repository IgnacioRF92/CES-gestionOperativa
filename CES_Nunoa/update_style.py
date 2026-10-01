import re

file_path = r'c:\Users\CES\Desktop\gestion CES\Codigo_CES_Nunoa_v34\CES_Nunoa\dist\index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Extraer el bloque <style> principal
style_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
if style_match:
    style_content = style_match.group(1)
    
    # Modificar style_content para glassmorphism
    new_style = style_content
    
    # 1. Actualizar fondo raíz
    new_style = new_style.replace('background: #eef3f6;', 'background: linear-gradient(135deg, #ffffff, #b7e5e5); background-attachment: fixed;')
    
    # 2. Actualizar panel lateral
    new_style = new_style.replace('background: #103750;', 'background: rgba(255, 255, 255, 0.4); backdrop-filter: blur(20px); border-right: 1px solid rgba(255,255,255,0.6);')
    new_style = new_style.replace('color: #e6f2f4;', 'color: #17364a;')
    new_style = new_style.replace('color: #cce0e5;', 'color: #2b6161;')
    new_style = new_style.replace('color: #a9cad3;', 'color: #3ab9b8;')
    new_style = new_style.replace('border-top: 1px solid #326077;', 'border-top: 1px solid rgba(58, 185, 184, 0.3);')
    new_style = new_style.replace('color: #b3ced5;', 'color: #2b6161;')
    new_style = new_style.replace('background: #24536a;', 'background: rgba(58, 185, 184, 0.2);')
    new_style = new_style.replace('color: white;', 'color: #0c3636;')

    # 3. Actualizar marca (marcador de logotipo)
    new_style = new_style.replace('background: #56cabd;', 'background: #3ab9b8;')
    new_style = new_style.replace('color: #103750;', 'color: #ffffff;')

    # 4. Actualizar encabezado (lead)
    new_style = new_style.replace('background: #103e59;', 'background: rgba(58, 185, 184, 0.8); backdrop-filter: blur(15px); border: 1px solid rgba(255,255,255,0.5); box-shadow: 0 8px 32px rgba(58,185,184,0.2);')
    new_style = new_style.replace('color: white;', 'color: #ffffff;')
    new_style = new_style.replace('color: #d4e8ed;', 'color: #f0fafa;')
    new_style = new_style.replace('border: 1px solid #5b8ba0;', 'border: 1px solid rgba(255,255,255,0.6);')
    new_style = new_style.replace('color: #bbede5;', 'color: #ffffff;')

    # 5. Actualizar tarjetas y contenedores anchos
    new_style = new_style.replace('background: #fff;', 'background: rgba(255, 255, 255, 0.55); backdrop-filter: blur(12px);')
    new_style = new_style.replace('border: 1px solid #d6e2e8;', 'border: 1px solid rgba(255, 255, 255, 0.8);')
    new_style = new_style.replace('box-shadow: 0 4px 16px #17364a08;', 'box-shadow: 0 8px 32px rgba(58, 185, 184, 0.1);')

    # 6. Botones / Píldoras / Fechas
    new_style = new_style.replace('background: white;', 'background: rgba(255, 255, 255, 0.6); backdrop-filter: blur(10px);')
    new_style = new_style.replace('border: 1px solid #c5d6df;', 'border: 1px solid rgba(255, 255, 255, 0.8);')
    
    # 7. Resumen (Brief)
    new_style = new_style.replace('background: #103e59;', 'background: rgba(58, 185, 184, 0.75); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.4);')
    new_style = new_style.replace('color: white;', 'color: #ffffff;')
    new_style = new_style.replace('color: #e0edf1;', 'color: #f0fafa;')

    # 8. Elementos de alerta
    new_style = new_style.replace('background: white;', 'background: rgba(255, 255, 255, 0.6); backdrop-filter: blur(12px);')
    new_style = new_style.replace('border: 1px solid #d6e2e8;', 'border: 1px solid rgba(255, 255, 255, 0.8);')

    # 9. Tabla y límite (Cutoff)
    new_style = new_style.replace('background: #fff7df;', 'background: rgba(255, 247, 223, 0.7); backdrop-filter: blur(8px);')
    
    # 10. Métricas y estilos específicos
    new_style = new_style.replace('background: white;', 'background: rgba(255, 255, 255, 0.6); backdrop-filter: blur(12px);')

    content = content.replace(style_match.group(0), f'<style>{new_style}</style>')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print('Estilo actualizado exitosamente en index.html')
else:
    print('No se pudo encontrar el bloque <style>')
