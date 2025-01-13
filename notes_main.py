#Это мой первый проект на GitHub
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QApplication, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QListWidget, QTextEdit, QInputDialog
import json

notes = {
    'Добро пожаловать!': {
        'текст': 'Это самое лучшее приложение для заметок в мире!',
        'теги': ['добро', 'инструкция']
    }
}

def show_results():
    data = notes_list.selectedItems()[0].text()
    text_field.setText(notes[data]['текст'])
    tegs_list.clear()
    tegs_list.addItems(notes[data]['теги'])

def add_note():
    note_name, ok = QInputDialog.getText(main_window, 'Название заметки', 'Название заметки')
    if note_name != '' and ok != '':
        notes[note_name] = {'текст': '', 'теги': []}
        notes_list.addItem(note_name)
        tegs_list.addItems(notes[note_name]['теги'])

def del_note():
    if notes_list.selectedItems():
        note = notes_list.selectedItems()[0].text()
        del notes[note]
        notes_list.clear()
        tegs_list.clear()
        text_field.clear()
        notes_list.addItems(notes)
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file)
    else:
        print('Заметка для удаления не выбрана')

def save_note():
    if notes_list.selectedItems():
        note = notes_list.selectedItems()[0].text()
        notes[note]['текст'] = text_field.toPlainText()
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file)
    else:
        print('Заметка для сохранения не выбрана')

def add_tag():
    if notes_list.selectedItems():
        note = notes_list.selectedItems()[0].text()
        new_tag = add_teg.text()
        if not new_tag in notes[note]['теги']:
            notes[note]['теги'].append(new_tag)
            tegs_list.addItem(new_tag)
            add_teg.clear()
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file)
    else:
        print('Заметка для добавления тега не выбрана')

def del_tag():
    if notes_list.selectedItems() and tegs_list.selectedItems():
        note = notes_list.selectedItems()[0].text()
        tag = tegs_list.selectedItems()[0].text()
        notes[note]['теги'].remove(tag)
        tegs_list.clear()
        tegs_list.addItems(notes[note]['теги'])
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file)
    else:
        print('Заметка и/или тег для удаления не выбран')

def search_tag():
    tag = add_teg.text()
    if find_notes.text() == 'Искать заметки по тегу':
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]['теги']:
                notes_filtered[note] = notes[note]
        find_notes.setText('Сбросить поиск')
        notes_list.clear()
        tegs_list.clear()
        notes_list.addItems(notes_filtered)
    elif find_notes.text() == 'Сбросить поиск':
        notes_list.clear()
        add_teg.clear()
        notes_list.addItems(notes)
        find_notes.setText('Искать заметки по тегу')

app = QApplication([])
main_window = QWidget()
main_window.setWindowTitle('Умные заметки')
main_window.resize(900, 600)

text_field = QTextEdit()
notes_list = QListWidget()
notes_list_label = QLabel('Список заметок')
button_add_note = QPushButton('Создать заметку')
button_del_note = QPushButton('Удалить заметку')
button_save_note = QPushButton('Сохранить заметку')
tegs_list = QListWidget()
tegs_list_label = QLabel('Список тегов')
add_teg = QLineEdit()
add_teg.setPlaceholderText('Введите тег')
add_to_note = QPushButton('Добавить к заметке')
del_from_note = QPushButton('Открепить от заметки')
find_notes = QPushButton('Искать заметки по тегу')

leftVline = QVBoxLayout()
leftVline.addWidget(text_field)
centralVline = QVBoxLayout()
centralVline.addWidget(notes_list_label)
centralVline.addWidget(notes_list)

Hline3 = QHBoxLayout()
Hline3.addWidget(button_add_note)
Hline3.addWidget(button_del_note)
Hline4 = QHBoxLayout()
Hline4.addWidget(button_save_note)
centralVline.addLayout(Hline3)
centralVline.addLayout(Hline4)

centralVline.addWidget(tegs_list_label)
centralVline.addWidget(tegs_list)
centralVline.addWidget(add_teg)

Hline8 = QHBoxLayout()
Hline8.addWidget(add_to_note)
Hline8.addWidget(del_from_note)
Hline9 = QHBoxLayout()
Hline9.addWidget(find_notes)
centralVline.addLayout(Hline8)
centralVline.addLayout(Hline9)

main_layout = QHBoxLayout()
main_layout.addLayout(leftVline)
main_layout.addLayout(centralVline)
main_window.setLayout(main_layout)

try:
    with open('notes_data.json', 'r') as file:
        notes = json.load(file)
except:
    print('Файл заметок не обнаружен')
notes_list.addItems(notes)
notes_list.itemClicked.connect(show_results)
button_add_note.clicked.connect(add_note)
button_del_note.clicked.connect(del_note)
button_save_note.clicked.connect(save_note)
add_to_note.clicked.connect(add_tag)
del_from_note.clicked.connect(del_tag)
find_notes.clicked.connect(search_tag)
main_window.show()
app.exec_()
