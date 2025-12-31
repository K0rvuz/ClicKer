# 🖱️ ClicKer

**ClicKer** é uma aplicação desktop para **automação visual**, capaz de identificar imagens na tela e executar cliques automaticamente quando elas aparecem.

O projeto foi desenvolvido em **Python + PySide6**, com foco em:
- performance
- interface moderna
- facilidade de uso
- distribuição profissional via instalador

---

##  Funcionalidades

-  Reconhecimento de imagens na tela (OpenCV)
-  Clique automático ao detectar a imagem
-  Banco de imagens local (pasta `imagens`)
-  Contador de cliques por imagem
-  Drag & Drop de imagens direto na interface
-  Interface minimalista com modo escuro
-  Indicador visual de **Rodando / Parado**
-  Executável rápido (Nuitka Standalone)
-  Instalador profissional (Inno Setup)

---

##  Interface

- Design limpo e escuro  
- Botões com bordas arredondadas  
- Área dedicada para arrastar imagens  
- Lista com contagem de cliques em tempo real  

> O layout foi pensado para ser simples, funcional e sem distrações.

---

##  Tecnologias Utilizadas

- **Python 3.12**
- **PySide6 (Qt for Python)**
- **PyAutoGUI**
- **OpenCV**
- **Nuitka (standalone)**
- **Inno Setup**

---

##  Instalação (Usuário Final)

1. Baixe o arquivo `ClicKerInstaller.exe`
2. Execute o instalador
3. Um atalho será criado na área de trabalho
4. Abra o ClicKer normalmente

 Não é necessário Python instalado  
 Não é necessário configurar nada manualmente  

---

##  Como Usar

1. Abra o **ClicKer**
2. Adicione imagens:
   - Clique em **Adicionar**
   - ou arraste imagens para a área de Drop
3. Clique em **Iniciar**
4. O programa irá:
   - monitorar a tela
   - clicar automaticamente quando encontrar as imagens
5. Clique em **Parar** para encerrar a automação

---

## 📁 Estrutura do Projeto

```text
ClicKer/
├── Installer/ClicKerInstaller.exe
├── ClicKer.py
├── imagens/
├── assets/
│   └── clicker.ico
├── ClicKer.dist/
├── ClicKer.iss
└── README.md
```

---

## ⚙️ Build do Executável (Desenvolvedores)

### Gerar executável standalone com Nuitka

```bat
python -m nuitka ClicKer.py --standalone --enable-plugin=pyside6 --enable-plugin=numpy --windows-console-mode=disable --windows-icon-from-ico=assets/clicker.ico --include-data-dir=imagens=imagens --assume-yes-for-downloads --lto=yes --msvc=latest
```

### Gerar instalador com Inno Setup

```bat
"C:\Program Files\Inno Setup 6\ISCC.exe" "ClicKer.iss"
```

---

##  Segurança & Antivírus

Por se tratar de um software de automação (controle de mouse), alguns antivírus podem emitir alertas iniciais.

 O código é aberto e pode ser auditado  
 Não há coleta de dados  
 Nenhuma ação ocorre sem o usuário iniciar  

---

##  Licença

Este projeto é distribuído sob a licença **MIT**.  
Sinta-se livre para usar, modificar e distribuir.

---

##  Autor

**Korvuz**  
🔗 GitHub: https://github.com/K0rvuz

---

##  Contribuições

Pull requests são bem-vindos!  
Se tiver ideias, sugestões ou melhorias, fique à vontade para contribuir.

---

> Projeto desenvolvido com foco em aprendizado profundo sobre automação, interfaces gráficas e distribuição profissional de software em Python.
