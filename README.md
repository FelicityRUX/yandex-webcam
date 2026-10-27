<h1 style="text-align:center;">Камера + микрофон для Яндекс Станции 2</h1>

## Содержание
1. [Как работает](#1-Как-работает)
2. [Установка](#2-Установка)

---
## 1. Как работает
Вот диаграма чтобы было понятнее как скрипт работает

```mermaid
stateDiagram-v2
    state "Ты" as You
    state "ffmpeg" as FFM
    state "UDP колонки" as Reciever
    state "Колонка" as Speaker
    state "Обработка видео" as Video

    You --> FFM: Микрофон
    FFM --> Reciever: WAV поток → UDP, порт 8188
    You --> Video: Камера
    Video --> Reciever: Кадр в 13x15, получает нужные пиксели -> UDP, порт 8388
    Reciever --> Speaker: Поток производится с помощью aplay
    Reciever --> Speaker: Кадры пишутся в /dev/fb0
```
---
## 2. Установка
1. `git clone https://github.com/FelicityRUX/yandex-webcam.git`
2. host.py должен запускаться с пк
3. yandex.py должен запускаться с колонки

> [!TIP]
> Не сработало? Поменяй последовательность запуска скриптов.
---
написал крутой ридми как вам
