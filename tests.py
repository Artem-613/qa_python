from main import BooksCollector
import pytest

class TestBooksCollector:

    # Тест 1: Добавление новой книги (изолированный тест)
    def test_add_new_book(self, collector):
        collector.add_new_book('Новая книга')
        assert 'Новая книга' in collector.books_genre
        assert collector.books_genre['Новая книга'] == ''

    # Тест 2: Параметризованный тест длины названия
    @pytest.mark.parametrize('name, expected', [
        ('К' * 40, True),
        ('К' * 41, False),
        ('Книга', True),
        ('', False)
    ])
    def test_add_new_book_name_validation(self, collector, name, expected):
        collector.add_new_book(name)
        assert (name in collector.books_genre) == expected

    # Тест 3: Установка валидного жанра (прямая установка данных)
    def test_set_book_genre_valid(self, collector):
        collector.books_genre = {'Тестовая книга': ''}
        collector.set_book_genre('Тестовая книга', 'Фантастика')
        assert collector.books_genre['Тестовая книга'] == 'Фантастика'

    # Тест 4: Попытка установки невалидного жанра
    def test_set_book_genre_invalid(self, collector):
        collector.books_genre = {'Тестовая книга': ''}
        collector.set_book_genre('Тестовая книга', 'Несуществующий жанр')
        assert collector.books_genre['Тестовая книга'] == ''

    # Тест 5: Получение жанра книги (отдельный тест)
    def test_get_book_genre(self, collector):
        collector.books_genre = {'Книга 1': 'Фантастика', 'Книга 2': 'Ужасы'}
        assert collector.get_book_genre('Книга 1') == 'Фантастика'
        assert collector.get_book_genre('Книга 2') == 'Ужасы'
        assert collector.get_book_genre('Несуществующая') is None

    # Тест 6: Получение всего словаря книг (отдельный тест)
    def test_get_books_genre(self, collector):
        expected_dict = {'Книга 1': 'Фантастика', 'Книга 2': 'Детективы'}
        collector.books_genre = expected_dict
        assert collector.get_books_genre() == expected_dict

    # Тест 7: Фильтрация книг по жанру (прямая установка)
    def test_get_books_with_specific_genre(self, collector):
        collector.books_genre = {
            'Книга 1': 'Фантастика',
            'Книга 2': 'Детективы', 
            'Книга 3': 'Фантастика'
        }
        result = collector.get_books_with_specific_genre('Фантастика')
        assert result == ['Книга 1', 'Книга 3']

    # Тест 8: Получение детских книг (прямая установка)
    def test_get_books_for_children(self, collector):
        collector.books_genre = {
            'Детская': 'Мультфильмы',
            'Взрослая': 'Ужасы',
            'Нейтральная': 'Комедии'
        }
        result = collector.get_books_for_children()
        assert result == ['Детская', 'Нейтральная']

    # Тест 9: Добавление в избранное (прямая установка)
    def test_add_book_in_favorites(self, collector):
        collector.books_genre = {'Книга': 'Фантастика'}
        collector.add_book_in_favorites('Книга')
        assert 'Книга' in collector.favorites

    # Тест 10: Получение списка избранного (уникальный тест)
    def test_get_list_of_favorites_books(self, collector):
        collector.favorites = ['Книга 1', 'Книга 2', 'Книга 3']
        result = collector.get_list_of_favorites_books()
        assert result == ['Книга 1', 'Книга 2', 'Книга 3']

    # Тест 11: Удаление из избранного (прямая установка)
    def test_delete_book_from_favorites(self, collector):
        collector.favorites = ['Книга 1', 'Книга 2']
        collector.delete_book_from_favorites('Книга 1')
        assert collector.favorites == ['Книга 2']

    # Тест 12: Не добавляется несуществующая книга
    def test_add_non_existent_book_to_favorites(self, collector):
        collector.books_genre = {'Существующая': 'Фантастика'}
        collector.add_book_in_favorites('Несуществующая')
        assert 'Несуществующая' not in collector.favorites