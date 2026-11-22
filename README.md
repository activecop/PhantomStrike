# PhantomStrike
Professional WiFi Auditing Tool - Multi-language
# 🎯 PhantomStrike

**Professional WiFi Auditing Tool**  
*Ferramenta Profissional de Auditoria de Redes WiFi*  
*专业WiFi网络审计工具*  
*Профессиональный инструмент аудита WiFi*

![Version](https://img.shields.io/badge/version-3.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.8+-yellow)
![OS](https://img.shields.io/badge/os-Zorin%20%7C%20Ubuntu%20%7C%20Debian-orange)

---

## 🌍 Multi-Language Support

PhantomStrike supports 4 languages with automatic detection:
- 🇵🇹 **Português** (Portugal)
- 🇬🇧 **English**
- 🇨🇳 **中文** (Chinese)
- 🇷🇺 **Русский** (Russian)

Press **`L`** in the main menu to switch languages at any time.

---

## ⚠️ Legal Disclaimer

**This tool is intended EXCLUSIVELY for authorized penetration testing** on networks you own or have explicit written permission to test. Unauthorized use is illegal and may result in criminal charges.

**Esta ferramenta destina-se EXCLUSIVAMENTE a testes de penetração autorizados** em redes próprias ou com permissão explícita do proprietário. O uso não autorizado é ilegal.

**此工具仅供授权渗透测试使用**，仅限您拥有或已获得明确书面许可的网络。未经授权使用属违法行为。

**Этот инструмент предназначен ИСКЛЮЧИТЕЛЬНО для авторизованного тестирования** сетей, которыми вы владеете или имеете явное письменное разрешение. Несанкционированное использование является незаконным.

---

## ✨ Features

### 🔍 Scan Module
- **Continuous WiFi scan** with real-time updates (press `CTRL+C` to stop)
- **Wifite-style colors**: WPA3 (green), WPA2 (yellow), WEP (red), Open (cyan)
- **Signal strength colors**: Strong (green), Medium (yellow), Weak (red)
- **Live client count** per Access Point
- **New client detection** with magenta highlight
- **Local network host scan** via arp-scan/nmap

### ⚔️ Attack Module
- **4 deauth methods**: Scapy, aireplay-ng, mdk3, mdk4
- **Per-client targeting**: Attacks each detected client individually
- **Detailed visual feedback**: See every packet being sent with MAC addresses
- **Smart filtering**: Only targets APs with connected clients
- **Adjustable parameters**: Duration (mdk3/4) or packet count (scapy/aireplay)

### 🎭 Anonymity Module
- **Random MAC spoofing** with one click
- **Automatic restoration** on exit or network restore
- **Visual indicator** showing spoofed/original MAC state

---

## 📸 Screenshots

<img width="1104" height="2110" alt="GUI_PT-PT" src="https://github.com/user-attachments/assets/10596d83-d061-4698-b48b-df02aa3535f5" />
<img width="1104" height="451" alt="SELEC_LANG" src="https://github.com/user-attachments/assets/ac41250c-6ce8-492f-9031-78cfc5c10df9" />

<img width="1104" height="2107" alt="GUI_EN" src="https://github.com/user-attachments/assets/d7437cb6-dda1-4ec6-af2a-a406764bbd00" />
<img width="1104" height="2107" alt="GUI_CN" src="https://github.com/user-attachments/assets/8d248401-ea4b-4326-82e0-1975e3461366" />
<img width="1104" height="2107" alt="GUI_RU" src="https://github.com/user-attachments/assets/038aab00-a967-4fb8-b001-7af8b5b3abb3" />
<img width="1104" height="568" alt="method" src="https://github.com/user-attachments/assets/ccc49099-8ab3-45cb-bddf-e56947d118dd" />
<img width="1104" height="2107" alt="SCAN" src="https://github.com/user-attachments/assets/9b74d292-d8dc-4834-8189-5ba9d719ad8c" />
<img width="1505" height="1535" alt="MDK4_" src="https://github.com/user-attachments/assets/52b9425a-0416-4435-aaf2-634d80d896fa" />


---

## 🚀 Installation

### Requirements
- **OS**: Zorin OS, Ubuntu, Debian (or any Debian-based distro)
- **Python**: 3.8+
- **Root privileges** required
- **WiFi adapter** with monitor mode support

### Quick Install

```bash
# Clone the repository
git clone https://github.com/activecop/PhantomStrike.git
cd PhantomStrike

# Run the installer
sudo chmod +x install.sh
sudo ./install.sh

# Launch
sudo phantomstrike
