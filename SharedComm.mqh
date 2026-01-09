//+------------------------------------------------------------------+
//|                                                   SharedComm.mqh |
//|                                  Copyright 2026, Antigravity AI  |
//|                 SOVEREIGN SHARED LOG: ZERO-BLOCK ENGINE v15.0    |
//+------------------------------------------------------------------+
#ifndef SOVEREIGN_SHARED_COMM_MQH
#define SOVEREIGN_SHARED_COMM_MQH

#include <Files\FileTxt.mqh>

namespace Sovereign {
    class SharedComm {
    private:
        static string m_buffer;
        static ulong  m_last_flush;
        static string m_last_read_cache;
        static ulong  m_last_read_time;

    public:
        // --- 🧵 ZERO-BLOCK LOGGING (v15.0) ---
        // Implementa um buffer circular em memória p/ evitar IO millisecond
        static void WriteLog(string msg) {
            if(msg == "" || MQLInfoInteger(MQL_TESTER)) return;
            
            m_buffer += "[" + TimeToString(TimeCurrent(), TIME_SECONDS) + "] " + msg + "\n";
            
            // Flush otimizado: Só grava se houver dados e o timer ou tamanho permitir
            if(StringLen(m_buffer) > 1024 || GetTickCount64() - m_last_flush > 2000) {
                Flush();
            }
        }
        
        static void Flush() {
            if(m_buffer == "") return;
            
            // Uso de FILE_SHARE_READ|FILE_SHARE_WRITE evita o bloqueio do PC
            int h = FileOpen("Sovereign_Shared_Log.txt", FILE_READ|FILE_WRITE|FILE_TXT|FILE_SHARE_READ|FILE_SHARE_WRITE|FILE_COMMON);
            if(h != INVALID_HANDLE) {
                FileSeek(h, 0, SEEK_END);
                FileWriteString(h, m_buffer);
                FileClose(h);
                m_buffer = "";
                m_last_flush = GetTickCount64();
            }
        }
        
        static string ReadLog() {
            // PERFORMANCE: Cache de leitura (Só abre o arquivo a cada 1.5s)
            if(GetTickCount64() - m_last_read_time < 1500) return m_last_read_cache;
            
            int h = FileOpen("Sovereign_Shared_Log.txt", FILE_READ|FILE_TXT|FILE_SHARE_READ|FILE_SHARE_WRITE|FILE_COMMON);
            string msg = "";
            if(h != INVALID_HANDLE) {
                // Lê apenas as últimas linhas (v15.0 Optimization)
                ulong size = FileSize(h);
                if(size > 1000) FileSeek(h, -1000, SEEK_END);
                
                while(!FileIsEnding(h)) {
                    msg += FileReadString(h) + "\n";
                }
                FileClose(h);
                m_last_read_cache = msg;
                m_last_read_time = GetTickCount64();
            }
            return msg;
        }
    };
    
    string SharedComm::m_buffer = "";
    ulong  SharedComm::m_last_flush = 0;
    string SharedComm::m_last_read_cache = "";
    ulong  SharedComm::m_last_read_time = 0;
}

#endif
