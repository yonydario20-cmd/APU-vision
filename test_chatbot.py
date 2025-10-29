"""
Script de prueba para verificar componentes sin ejecutar el bot completo
"""
import sys
import os

def test_imports():
    """Verifica que todos los módulos se puedan importar"""
    print("✓ Verificando imports...")
    try:
        import config
        print("  ✓ config.py importado correctamente")
        
        import knowledge_base
        print("  ✓ knowledge_base.py importado correctamente")
        print(f"  ✓ Base de conocimiento contiene {len(knowledge_base.CLINIC_KNOWLEDGE)} categorías")
        
        # Verificar que tenemos las dependencias necesarias
        try:
            import telegram
            print("  ✓ python-telegram-bot instalado")
        except ImportError:
            print("  ⚠ python-telegram-bot no instalado (normal en testing)")
        
        try:
            import langchain
            print("  ✓ langchain instalado")
        except ImportError:
            print("  ⚠ langchain no instalado (normal en testing)")
        
        try:
            import chromadb
            print("  ✓ chromadb instalado")
        except ImportError:
            print("  ⚠ chromadb no instalado (normal en testing)")
            
        return True
    except Exception as e:
        print(f"  ✗ Error al importar: {str(e)}")
        return False

def test_configuration():
    """Verifica la configuración"""
    print("\n✓ Verificando configuración...")
    try:
        # Verificar que el archivo .env.example existe
        if os.path.exists('.env.example'):
            print("  ✓ .env.example existe")
        
        # Verificar que .gitignore existe
        if os.path.exists('.gitignore'):
            print("  ✓ .gitignore existe")
            
        return True
    except Exception as e:
        print(f"  ✗ Error en configuración: {str(e)}")
        return False

def test_knowledge_base():
    """Verifica la base de conocimiento"""
    print("\n✓ Verificando base de conocimiento...")
    try:
        from knowledge_base import CLINIC_KNOWLEDGE
        
        categories = [item['category'] for item in CLINIC_KNOWLEDGE]
        print(f"  ✓ Categorías encontradas: {len(categories)}")
        for cat in categories:
            print(f"    - {cat}")
        
        # Verificar que cada item tiene los campos requeridos
        for item in CLINIC_KNOWLEDGE:
            assert 'category' in item, "Falta campo 'category'"
            assert 'content' in item, "Falta campo 'content'"
            assert len(item['content'].strip()) > 0, "Contenido vacío"
        
        print("  ✓ Todos los items tienen campos requeridos")
        return True
    except Exception as e:
        print(f"  ✗ Error en base de conocimiento: {str(e)}")
        return False

def test_file_structure():
    """Verifica la estructura de archivos"""
    print("\n✓ Verificando estructura de archivos...")
    required_files = [
        'telegram_bot.py',
        'chatbot.py',
        'vector_store.py',
        'config.py',
        'knowledge_base.py',
        'requirements.txt',
        'README.md',
        '.gitignore',
        '.env.example'
    ]
    
    all_exist = True
    for filename in required_files:
        if os.path.exists(filename):
            print(f"  ✓ {filename}")
        else:
            print(f"  ✗ {filename} no encontrado")
            all_exist = False
    
    return all_exist

def main():
    """Ejecuta todas las pruebas"""
    print("=" * 60)
    print("PRUEBAS DEL CHATBOT IPS VISIÓN CÁRDENAS")
    print("=" * 60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Configuración", test_configuration()))
    results.append(("Base de conocimiento", test_knowledge_base()))
    results.append(("Estructura de archivos", test_file_structure()))
    
    print("\n" + "=" * 60)
    print("RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(results)} pruebas pasadas")
    
    if passed == len(results):
        print("\n🎉 ¡Todas las pruebas pasaron correctamente!")
        return 0
    else:
        print("\n⚠ Algunas pruebas fallaron")
        return 1

if __name__ == "__main__":
    sys.exit(main())
