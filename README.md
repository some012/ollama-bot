# Подготовка

Cоздать файл .env и добавить туда наподобии .env.example свой токен, взятый у BotFather в Telegram

```python

python -m venv venv

source .venv/bin/activate.fish

pip install -r requirements.txt

```
После установки Ollama и выбора необходимой модели

```python
python run.py
```

### Бот запускается локально, краткие инструкции уложены здесь, либо же их можно найти в полном виде в документации Ollama:

### https://github.com/ollama/ollama/blob/main/docs/linux.md

### https://github.com/ollama/ollama/blob/main/docs/windows.md



# Ollama на Linux

## Установка

Чтобы установить Ollama, выполните следующие команды:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

## Ручная установка

Скачайте и разархивируйте пакет:

```bash
curl -L https://ollama.com/download/ollama-linux-amd64.tgz -o ollama-linux-amd64.tgz
sudo tar -C /usr -xzf ollama-linux-amd64.tgz
```

Запустите Ollama:

```bash
ollama serve
```

В другом терминале проверьте, что Ollama работает:

```bash
ollama -v
```

## Установка на AMD GPU 

Если у вас есть AMD GPU, скачайте и разархивируйте дополнительный пакет ROCm:

```bash
curl -L https://ollama.com/download/ollama-linux-amd64-rocm.tgz -o ollama-linux-amd64-rocm.tgz
sudo tar -C /usr -xzf ollama-linux-amd64-rocm.tgz
```

## Установка на ARM64 

Скачайте и разархивируйте пакет для ARM64:

```bash
curl -L https://ollama.com/download/ollama-linux-arm64.tgz -o ollama-linux-arm64.tgz
sudo tar -C /usr -xzf ollama-linux-arm64.tgz
```

## Добавление Ollama в качестве сервиса запуска (рекомендуется)

Создайте пользователя и группу для Ollama:

```bash
sudo useradd -r -s /bin/false -U -m -d /usr/share/ollama ollama
sudo usermod -a -G ollama $(whoami)
```

Создайте файл конфигурации сервиса в `/etc/systemd/system/ollama.service`:

```ini
[Unit]
Description=Описание сервиса Ollama
After=network-online.target

[Service]
ExecStart=/usr/bin/ollama serve
User=ollama
Group=ollama
Restart=always
RestartSec=3
Environment="ПУТЬ=$PATH"

[Install]
WantedBy=default.target
```

Затем запустите сервис:

```bash
sudo systemctl daemon-reload
sudo systemctl enable ollama
```

## Установка драйверов CUDA (необязательно)

Скачайте и установите [CUDA](https://developer.nvidia.com/cuda-downloads).

Проверьте, что драйверы установлены, выполнив команду:

```bash
nvidia-smi
```

## Запуск Ollama

Запустите Ollama:

```bash
sudo systemctl start ollama
sudo systemctl status ollama
```

## Удаление

Удалите файл конфигурации сервиса:

```bash
sudo systemctl stop ollama
sudo systemctl disable ollama
sudo rm /etc/systemd/system/ollama.service
```

Удалите двоичный файл Ollama из каталога bin (или `/usr/local/bin`, `/usr/bin` или `/bin`):

```bash
sudo rm $(which ollama)
```

Удалите скачанные модели и пользователя-уživелеc Ollama:

```bash
sudo rm -r /usr/share/ollama
sudo userdel ollama
sudo groupdel ollama
```


# Ollama для Windows

Нет необходимости использовать WSL!


## Требования к системе

* Windows 10 22H2 или новее, Home или Pro
* NVIDIA 452.39 или новее Драйвера, если у вас есть видеокарта NVIDIA
* Драйвер Radeon https://www.amd.com/en/support, если у вас есть карта Radeon


## Требования к файловой системе

Установка Олламы не требует прав администратора и устанавливается по умолчанию в домашней папке.  Для установки Олламы требуется хотя бы 4 ГБ свободного места на диске. После установления Олламы потребуется дополнительное место для хранения больших языковых моделей, которые могут занимать десятки или сотни гигабайт в размере. Если ваша домашняя папка не имеет достаточно пространства, вы можете изменить местоположение установки Олламы и места, где хранятся модели.

### Изменение местоположения установки

Чтобы установить приложение Олламы в другом месте, чем домашняя папка, запустите установщик с следующей флагом:

powershell
ОllamaSetup.exe /DIR="d:\some\location"

### Изменение местоположения моделей

Чтобы изменить местоположение, где Оллама хранит загруженные модели вместо использования домашней папки, задайте переменную среды OLLAMA_MODELS в вашем аккаунте.

1. Начните настройку (Windows 11) или панель управления (Windows 10) и найдите _переменные среды_.

2. Нажмите кнопку редактирования переменных среды для вашего учетной записи.

3. Редактируйте или создайте новую переменную для вашей учетной записи для OLLAMA_MODELS, где вы хотите хранить модели

4. Кликните ОК/Применить, чтобы сохранить.

Если Оллама уже запущена, закройте приложение из трея и перезапустите его из меню "Пуск", или новое терминальное окно после того, как вы сохранили переменные среды.



## Удаление

Установщик Олламы зарегистрирует приложение для удаления.  В разделе "Добавить/удалить программы" в настройках Windows вы можете удалить Олламу.

> [!Примечание]
> Если вы [изменили местоположение OLLAMA_MODELS](#Changing_model_location), установщик не удаляет загруженные модели

