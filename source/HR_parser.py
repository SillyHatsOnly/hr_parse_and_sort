import os
from striprtf.striprtf import rtf_to_text
#import string

main_path = 'C:\\HR'


# считываем все имена файлов из папки
def get_file_names(folder_path):
    file_paths = [f.path for f in os.scandir(folder_path) if not f.is_dir()]
    file_names = [{'name': os.path.basename(f)} for f in file_paths]

    return file_names


# читаем текст из файла
def get_encoded_files(file_names):
    error_files_dict = {}
    for file in file_names:
        with open(os.path.join(main_path, file['name'])) as f:
            try:
                file['text'] = rtf_to_text(f.read())
            except UnicodeEncodeError:
                error_files_dict[file['name']] = 'UnicodeEncodeError'
            except UnicodeDecodeError:
                error_files_dict[file['name']] = 'UnicodeDecodeError'

    return file_names, error_files_dict


# ищем профессию
def get_prof(files):
    ruPr = 'Желаемая должность и зарплата|'
    engPr = 'Desired position and salary|'
    ruE = 'Занятость:'
    engE = 'Employment:'
    err_symb = '''."[]:;|=,?"/\\<>*|:'''
    #string.punctuation

    for person in files:
        prIndex, emIndex, suf = 0, 0, 0
        if 'text' in person:
            if person['text'].find(ruPr) != -1:
                prIndex = person['text'].index(ruPr)
                suf = len(ruPr)
                emIndex = person['text'].find(ruE)
            elif person['text'].find(engPr) != -1:
                prIndex = person['text'].index(engPr)
                suf = len(engPr)
                emIndex = person['text'].find(engE)

            prof = person['text'][prIndex+suf:emIndex].strip().split('\n')[0]

            if len(prof) <= 140:
                prof = prof.translate({ord(i): ' ' for i in prof if i in err_symb})
                person['prof'] = ' '.join(prof.split()).lower()
            else:
                print('\nУКАЗАНО В РЕЗЮМЕ: \n\n', person['text'][prIndex+suf:emIndex].strip())
                print()
                tempProf = input('Укажите специальность (до 140 знаков): ')
                print('---------------------------------------------------------')
                person['prof'] = tempProf.strip().lower()

    return files


# создаём папки с названиями из словаря/списка
def create_folders_from_list(folder_path, folder_names):
    for folder in folder_names:
        if 'prof' in folder:
            if not os.path.exists(os.path.join(folder_path, folder['prof'])):
                os.mkdir(os.path.join(folder_path, folder['prof']))
        else:
            if not os.path.exists(os.path.join(folder_path, 'прочее')):
                os.mkdir(os.path.join(folder_path, 'прочее'))


def get_file_paths(folder_path):
    file_paths = [f.path for f in os.scandir(folder_path) if not f.is_dir()]

    return file_paths


# сортировка и перемещение файлов
def sort_files(folder_path, files):
    for file in files:
        if 'prof' in file:
            new_file_path = file['prof'].strip()
            os.replace(os.path.join(main_path, file['name']), os.path.join(main_path, new_file_path, file['name']))
        else:
            os.replace(os.path.join(main_path, file['name']),os.path.join(main_path, 'прочее', file['name']))


if __name__ == '__main__':
    files, err = get_encoded_files(get_file_names(main_path))
    files = get_prof(files)
    for i in files:
        if len(i)>1:
            print(i['name'], ': ', i['prof'])
        else:
            print('########## ОШИБКА ПРИ РАБОТЕ С ФАЙЛОМ: ', i['name'])
    print()
    while True:
        q = input('Проверьте данные. Если всё верно, для продолжения введите YES. Иначе введите NO. ')
        if q.lower() == 'yes':
            break
        elif q.lower() == 'no':
            print('Программа была завершена.')
            exit()
        else:
            print('Неверно введена ккоманда. Попробуйте ещё раз.')

    create_folders_from_list(main_path, files)
    sort_files(main_path, files)

    print()
    print('Файлы, которые не удалось прочитать (перемещены в папку ПРОЧЕЕ):')
    print()
    for i in err:
        print(i)
