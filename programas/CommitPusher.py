import os
import time
import subprocess
from git import Repo, GitCommandError
from tkinter import Tk, filedialog
from tqdm import tqdm

TOKEN_FILE = os.path.expanduser("~/.token_git")
MAX_ARCHIVOS_POR_PUSH = 100

# === FUNCIONES ===

def leer_gitignore(ruta):
    patrones = []
    gitignore_path = os.path.join(ruta, ".gitignore")
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if linea and not linea.startswith("#"):
                    patrones.append(linea)
    return patrones

def archivo_ignorado(ruta_archivo, patrones):
    for patron in patrones:
        if patron in ruta_archivo:
            return True
    return False

def listar_archivos_validos(ruta, patrones):
    archivos_validos = []
    for raiz, _, archivos in os.walk(ruta):
        if ".git" in raiz:
            continue
        for archivo in archivos:
            ruta_relativa = os.path.relpath(os.path.join(raiz, archivo), ruta)
            if archivo_ignorado(ruta_relativa, patrones):
                continue
            if archivo.endswith(('.tmp', '.log', '.bak', '.pyc', '.swp')):
                continue
            archivos_validos.append(ruta_relativa)
    return archivos_validos

def dividir_archivos(archivos, total_commits):
    grupos = []
    total_archivos = len(archivos)
    base = total_archivos // total_commits
    resto = total_archivos % total_commits
    indice = 0
    for i in range(total_commits):
        cantidad = base + (1 if i < resto else 0)
        grupo = archivos[indice:indice + cantidad]
        grupos.append(grupo)
        indice += cantidad
    return grupos

def dividir_por_tamano(grupo):
    return [grupo[i:i + MAX_ARCHIVOS_POR_PUSH] for i in range(0, len(grupo), MAX_ARCHIVOS_POR_PUSH)]

def ejecutar_comando(comando, ruta):
    resultado = subprocess.run(comando, shell=True, cwd=ruta, text=True, capture_output=True)
    if resultado.returncode != 0:
        print(f"⚠️ Error ejecutando {comando}: {resultado.stderr}")

def obtener_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r", encoding="utf-8") as f:
            token = f.read().strip()
            if token:
                print("🔐 Token cargado automáticamente desde archivo seguro.")
                return token

    token = input("🔐 Ingresa tu token de acceso personal (PAT) de GitHub: ").strip()
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        f.write(token)
    print("✅ Token guardado de forma segura. No volverá a pedirse.")
    return token

def seleccionar_rama(repo):
    """Detecta ramas existentes y permite al usuario elegir o crear una."""
    ramas_locales = [h.name for h in repo.heads]
    ramas_remotas = []
    try:
        repo.git.fetch("--all")
        ramas_remotas = [r.name.split("/")[-1] for r in repo.remotes.origin.refs]
    except Exception:
        pass

    todas = sorted(set(ramas_locales + ramas_remotas))
    if todas:
        print("\n🌿 Ramas detectadas:")
        for i, r in enumerate(todas, start=1):
            print(f"  {i}. {r}")
        opcion = input("👉 Elige el número de la rama o deja vacío para crear una nueva: ").strip()
        if opcion.isdigit() and 1 <= int(opcion) <= len(todas):
            rama = todas[int(opcion)-1]
            print(f"✅ Usando rama existente: {rama}")
            repo.git.checkout(rama)
            return rama

    # Si no hay ramas o el usuario desea crear una nueva
    rama = input("🆕 Nombre de nueva rama (por defecto 'main'): ").strip() or "main"
    try:
        repo.git.checkout("-b", rama)
        print(f"🌱 Rama creada y activada: {rama}")
    except GitCommandError:
        repo.git.checkout(rama)
        print(f"🌿 Rama existente activada: {rama}")
    return rama

# === PROGRAMA PRINCIPAL ===

def main():
    print("🗂️  Selecciona la carpeta del proyecto...")
    Tk().withdraw()
    ruta_proyecto = filedialog.askdirectory(title="Selecciona la carpeta del proyecto")

    if not ruta_proyecto:
        print("❌ No se seleccionó ninguna carpeta.")
        return

    print(f"📂 Proyecto seleccionado: {ruta_proyecto}")

    if not os.path.exists(os.path.join(ruta_proyecto, ".git")):
        print("📦 Inicializando repositorio Git nuevo...")
        ejecutar_comando("git init", ruta_proyecto)

    repo = Repo(ruta_proyecto)

    rama = seleccionar_rama(repo)

    patrones_ignore = leer_gitignore(ruta_proyecto)
    archivos = listar_archivos_validos(ruta_proyecto, patrones_ignore)

    print(f"📂 Total de archivos detectados: {len(archivos)}")

    if not archivos:
        print("❌ No se encontraron archivos válidos para hacer commit.")
        return

    remote_url = input("🔗 Ingresa la URL del repositorio remoto: ").strip()

    token = obtener_token()
    if remote_url.startswith("https://") and "@" not in remote_url:
        remote_url = remote_url.replace("https://", f"https://{token}@")

    if "origin" not in [remote.name for remote in repo.remotes]:
        repo.create_remote("origin", remote_url)
    else:
        repo.git.remote("set-url", "origin", remote_url)

    num_colaboradores = int(input("👥 ¿Cuántos colaboradores participarán?: "))
    colaboradores = []

    for i in range(num_colaboradores):
        print(f"\n👤 Datos del integrante {i+1}:")
        nombre = input("  Nombre completo: ").strip()
        username = input("  GitHub username: ").strip()
        email = input("  Email (puede ser ficticio): ").strip()
        commits = int(input("  ¿Cuántos commits debe generar este usuario?: "))
        colaboradores.append({
            "nombre": nombre,
            "username": username,
            "email": email,
            "commits": commits
        })

    total_commits = sum(c["commits"] for c in colaboradores)
    grupos = dividir_archivos(archivos, total_commits)

    print(f"\n🚀 Se generarán {total_commits} commits automáticos (máx. 100 archivos por push)...\n")

    index_commit = 0
    for colaborador in colaboradores:
        for i in range(colaborador["commits"]):
            if index_commit >= len(grupos):
                break
            grupo = grupos[index_commit]
            index_commit += 1

            subgrupos = dividir_por_tamano(grupo)

            repo.config_writer().set_value("user", "name", colaborador["nombre"]).release()
            repo.config_writer().set_value("user", "email", colaborador["email"]).release()

            for sub_index, subgrupo in enumerate(subgrupos, start=1):
                if not subgrupo:
                    continue

                repo.index.add(subgrupo)
                mensaje = f"Commit {i+1}.{sub_index}/{colaborador['commits']} de {colaborador['nombre']} ({len(subgrupo)} archivos)"
                repo.index.commit(mensaje)
                print(f"📄 {mensaje}")

                try:
                    repo.git.push("origin", rama)
                    print(f"⬆️  Push exitoso ({mensaje})")
                except GitCommandError as e:
                    print(f"⚠️ Error en el push: {e}")

                for _ in tqdm(range(10), desc="⏳ Esperando siguiente push", ncols=70):
                    time.sleep(1)

    print("\n🎉 ¡Proceso completado! Todos los commits fueron generados y subidos correctamente 🚀")

if __name__ == "__main__":
    main()
