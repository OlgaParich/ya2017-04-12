import heapq

task = '''
Lesson 3. A_Huffman.
Разработайте метод encode(File file) для кодирования строки (код Хаффмана)

 По данным файла (непустой строке ss длины не более 104104),
 состоящей из строчных букв латинского алфавита,
 постройте оптимальный по суммарной длине беспрефиксный код.

 Используйте Алгоритм Хаффмана — жадный алгоритм оптимального
 безпрефиксного кодирования алфавита с минимальной избыточностью.

 В первой строке выведите количество различных букв kk,
 встречающихся в строке, и размер получившейся закодированной строки.
 В следующих kk строках запишите коды букв в формате "letter: code".
 В последней строке выведите закодированную строку. Примеры ниже

        Sample Input 1:
        a

        Sample Output 1:
        1 1
        a: 0
        0

        Sample Input 2:
        abacabad

        Sample Output 2:
        4 14
        a: 0
        b: 10
        c: 110
        d: 111
        01001100100111

# Изучите классы Node, InternalNode, LeafNode - без
  полного понимания их работы вы не выполните это задание
'''

class Node:
    # абстрактный класс элемент дерева
    # (сделан abstract, чтобы нельзя было использовать его напрямую)
    # а только через его версии InternalNode и LeafNode
    def __init__(self, frequence):  # конструктор по умолчанию
        self.frequence = frequence  # частота символов
        self.symbol = None  # FIX символ нужен для лексикографической
        # сортировки при равенстве частот

    # генерация кодов (вызывается на корневом узле
    # вызывается один раз в конце, т.е.после построения дерева)
    def fill_codes(self, code):
        raise NotImplementedError("Please Implement this method")
        # метод нужен для корректной работы узла в приоритетной очереди
        # или для сортировок

    # компаратор узлов по частоте (нужен для heapq)
    def __lt__(self, other):
        if self.frequence != other.frequence:
            return self.frequence < other.frequence
        else:
            return self.symbol > other.symbol  # FIX


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# расширение базового класса до внутреннего узла дерева
class InternalNode(Node):
    # внутренний узел дерева
    # для этого дерева не существует внутренних узлов без обоих детей
    # поэтому вот такого конструктора будет достаточно
    def __init__(self, left, right):
        super().__init__(left.frequence + right.frequence)
        self.left = left  # левый ребенок бинарного дерева
        self.right = right  # правый ребенок бинарного дерева
        self.symbol = left.symbol  # копируем символ из левого листа (для корректной сортировки)

    def __repr__(self):
        return repr(("-", self.frequence))

    def fill_codes(self, code):
        self.left.fill_codes(code + "1")
        self.right.fill_codes(code + "0")


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# расширение базового класса до листа дерева

class LeafNode(Node):
    def __init__(self, symbol, frequence):
        super().__init__(frequence)
        self.symbol = symbol    # символы хранятся в листах и дублируются
                                # в вершины для лексикографической сортировки

    # добрались до листа, значит рекурсия закончена, код уже готов
    # и можно запомнить его в индексе для поиска кода по символу.
    def fill_codes(self, code):
        codes.setdefault(self.symbol, code)

    def __repr__(self):
        return repr((self.symbol, self.frequence))


# очередь, выделена в отдельный
# класс для удобного использования

class Heap():
    def __init__(self) -> None:
        self._heap = []
        heapq.heapify(self._heap)

    def size(self):
        return len(self._heap)

    def push(self, node):
        heapq.heappush(self._heap, node)

    def pop(self):
        n = heapq.heappop(self._heap)
        return n


# словарь для кодов в формате symbol:code
codes = dict()


# !!!!!!!!!!!!!!!!!!!!!!!!!     НАЧАЛО ЗАДАЧИ     !!!!!!!!!!!!!!!!!!!!!!!!!
def encode(filename):
    # 1. переберем все символы по очереди и рассчитаем их частоту в словаре counts
    # для каждого символа добавим 1 если элемента еще нет или инкремент если есть.
    f = open(filename)
    string = f.readline()
    counts = dict()
    for ch in string:
        count = counts.get(ch)
        if count:
            counts.update({ch: count+1})
        else:
            counts.update({ch: 1})
    # 2. перенесем все символы в приоритетную очередь в виде листьев
    h = Heap()
    for sym, count in counts.items():
        leaf = LeafNode(sym, count)
        h.push(leaf)
    # 3. вынимая по два узла из очереди (для сборки родителя)
    # и возвращая этого родителя обратно в очередь
    # построим дерево кодирования Хаффмана
    # все комментарии от тестового решения были оставлены т.к. это задание A.
    # если они вам мешают их можно удалить
    while h.size() > 1:
        left = h.pop()
        right = h.pop()
        parent = InternalNode(left, right)
        h.push(parent)
    # 4. последний из родителей будет корнем этого дерева
    # это будет последний и единственный элемент оставшийся в очереди.
    root = h.pop()

    if len(counts) == 1:
        root.fill_codes("0")
    else:
        root.fill_codes("")

    # for ch, code in codes.items():
    #     print(ch, ":", code)
    # 5. Можно кодировать. Для этого нужно получить коды и составить словарь
    res = ""
    for ch in string:
        res = res + codes.get(ch)
    return res

# encode("F:\python\ya2017-04-12\src\moskalenko\lesson03\dataHuffman.txt")

# !!!!!!!!!!!!!!!!!!!!!!!!!     КОНЕЦ ЗАДАЧИ     !!!!!!!!!!!!!!!!!!!!!!!!!


def main():
    res = encode("dataHuffman.txt")
    print(res)


# Для ручной проверки нажмите Ctrl+Shift+F10
# установив курсор на  main
# или создайте конфигурацию Run-Edit configuration
if __name__ == "__main__":
    main()
