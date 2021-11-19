#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Optional, Union
import re


def is_name_valid(name):
    def is_letter(sign):
        if (ord('a') <= ord(sign) <= ord('z')) or (ord('A') <= ord(sign) <= ord('Z')):
            return True
        else:
            return False

    def is_number(sign):
        if ord('0') <= ord(sign) <= ord('9'):
            return True
        else:
            return False

    n_count = 0
    l_count = 0
    letters_part = True
    for sign in name:
        if (not is_number(sign)) and (not is_letter(sign)):
            raise ValueError('Name can only consist of letter and numbers')
        if letters_part and is_number(sign):
            letters_part = False
        if not letters_part and is_letter(sign):
            raise ValueError('Cannot place letter after number')
        if is_number(sign):
            n_count += 1
        if is_letter(sign):
            l_count += 1
    if l_count == 0 or n_count == 0:
        raise ValueError('name must consist of at least 1 number and 1 letter')


class Product:
    def __init__(self, name: str, price: float):
        is_name_valid(name)
        self.name = name
        self.price = price

    def __eq__(self, other):
        if self.name == other.id and self.price == other.price:
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.name, self.price))


class TooManyProductsFoundError:
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    pass


# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania

class ListServer:
    lst = []

    def __init__(self, products):
        self.lst = products

    def get_entries(self, n_letters):
        matching_prod = []
        for product in self.lst:
            criteria = "[a-zA-Z]" + "{" + str(n_letters) + "}[1-9]{2,3}"
            m = re.match(criteria, product.name)
            if m is not None and len(m.group(0)) == len(product.name):
                matching_prod.append(product)
        matching_prod.sort(key=lambda x: x.price)
        return matching_prod



class MapServer:
    dct = {}

    def __init__(self, products):
        for product in products:
            self.dct[product.name] = product

    def get_entries(self, n_letters):
        matching_prod = []
        for product in self.dct:
            criteria = "[a-zA-Z]" + "{" + str(n_letters) + "}[1-9]{2,3}"
            m = re.match(criteria, product)
            if m is not None and len(m.group(0)) == len(product):
                matching_prod.append(self.dct[product])
        matching_prod.sort(key=lambda x: x.price)
        return matching_prod


class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer
    def __init__(self, server: Union[MapServer, ListServer]):
        self.client_server = server

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        products = self.client_server.get_entries(n_letters)
        total_price = 0
        for prod in products:
            total_price += prod.price
        return total_price
