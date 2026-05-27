import re
import os

class SecurityShield:
    """
    Módulo de Seguridad Grado Bancario (Bank-Grade Security).
    Encargado de interceptar, validar y sanitizar todas las entradas y archivos.
    """
    
    # Firmas mágicas de archivos (Hex signatures)
    # Excel moderno (.xlsx) es un ZIP, su firma empieza con PK
    MAGIC_BYTES = {
        'xlsx': b'PK\x03\x04',
        'xls': b'\xd0\xcf\x11\xe0',
        'xml': b'<?xml',
        'csv': None, # CSV es texto plano, no tiene firma mágica estándar estricta
        'pdf': b'%PDF',
        'png': b'\x89PNG\r\n\x1a\n',
        'jpg': b'\xff\xd8\xff'
    }

    # Máximo tamaño en Megabytes
    MAX_FILE_SIZE_MB = 15

    @classmethod
    def scan_file(cls, uploaded_file, expected_extension: str) -> tuple[bool, str]:
        """
        Escanea un archivo subido en memoria antes de procesarlo.
        Retorna (es_seguro, mensaje_error).
        """
        if uploaded_file is None:
            return False, "No se detectó archivo."

        filename = uploaded_file.name.lower()
        
        # 1. Validación de tamaño (Anti-DDoS)
        file_size_mb = uploaded_file.size / (1024 * 1024)
        if file_size_mb > cls.MAX_FILE_SIZE_MB:
            return False, f"⚠️ AMENAZA: Archivo supera el límite seguro de {cls.MAX_FILE_SIZE_MB}MB. Posible ataque de denegación de servicio."

        # 2. Validación de extensión doble (Anti-Evasion)
        # Ejemplo: archivo.xlsx.exe -> peligroso
        parts = filename.split('.')
        if len(parts) > 2 and parts[-1] not in ['xlsx', 'xml', 'csv', 'jpg', 'png', 'pdf']:
            return False, "⚠️ AMENAZA: Intento de ofuscación de extensión detectado."
            
        if not filename.endswith(expected_extension.lower()):
            return False, f"Extensión no coincide con {expected_extension}"

        # 3. Validación de Magic Bytes (Anti-Malware Spoofing)
        expected_extension = expected_extension.lower().replace('.', '')
        if expected_extension in cls.MAGIC_BYTES and cls.MAGIC_BYTES[expected_extension]:
            magic_signature = cls.MAGIC_BYTES[expected_extension]
            # Leer los primeros bytes
            header = uploaded_file.read(len(magic_signature))
            # Resetear el puntero para que Pandas/XML lo pueda leer después
            uploaded_file.seek(0)
            
            # Para XML, permitimos espacios o BOM antes del <?xml
            if expected_extension == 'xml':
                header_str = header.decode('utf-8', errors='ignore').strip()
                if not header_str.startswith('<?xml') and '<' not in header_str:
                     return False, "⚠️ AMENAZA DE MALWARE: El archivo no es un XML real. Posible inyección."
            else:
                if header != magic_signature:
                    return False, f"⚠️ AMENAZA DE MALWARE: El archivo aparenta ser .{expected_extension} pero su firma interna es maliciosa o corrupta."

        return True, "SAFE"

    @classmethod
    def analyze_text_threats(cls, text: str) -> tuple[bool, str]:
        """
        Analiza texto (inputs del chat) en busca de inyecciones SQL, XSS o comandos.
        Retorna True si hay AMENAZA.
        """
        if not text:
            return False, ""
            
        text_lower = text.lower()
        
        # Patrones de ataque comunes
        threat_patterns = [
            r"<script.*?>.*?</script>", # XSS
            r"javascript:",             # XSS
            r"(?i)(union\s+select|drop\s+table|delete\s+from|insert\s+into)", # SQL Injection básica
            r"(\.\./\.\./\.\./)",       # Path Traversal
            r"cat\s+/etc/passwd",       # Linux exploits
        ]
        
        for pattern in threat_patterns:
            if re.search(pattern, text_lower):
                return True, "Inyección de código malicioso detectada."
                
        return False, ""
