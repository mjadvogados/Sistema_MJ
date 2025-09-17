import psutil

def get_hamachi_ip_psutil():
    """Busca o IP da interface Hamachi usando psutil."""
    interfaces = psutil.net_if_addrs()
    for iface_name, addrs in interfaces.items():
        if "hamachi" in iface_name.lower() or "logmein" in iface_name.lower():
            for addr in addrs:
                # Endereço IPv4
                if addr.family == psutil.AF_INET:
                    ip = addr.address
                    # Desconsiderar IP APIPA 169.254.x.x
                    if not ip.startswith("169.254."):
                        return ip
    return None

def is_hamachi_online_psutil():
    if not is_hamachi_running():
        return False
    ip = get_hamachi_ip_psutil()
    if ip:
        return True
    return False

if __name__ == "__main__":
    if is_hamachi_running():
        print("Hamachi está em execução.")
        ip = get_hamachi_ip_psutil()
        if ip:
            print(f"Hamachi está ONLINE com IP: {ip}")
        else:
            print("Hamachi está OFFLINE (não encontrou IP válido na interface).")
    else:
        print("Hamachi NÃO está em execução.")
