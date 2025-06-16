import requests

BASE_URL = "http://127.0.0.1:8000"

def test_list_containers():
    print("Probando GET /containers")
    response = requests.get(f"{BASE_URL}/containers")
    if response.status_code == 200:
        containers = response.json()
        print(f"Contenedores encontrados: {len(containers)}")
        for c in containers:
            print(f"- {c['name']} ({c['id']}): {c['status']}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

def test_get_alerts():
    print("\nProbando GET /alerts")
    response = requests.get(f"{BASE_URL}/alerts")
    if response.status_code == 200:
        alerts = response.json()
        if alerts:
            print("Alertas activas:")
            for a in alerts:
                print(f" - {a}")
        else:
            print("No hay alertas activas")
    else:
        print(f"Error: {response.status_code} - {response.text}")

def test_get_logs(container_id):
    print(f"\nProbando GET /containers/{container_id}/logs")
    response = requests.get(f"{BASE_URL}/containers/{container_id}/logs")
    if response.status_code == 200:
        logs = response.json().get("logs", "")
        print(f"Logs últimos 50 líneas:\n{logs[:500]}") 
    else:
        print(f"Error: {response.status_code} - {response.text}")

def main():
    test_list_containers()
    test_get_alerts()

    response = requests.get(f"{BASE_URL}/containers")
    if response.status_code == 200 and len(response.json()) > 0:
        first_container_id = response.json()[0]["id"]
        test_get_logs(first_container_id)
    else:
        print("No se pudo probar logs por falta de contenedores")

if __name__ == "__main__":
    main()
