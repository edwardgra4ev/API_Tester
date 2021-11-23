from typing import Optional
import random

import requests
from rich.console import Console


class BaseNumberAPI(object):
    """Основной класс для NumberAPI от которого наследуются все остальные"""
    _CONSTANT_BASE_URL = 'http://numbersapi.com/{0}'
    _CONSTANT_A = 1
    _CONSTANT_B = 9999
    _CONSTANT_DATE_A = 1
    _CONSTANT_DATE_B = 31
    _CONSTANT_MONTH_A = 1
    _CONSTANT_MONTH_B = 12

    def _create_random_str_number(self) -> str:
        return str(random.randint(self._CONSTANT_A, self._CONSTANT_B))

    def _create_random_str_date(self) -> str:
        return str(random.randint(self._CONSTANT_DATE_A, self._CONSTANT_DATE_B))

    def _create_random_str_month(self) -> str:
        return str(random.randint(self._CONSTANT_MONTH_A, self._CONSTANT_MONTH_A))

    def _is_int(self, number) -> bool:
        try:
            int(number)
            return True
        except TypeError:
            raise ValidationError("number cannot be converted to a int")

    def _print_testing_response(self, result):
        """Функиця вывода результата тестирования в консоль"""
        console = Console()
        console.print("Результат тестирования метода Trivia для NumberAPI:", style="bold white")
        for key, values in result.items():
            if values[1] is True:
                console.print(f"{key}: {values[0]}", style="bold green")
            else:
                console.print(f"{key}: {values[0]}", style="bold red")

    def _testing_response(self, response: requests, number: str):
        """
        Функция тестирования выполнения HTTP запроса.
        Проверяет что status_code = 200 и что по запрашиваему числу есть результат.
        """
        result = {}
        status_code = response.status_code
        text = response.text
        # Код ответа
        if status_code == 200:
            result.update({"status_code": [status_code, True]})
        else:
            result.update({"status_code": [status_code, False]})
        # Есть ли ответ на это число
        false_answer = [f"{number} is an uninteresting number.", f"{number} is a boring number.",
                        f"{number} is an unremarkable number.", f"{number} is a number "
                        f"for which we're missing a fact (submit one to numbersapi at google mail!)."]
        if text in false_answer:
            result.update({"response_text": [text, False]})
        else:
            result.update({"response_text": [text, True]})
        return result


class Random(BaseNumberAPI):
    """ 23/11/2021 Eduard Grachev
     Класс реализующий работу с методом RANDOM для API Numbers
     """
    def __init__(self, *, method: str):
        self._method = method
        self._dictionary_methods = {
            'trivia': "random/trivia",
            'year': "random/year",
            'date': "random/date",
            'math': "random/math",
        }

    def __repr__(self):
        self._data_validation()
        return self._execute_http_request()

    def _data_validation(self) -> bool:
        """
        Функция валидации данных.
        Проверяет что self._method = str преобразует строку в нижний регистр
        и что есть такой ключ в словаре методов.
        В противном случаии вызывает raise RandomValidationError
        """
        if isinstance(self._method, str):
            self._method = self._method.lower()
            if self._method in self._dictionary_methods.keys():
                return True
        raise ValidationError()

    def _execute_http_request(self):
        """
        Функция HTTP запроса на API
        Получает метод из словаря методов. Формирует конечный URL. Выполняет get запрос к API и если статус ответа 200
        возвращает полученный результат
        В противном случаии вызывает raise ResponseStatusCodeError с указанием кода ответа
        :return:
        """
        url = self._CONSTANT_BASE_URL.format(self._dictionary_methods.get(self._method))
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        raise ResponseStatusCodeError(response.status_code)


