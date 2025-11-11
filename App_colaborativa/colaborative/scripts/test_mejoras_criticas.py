from validador_contexto_retorica import ValidadorContextoRetorica

def main():
    texto = "La CSJN resolvió con autoridad. Hubo crisis y urgencia, por lo tanto se actuó razonablemente."
    v = ValidadorContextoRetorica()
    ethos = v.analizar_ethos(texto)
    pathos = v.analizar_pathos(texto)
    logos = v.analizar_logos(texto)
    print(f"ETHOS: {len(ethos)} PATHOS: {len(pathos)} LOGOS: {len(logos)}")
    
    # Mostrar detalles de cada análisis
    print("\n=== ANÁLISIS DETALLADO ===")
    print(f"ETHOS encontrados: {len(ethos)}")
    for e in ethos:
        print(f"  - '{e.palabra}' (confianza: {e.confianza})")
    
    print(f"\nPATHOS encontrados: {len(pathos)}")
    for p in pathos:
        print(f"  - '{p.palabra}' (confianza: {p.confianza})")
    
    print(f"\nLOGOS encontrados: {len(logos)}")
    for l in logos:
        print(f"  - '{l.palabra}' (confianza: {l.confianza})")
    
    print("✅ Test retórico ejecutado correctamente.")

if __name__ == "__main__":
    main()