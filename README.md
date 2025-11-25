# cs2run MITM Dump

Этот проект запускает MITM-прокси в GitHub Codespaces.
Используется для полного захвата клиентского трафика:
- JS/CSS/JSON/WASM
- динамические импорты
- WebSocket frames
- все response bodies

Запуск:
1. Создать Codespace
2. Открыть терминал
3. Выполнить: chmod +x start.sh
4. Запустить: ./start.sh