# CB Wrapper
**CB Wrapper** est un module python vous permettant de traduire des fichiers JSON à l'aide de l'API ModernMT.

![Python package](https://github.com/Leynaic/CB-Test-Technique/workflows/Python%20package/badge.svg?branch=main)

## Exemple d'utilisation
```python
from cb_wrapper import APIModern

files = (os.path.relpath('file_en.json'), os.path.relpath('file2_en.json'))

try:
    api = APIModern()
    api.translate('fr', files, source='en', path=os.path.relpath('translated'))
except Exception as e:
    print(e)
```

Les fichiers traduits se retrouverons dans le même dossier que ceux passés en paramètre. \
Pour éviter cela, vous pouvez indiquer le dossier de destination des fichiers traduits en passant un `path=` en paramètre. \
Il est également conseillé d'indiquer la langue source pour éviter que l'API ne reconnaisse pas la langue.

## Installer CB Wrapper

Pour utiliser CB Wrapper vous devez clôner le dépôt, et utiliser la commande suivante :

```console
pip install -e le_chemin_du_depot
```

N'oubliez pas de créer un fichier `config.yaml` et insérer la ligne suivante :
```yaml
api_key: "change me"
```
