# image-classification-model
Image classification and(or) clusterisation model for UrFU hakaton

* Решаемая задача: сегментация текста из сканов чеков
* Используемая модель: tesseract 3(pytesseract)
* Язык текста: eng

## Локальный запуск модели

`python main.py --file <filename/path_to_folder>`

## Аргументы скрипта

* `--file` путь до файла со сканом jpg. Путь должен быть абсолютным. Если не вызывать параметр, программа не исполняется.