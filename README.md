# Voice Typing

## Linux setup

```bash
sudo apt install python3-full pipx
pipx install poetry
poetry install
poetry run pre-commit install
```

## Windows setup

See [documentation](https://gist.github.com/Isfhan/b8b104c8095d8475eb377230300de9b0)

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

And add this to your PATH

```path
C:\Users\pea\AppData\Roaming\Python\Scripts\poetry
```

## Execution

``` bash
poetry run voice-typing
```
