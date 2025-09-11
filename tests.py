from main import BooksCollector
import pytest

class TestBooksCollector:

    # Тест 1: Добавление двух книг
    def test_add_new_book_add_two_books(self, collector):
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        assert len(collector.get_books_genre()) == 2

    # Тест 2: Параметризованный тест на проверку граничных значений длины названия книги
    @pytest.mark.parametrize(
        'name, expected', 
        [
            ('К' * 40, True),      # 40 символов - максимально допустимая длина
            ('К' * 41, False),     # 41 символ - уже недопустимо
            ('Книга', True),       # нормальное название
            ('', False)            # пустое название - недопустимо
        ]
    )
    def test_add_new_book_different_name_lengths(self, collector, name, expected):
        collector.add_new_book(name)
        assert (name in collector.get_books_genre()) == expected

    # Тест 3: Установка валидного жанра для существующей книги
    def test_set_book_genre_valid_genre(self, collector):
        collector.add_new_book('Тестовая книга')
        collector.set_book_genre('Тестовая книга', 'Фантастика')
        assert collector.get_book_genre('Тестовая книга') == 'Фантастика'

    # Тест 4: Попытка установки недопустимого жанра
    def test_set_book_genre_invalid_genre(self, collector):
        collector.add_new_book('Тестовая книга')
        collector.set_book_genre('Тестовая книга', 'Несуществующий жанр')
        assert collector.get_book_genre('Тестовая книга') == ''  # Жанр должен остаться пустым

    # Тест 5: Получение книг с определенным жанром
    def test_get_books_with_specific_genre(self, collector):
        collector.add_new_book('Книга 1')
        collector.add_new_book('Книга 2')
        collector.set_book_genre('Книга 1', 'Фантастика')
        collector.set_book_genre('Книга 2', 'Детективы')
        
        fantasy_books = collector.get_books_with_specific_genre('Фантастика')
        assert 'Книга 1' in fantasy_books    # Книга с жанром Фантастика должна быть в списке
        assert 'Книга 2' not in fantasy_books  # Книга с другим жанром не должна быть в списке

    # Тест 6: Получение книг, подходящих для детей (без возрастного рейтинга)
    def test_get_books_for_children(self, collector):
        collector.add_new_book('Детская книга')
        collector.add_new_book('Взрослая книга')
        collector.set_book_genre('Детская книга', 'Мультфильмы')  # Жанр без возрастного рейтинга
        collector.set_book_genre('Взрослая книга', 'Ужасы')       # Жанр с возрастным рейтингом
        
        children_books = collector.get_books_for_children()
        assert 'Детская книга' in children_books    # Должна быть в списке для детей
        assert 'Взрослая книга' not in children_books  # Не должна быть в списке для детей

    # Тест 7: Добавление существующей книги в избранное
    def test_add_book_in_favorites(self, collector):
        collector.add_new_book('Избранная книга')
        collector.add_book_in_favorites('Избранная книга')
        assert 'Избранная книга' in collector.get_list_of_favorites_books()

    # Тест 8: Попытка добавления несуществующей книги в избранное
    def test_add_non_existent_book_to_favorites(self, collector):
        collector.add_book_in_favorites('Несуществующая книга')
        assert 'Несуществующая книга' not in collector.get_list_of_favorites_books()

    # Тест 9: Удаление книги из избранного
    def test_delete_book_from_favorites(self, collector):
        collector.add_new_book('Книга для удаления')
        collector.add_book_in_favorites('Книга для удаления')
        collector.delete_book_from_favorites('Книга для удаления')
        assert 'Книга для удаления' not in collector.get_list_of_favorites_books()

    # Тест 10: Получение полного списка избранных книг
    def test_get_list_of_favorites_books(self, collector):
        collector.add_new_book('Книга 1')
        collector.add_new_book('Книга 2')
        collector.add_book_in_favorites('Книга 1')
        collector.add_book_in_favorites('Книга 2')
        
        favorites = collector.get_list_of_favorites_books()
        assert 'Книга 1' in favorites      # Обе книги должны быть в избранном
        assert 'Книга 2' in favorites
        assert len(favorites) == 2         # В избранном должно быть 2 книги
