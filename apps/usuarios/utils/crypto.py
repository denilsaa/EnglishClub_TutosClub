# apps/usuarios/utils/crypto.py
import hashlib

def hash_password(password: str, correo: str) -> str:
    """
    Genera SHA-256(password + salt).
    El 'salt' será:
      - lo que está antes del '@' si existe '@'
      - o todo el string si no hay '@'
    """
    correo = (correo or "").strip()
    salt = correo.split("@")[0] if "@" in correo else correo
    return hashlib.sha256((password + salt).encode()).hexdigest()
