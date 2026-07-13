# Wissensbasis für Config B (RAG)

Lege hier **dieselben Rohdokumente** ab, die auch das agentische System (Config A) nutzt.

Unterstützte Formate (via LlamaIndex `SimpleDirectoryReader`): `.txt`, `.md`, `.pdf`, `.docx`, `.html` u. a.

Nach dem ersten Lauf wird der Index in `../rag_index/` persistiert. Zum Neuaufbau den Ordner `rag_index/` löschen.
