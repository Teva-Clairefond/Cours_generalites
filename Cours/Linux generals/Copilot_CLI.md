# GITHUB COPILOT CLI

## Installation :

### Installation de NVM :

NVM (Node.js Version Manager) est le controleur de version de Node.js

```bash
export PROFILE="$HOME/.bashrc"
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
# Chargement de NVM dans le shell :
source ~/.bashrc
nvm install 24
```
npm s'installe automatiquement avec nvm

### Installation de github :

```bash
npm install -g @github/copilot
```

### Premier lancement :

```bash
copilot
```

Pour s'authentifier :
```bash
/login
```