class Trivia(BaseNumberAPI):
    """ 23/11/2021 Eduard Grachev
    Класс реализующий работу с методом Trivia для API Numbers
    """
    def __init__(self, *, number: Optional[int or str] = None, testing: Optional[bool] = False):
        self._number = number
        self._testing = testing

    def _execute_http_request(self) -> str or dict:
        """
        Функция вполенния запроса к API
        Если требуеться тестирование вызывает _testing_response(response) и возвращает словарь.
        Если тестирование не требуеться возвращает ответ от API
        """
        url = self._CONSTANT_BASE_URL.format(f"{self._number}/trivia")
        response = requests.get(url)
        if self._testing is True:
            return self._testing_response(response, self._number)
        if response.status_code == 200:
            return response.text
        raise ResponseStatusCodeError(response.status_code)

    def main(self) -> str or None:
        """Основаная функция класса"""
        if self._number is None:
            self._number = self._create_random_str_number()
        elif self._is_int(self._number):
            self._number = str(self._number)
        else:
            raise ValidationError()
        result = self._execute_http_request()
        if isinstance(result, str):
            return result
        else:
            self._print_testing_response(result)


class Math(BaseNumberAPI):
    """ 23/11/2021 Eduard Grachev
    Класс реализующий работу с методом Math для API Numbers
    """
    def __init__(self, *, number: Optional[int or str] = None, testing: Optional[bool] = False):
        self._number = number
        self._testing = testing

    def _execute_http_request(self) -> str or dict:
        """
        Функция вполенния запроса к API
        Если требуеться тестирование вызывает _testing_response(response) и возвращает словарь.
        Если тестирование не требуеться возвращает ответ от API
        """
        url = self._CONSTANT_BASE_URL.format(f"{self._number}/math")
        response = requests.get(url)
        if self._testing is True:
            return self._testing_response(response, self._number)
        if response.status_code == 200:
            return response.text
        raise ResponseStatusCodeError(response.status_code)

    def main(self) -> str or None:
        """Основаная функция класса"""
        if self._number is None:
            self._number = self._create_random_str_number()
        elif self._is_int(self._number):
            self._number = str(self._number)
        else:
            raise ValidationError()
        result = self._execute_http_request()
        if isinstance(result, str):
            return result
        else:
            self._print_testing_response(result)


class Date(BaseNumberAPI):
    """ 23/11/2021 Eduard Grachev
    Класс реализующий работу с методом Date для API Numbers
    """
    def __init__(self, *, date: Optional[int or str] = None, month: Optional[int or str] = None,
                 testing: Optional[bool] = False):
        self._date = date
        self._month = month
        self._testing = testing

    def _testing_response(self, response: requests):
        """
        Функция тестирования выполнения HTTP запроса.
        Проверяет что status_code = 200 и что по запрашиваему числу есть результат.
        """
        result = {}
        status_code = response.status_code
        text = response.text
        # Код ответа
        if status_code == 200:
            result.update({"status_code": [status_code, True]})
        else:
            result.update({"status_code": [status_code, False]})
        # Есть ли ответ на это число
        false_answer = 'undefined NaNth is the day that no newsworthy events happened.'
        if text == false_answer:
            result.update({"response_text": [text, False]})
        else:
            result.update({"response_text": [text, True]})
        return result

    def _execute_http_request(self) -> str or dict:
        """
        Функция вполенния запроса к API
        Если требуеться тестирование вызывает _testing_response(response) и возвращает словарь.
        Если тестирование не требуеться возвращает ответ от API
        """
        url = self._CONSTANT_BASE_URL.format(f"{self._month}/{self._date}/date")
        response = requests.get(url)
        if self._testing is True:
            return self._testing_response(response)
        if response.status_code == 200:
            return response.text
        raise ResponseStatusCodeError(response.status_code)

    def main(self) -> str or None:
        """Основаная функция класса"""
        if self._date is not None:
            if self._is_int(self._date):
                self._date = str(self._date)
            else:
                raise ValidationError()
        elif self._date is None:
            self._date = self._create_random_str_date()

        if self._month is not None:
            if self._is_int(self._month):
                self._month = str(self._month)
            else:
                raise ValidationError()
        elif self._month is None:
            self._month = self._create_random_str_month()

        result = self._execute_http_request()
        if isinstance(result, str):
            return result
        else:
            self._print_testing_response(result)


class ValidationError(BaseException):
    """Класс ошибки валидации данных"""
    pass


class ResponseStatusCodeError(BaseException):
    """Класс Ошибки статуса ответа от API"""
    pass
