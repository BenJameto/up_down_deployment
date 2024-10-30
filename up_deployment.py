import subprocess

def get_namespaces():
    # Ejecutar el comando kubectl get namespaces
    result = subprocess.run(["kubectl", "get", "namespaces", "-o", "name"], capture_output=True, text=True)
    
    # Procesar la salida y convertirla en una lista
    namespaces = result.stdout.splitlines()
    #print("Namespaces disponibles:", namespaces)
    
    # Eliminar el prefijo 'namespace/' de cada entrada
    namespaces = [ns.split("/")[1] for ns in namespaces]
    
    return namespaces

def scale_service():
    # Obtener la lista de namespaces
    namespaces = get_namespaces()
    
    # Mostrar la lista y pedir al usuario que elija un namespace
    print("Lista de namespaces disponibles:")
    for idx, ns in enumerate(namespaces, 1):
        print(f"{idx}. {ns}")
    
    ns_idx = int(input("Selecciona el número del namespace que deseas usar: ")) - 1
    selected_namespace = namespaces[ns_idx]
    
    # Obtener la lista de deployments en el namespace seleccionado
    result = subprocess.run(["kubectl", "get", "deployments", "-n", selected_namespace, "-o", "name"], capture_output=True, text=True)
    deployments = result.stdout.splitlines()
    deployments = [dep.split("/")[1] for dep in deployments]
    
    # Mostrar la lista de deployments y pedir al usuario que elija uno
    print("Lista de deployments disponibles en el namespace seleccionado:")
    for idx, dep in enumerate(deployments, 1):
        print(f"{idx}. {dep}")
    
    dep_idx = int(input("Selecciona el número del deployment que deseas escalar: ")) - 1
    selected_deployment = deployments[dep_idx]
    
    # Preguntar cuántas réplicas desea
    replicas = int(input("¿Cuántas réplicas deseas para este deployment?: "))
    
    # Escalar el deployment
    subprocess.run(["kubectl", "scale", f"deployment/{selected_deployment}", f"--replicas={replicas}", "-n", selected_namespace])

if __name__ == "__main__":
    scale_service()
