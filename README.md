# Password-Manager

Password Manager (GUI - CustomTkinter)
Applicazione desktop per la gestione sicura delle password, sviluppata in Python con interfaccia grafica basata su CustomTkinter.

L'app consente di:
    •	Salvare credenziali (website, username, password)
    •	Generare password sicure
    •	Cercare e recuperare credenziali
    •	Gestire e cancellare entries
    •	Proteggere i dati tramite crittografia AES

Funzionalità principali
Autenticazione (Master Password)
    •	Primo avvio:
        o	L'utente imposta una master password
        o	La password viene crittografata (AES) e salvata in data.json
    •	Accessi successivi:
        o	L'input viene verificato con la password salvata
        o	Accesso consentito solo in caso di match

Gestione credenziali
    •	Aggiunta di nuove entries:
        o	Website/App
        o	Email/Username
        o	Password
    •	Logica intelligente:
        o	Nuovo sito → aggiunta completa
        o	Sito esistente + nuovo utente → aggiunta utente
        o	Sito + utente già esistenti → richiesta conferma per sovrascrivere password

Ricerca
    •	Ricerca per:
        o	Website
        o	Website + Username
    •	Output:
        o	Password decrittografata
        o	Copiata automaticamente negli appunti
    •	Se viene inserito solo il website:
        o	Mostra tutte le utenze associate

Sicurezza
    •	Tutte le password vengono:
        o	Criptate con AES usando cryptography.hazmat
        o	Salvate in data.json
    •	Decrittazione solo al momento della visualizzazione

Generatore password
    •	Genera password robuste con:
        o	Lettere maiuscole e minuscole
        o	Numeri
        o	Caratteri speciali
    •	Lunghezza adeguata per sicurezza elevata

User Experience
    •	GUI moderna con CustomTkinter
    •	Autocomplete per:
        o	Website
        o	Username
    •	Shortcut da tastiera per azioni rapide
    •	Validazione input:
        o	Campi obbligatori
        o	Messaggi di errore e warning
    •	Conferme per operazioni critiche (es. delete)

Architettura del progetto
L'app è suddivisa in 3 macro moduli principali:

1. main.py
    •	Entry point dell'applicazione
    •	Inizializza la classe App
    •	Determina lo stato dell'app:
        o	stato = 0 → primo accesso
        o	stato = 1 → accesso successivo

2. window_login.py
    •	Contiene la classe LoginApp
    •	GUI per login/master password
    •	Interazione con LoginFunctions
Logica:
    •	Input utente → LoginFunctions.verify
    •	Se:
        o	corretto → apre MainApp
        o	errato → mostra errore

3. app.py
    •	Contiene la classe MainApp
    •	GUI principale del password manager
    •	Gestione di:
        o	Aggiunta
        o	Ricerca
        o	Eliminazione
        o	Generazione password

Moduli secondari
    •	cryptography.py
        o	Funzioni di:
            	encrypt_password
            	decrypt_password
    •	autocomplete.py
        o	Classe Autocomplete
        o	Suggerimenti dinamici durante la digitazione
    •	Altri moduli:
        o	Utility
        o	Validazione input
        o	Gestione JSON

Struttura dati
Il file data.json viene creato automaticamente nella stessa directory di main.py.
Esempio struttura:
{
  "master": {
“salt”: "<encrypted>",
“hash”: "<encrypted>"
},
  "entries": {
    	"example.com": {
      		"email": "<encrypted_password>",
      		"password": "<encrypted_password>",
      		"nonce": "<encrypted_nonce>"
    	}
  }
}

Avvio dell'applicazione
Requisiti
    •	Python 3.x
    •	Librerie necessarie:
    •	pip install customtkinter cryptography
Esecuzione
python main.py

Validazioni e controlli
L'app include:
    •	Controllo campi vuoti
    •	Prevenzione duplicati
    •	Conferma eliminazioni
    •	Gestione errori login
    •	Input validation avanzata

Shortcut da tastiera
    •	I principali bottoni sono bindati a tasti per:
        o	Login
        o	Aggiunta
        o	Ricerca
        o	Eliminazione
(esperienza user friendly)

Note importanti
    •	Il file data.json contiene dati sensibili (anche se criptati)
    •	Non condividere il file
    •	La sicurezza dipende dalla robustezza della master password

Possibili miglioramenti
    •	Backup automatico
    •	Sincronizzazione cloud
    •	Multi-account
    •	2FA (autenticazione a due fattori)
    •	UI/UX enhancements
