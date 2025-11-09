#!/usr/bin/env python3
import socket
import subprocess
import platform
import requests
import json
from typing import Optional

def get_public_ip() -> str:
    """Récupère l'adresse IP publique"""
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        return response.json()['ip']
    except:
        try:
            response = requests.get('https://icanhazip.com', timeout=5)
            return response.text.strip()
        except:
            return "Impossible à récupérer"

def get_local_ip() -> str:
    """Récupère l'adresse IP locale"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "Impossible à récupérer"

def get_gateway_ip() -> str:
    """Récupère l'adresse IP du routeur (passerelle)"""
    system = platform.system()
    
    try:
        if system == "Windows":
            result = subprocess.check_output("ipconfig", shell=True).decode('cp850', errors='ignore')
            for line in result.split('\n'):
                if "Passerelle par défaut" in line or "Default Gateway" in line:
                    parts = line.split(':')
                    if len(parts) > 1:
                        gateway = parts[1].strip()
                        if gateway and gateway != "":
                            return gateway
        
        elif system == "Linux":
            result = subprocess.check_output("ip route | grep default", shell=True).decode()
            gateway = result.split()[2]
            return gateway
        
        elif system == "Darwin":  # macOS
            result = subprocess.check_output("netstat -nr | grep default", shell=True).decode()
            gateway = result.split()[1]
            return gateway
    except:
        pass
    
    return "Impossible à récupérer"



def print_separator():
    """Affiche une ligne de séparation"""
    print("\033[36m" + "=" * 60 + "\033[0m")

def print_header():
    """Affiche le header avec logo NXN"""
    print("\n")
    print("\033[36m" + "=" * 60 + "\033[0m")
    print("\033[35m" + """
    ███╗   ██╗██╗  ██╗███╗   ██╗
    ████╗  ██║╚██╗██╔╝████╗  ██║
    ██╔██╗ ██║ ╚███╔╝ ██╔██╗ ██║
    ██║╚██╗██║ ██╔██╗ ██║╚██╗██║
    ██║ ╚████║██╔╝ ██╗██║ ╚████║
    ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═══╝
    """ + "\033[0m")
    print("\033[33m" + "      INFORMATIONS RÉSEAU" + "\033[0m")
    print("\033[36m" + "=" * 60 + "\033[0m")
    print()

def main():
    """Fonction principale"""
    print_header()
    
    print("\033[35m Adresse IP Publique:\033[0m")
    public_ip = get_public_ip()
    print(f"\033[33m   {public_ip}\033[0m")
    print()
    
    print("\033[35m Adresse IP Locale:\033[0m")
    local_ip = get_local_ip()
    print(f"\033[33m   {local_ip}\033[0m")
    print()
    
    print("\033[35m Adresse IP du Routeur:\033[0m")
    gateway_ip = get_gateway_ip()
    print(f"\033[33m   {gateway_ip}\033[0m")
    print()
    
    print_separator()
    
    # Informations supplémentaires
    print("\n\033[35m Informations de localisation (IP publique):\033[0m")
    location_found = False
    
    # Essayer ip-api.com (gratuit, sans limite stricte)
    try:
        response = requests.get('http://ip-api.com/json/', timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                print(f"\033[33m   Pays: {data.get('country', 'N/A')}\033[0m")
                print(f"\033[33m   Ville: {data.get('city', 'N/A')}\033[0m")
                print(f"\033[33m   Région: {data.get('regionName', 'N/A')}\033[0m")
                print(f"\033[33m   FAI: {data.get('isp', 'N/A')}\033[0m")
                location_found = True
    except:
        pass
    
    # Si ip-api.com échoue, essayer ipapi.co
    if not location_found:
        try:
            response = requests.get('https://ipapi.co/json/', timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"\033[33m   Pays: {data.get('country_name', 'N/A')}\033[0m")
                print(f"\033[33m   Ville: {data.get('city', 'N/A')}\033[0m")
                print(f"\033[33m   Région: {data.get('region', 'N/A')}\033[0m")
                print(f"\033[33m   FAI: {data.get('org', 'N/A')}\033[0m")
                location_found = True
        except:
            pass
    
    # Si tout échoue, essayer ipinfo.io
    if not location_found:
        try:
            response = requests.get('https://ipinfo.io/json', timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"\033[33m   Pays: {data.get('country', 'N/A')}\033[0m")
                print(f"\033[33m   Ville: {data.get('city', 'N/A')}\033[0m")
                print(f"\033[33m   Région: {data.get('region', 'N/A')}\033[0m")
                print(f"\033[33m   FAI: {data.get('org', 'N/A')}\033[0m")
                location_found = True
        except:
            pass
    
    if not location_found:
        print("\033[33m   Impossible de récupérer les informations de localisation\033[0m")
    
    print()
    print_separator()
    
    print()

if __name__ == "__main__":
    main()
