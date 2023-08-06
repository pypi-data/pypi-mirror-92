import six
from utils.query import (ContainsQuery, OrderByQuery, StartsQuery, EndsQuery, FilterQuery, SelectDictQuery, TakeQuery,
                         SkipQuery, QueryRunner, MaxQuery, MinQuery, SumQuery, CountQuery, AvgQuery, DistinctQuery,
                         SelectListQueryFactory, InQuery, FirstQuery, LastQuery, ExistsQuery, SliceQuery, EvenQuery,
                         OddQuery)

if six.PY2:
    from UserList import UserList
else:
    from collections import UserList


class QueryableList(UserList):
    """
    Generates lazy queries for any lists you want with using builder design pattern.
    """

    __slots__ = ['data', '__queries']

    def __init__(self, init_list=None):
        super(QueryableList, self).__init__(init_list)
        self.__queries = []

    def __set_queries(self, queries):
        self.__queries = queries

    def __new_instance(self, last_added_query):
        instance = QueryableList(self.data)
        instance.__set_queries(self.__queries + [last_added_query])
        return instance

    def __iter__(self):
        return iter(self.run())

    def __repr__(self):
        return str(self.run())

    def run(self, query=None):
        """
        Runs the queries.

        Parameters:
            query (Query): (Optional) Single query object

        Returns:
             result: Total result of the query
        """

        queries = [query] if query else self.__queries
        return QueryRunner(queries).run(self.data)

    def filter(self, func):
        """
         Filters the list by using a function.

         Parameters:
             func (Function): filter function

         Returns:
             QueryableList
        """

        return self.__new_instance(FilterQuery(func))

    def starts(self, value):
        """
         Filters the list items  which start by value.

         Parameters:
             value (str)

         Returns:
             QueryableList
        """

        return self.__new_instance(StartsQuery(value))

    def ends(self, value):
        """
         Filters the list items which end by value.

         Parameters:
             value (str)

         Returns:
             QueryableList
        """

        return self.__new_instance(EndsQuery(value))

    def contains(self, value):
        """
         Filters the list items which contain value.

         Parameters:
             value (str)

         Returns:
             QueryableList
        """

        return self.__new_instance(ContainsQuery(value))

    def order_by(self, field=None, desc=False):
        """
         Sorts the list items.

         Parameters:
             field (str): None (default)
             desc (bool): False (default)

         Returns:
             QueryableList
        """

        return self.__new_instance(OrderByQuery(field, desc))

    def select(self, *fields):
        """
         Generates a dictionary which consists of specified fields.

         Parameters:
             fields (Tuple): The fields to selected

         Returns:
             QueryableList
        """

        return self.__new_instance(SelectDictQuery(*fields))

    def select_list(self, *fields, **kwargs):
        """
         Generates a list which consists of specified fields.

         Parameters:
             fields (Tuple): The fields to selected
             flat (bool): (default) False

         Returns:
             QueryableList
        """

        return self.__new_instance(SelectListQueryFactory.new(fields, kwargs.get('flat', False)))

    def skip(self, count):
        """
         Gets remained items of the list after specific number of items are skipped.

         Parameters:
             count (int): Item count to skipped

         Returns:
             QueryableList
        """

        return self.__new_instance(SkipQuery(count))
    
    def take(self, count):
        """
         Gets the first list items of specific number.

         Parameters:
             count (int): Item count to taken

         Returns:
             QueryableList
        """

        return self.__new_instance(TakeQuery(count))
    
    def max(self, field=None):
        """
         Gets the maximum value of the list or a specific field.

         Parameters:
             field (str): default None

         Returns:
            int
        """

        return self.run(MaxQuery(field))

    def min(self, field=None):
        """
         Gets the minimum value of the list or a specific field.

         Parameters:
             field (str): default None

         Returns:
            int
        """

        return self.run(MinQuery(field))

    def sum(self, field=None):
        """
         Gets the sum of the list or a specific field.

         Parameters:
             field (str): default None

         Returns:
            int
        """

        return self.run(SumQuery(field))

    def count(self, field=None):
        """
         Gets the count of the list or a specific field.

         Parameters:
             field (str): default None

         Returns:
            int
        """

        return self.run(CountQuery(field))
    
    def avg(self, field=None):
        """
         Gets the average of the list or a specific field.

         Parameters:
             field (str): default None

         Returns:
            float
        """

        return self.run(AvgQuery(field))
    
    def distinct(self, field=None):
        """
         Gets the unique items of the list

         Parameters:
             field (str): default None

         Returns:
            QueryableList
        """

        return self.__new_instance(DistinctQuery(field))

    def within(self, search_list):
        """
         Gets the existed list items within the given search list.

         Parameters:
             search_list (list): list to searched

         Returns:
            QueryableList
        """

        return self.__new_instance(InQuery(search_list))

    def first(self):
        """
          Gets the first item of the list.

          Returns:
             Any
         """

        return self.run(FirstQuery())

    def last(self):
        """
          Gets the last item of the list.

          Returns:
             Any
         """

        return self.run(LastQuery())

    def exists(self):
        """
          Returns the whether the query matches any list items.

          Returns:
             bool
         """

        return self.run(ExistsQuery())

    def slice(self, start, end):
        """
          Returns the sliced part of the list by the given start and end indexes.

          Returns:
             QueryableList
         """

        return self.__new_instance(SliceQuery(start, end))

    def even(self):
        """
          Returns the even items of the list.

          Returns:
             QueryableList
         """

        return self.__new_instance(EvenQuery())

    def odd(self):
        """
          Returns the odd items of the list.

          Returns:
             QueryableList
         """

        return self.__new_instance(OddQuery())
