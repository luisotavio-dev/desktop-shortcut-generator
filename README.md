# Desktop Shortcut Generator

Aplicativo desktop em **Python** e **PyQt6** para criar atalhos `.desktop` no Linux de forma simples, com interface gráfica e suporte a múltiplos idiomas.

Funciona em ambientes que seguem o padrão [FreeDesktop.org](https://specifications.freedesktop.org/) — **KDE Plasma**, **GNOME**, **XFCE**, **Cinnamon**, **MATE** e derivados (Fedora, Ubuntu, Bazzite, Arch, Linux Mint, etc.).

## Funcionalidades

- Interface gráfica para criar atalhos `.desktop`
- Campos: nome, executável, ícone (com pré-visualização), descrição e opção *Executar no Terminal*
- Validação de caminhos antes de salvar
- Detecção automática da pasta da área de trabalho via **XDG** (`user-dirs.dirs`)
- Fallback para `~/.local/share/applications` quando não há desktop configurado
- Suporte a atalhos confiáveis no **GNOME** (`metadata::trusted`)
- Internacionalização: **Português (Brasil)**, **Inglês** e **Espanhol**
- Detecção do idioma do sistema com fallback para inglês

## Requisitos

| Requisito | Versão mínima |
|-----------|---------------|
| Python | 3.11+ |
| PyQt6 | 6.4+ |
| gettext (`msgfmt`) | apenas para compilar traduções |

### Instalar dependências do sistema

**Fedora / Bazzite / RHEL:**

```bash
sudo dnf install python3 python3-pip gettext
```

**Ubuntu / Debian / Mint:**

```bash
sudo apt install python3 python3-pip python3-venv gettext
```

**Arch Linux:**

```bash
sudo pacman -S python python-pip gettext
```

## Como executar

### 1. Clonar o repositório

```bash
git clone https://github.com/SEU_USUARIO/desktop-shortcut-generator.git
cd desktop-shortcut-generator
```

Substitua `SEU_USUARIO` pela organização ou usuário real do GitHub quando o repositório estiver publicado.

### 2. Criar ambiente virtual (recomendado)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependências Python

```bash
pip install -r requirements.txt
```

### 4. Compilar traduções

```bash
python scripts/compile_translations.py
```

### 5. Executar o aplicativo

```bash
python -m desktop_shortcut_generator.main
```

Preencha o formulário, selecione o executável e a imagem do ícone, e clique em **Criar Atalho**. O arquivo `.desktop` será salvo na sua área de trabalho (se existir) ou no menu de aplicativos.

## Estrutura do projeto

```text
desktop_shortcut_generator/
├── config/           # Configurações globais (nome, versão, idiomas)
├── domain/           # Entidades e regras de negócio puras
├── use_cases/        # Casos de uso (orquestração)
├── infrastructure/   # I/O: escrita de arquivos, XDG, trust GNOME
├── presentation/     # Interface PyQt6
├── i18n/             # Traduções gettext (.po / .mo)
└── main.py           # Ponto de entrada

scripts/
└── compile_translations.py
```

O projeto segue **Clean Architecture**: a lógica de negócio não depende de PyQt6.

## Como contribuir

Contribuições são bem-vindas — correções, melhorias, traduções e documentação.

### 1. Fork e branch

```bash
git clone https://github.com/SEU_USUARIO/desktop-shortcut-generator.git
cd desktop-shortcut-generator
git checkout -b minha-feature
```

### 2. Configurar o ambiente de desenvolvimento

Siga os passos da seção [Como executar](#como-executar).

### 3. Fazer suas alterações

- Siga **PEP 8** e use **type hints** em código novo
- Mantenha a separação de camadas (`domain` não importa PyQt6)
- Adicione docstrings em classes e funções públicas
- Se alterar textos da interface, atualize **todos** os arquivos `.po` em `i18n/locales/`

### 4. Compilar traduções (se necessário)

```bash
python scripts/compile_translations.py
```

### 5. Testar localmente

```bash
python -m desktop_shortcut_generator.main
```

Verifique se o atalho é criado corretamente e se a interface está traduzida.

### 6. Commit e Pull Request

```bash
git add .
git commit -m "feat: descrição clara da mudança"
git push origin minha-feature
```

Abra um **Pull Request** no GitHub descrevendo o que foi feito e como testar.

### Ideias de contribuição

- Novos idiomas em `i18n/locales/`
- Melhorias de acessibilidade na interface
- Empacotamento Flatpak / Flathub
- Testes automatizados
- Correções de compatibilidade com ambientes desktop específicos

## Adicionar um novo idioma

1. Copie `desktop_shortcut_generator/i18n/locales/en/LC_MESSAGES/messages.po` para `locales/<código>/LC_MESSAGES/messages.po`
2. Traduza os `msgstr` e ajuste o cabeçalho `Language:`
3. Registre o idioma em `config/settings.py` → `SUPPORTED_LANGUAGES`
4. Execute `python scripts/compile_translations.py`

## Licença

Licença ainda não definida. Consulte o repositório para atualizações.
