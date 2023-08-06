import abc

import pandas as pd


class InsightGenerator(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):

        return (hasattr(subclass, 'execute') and
                callable(subclass.execute) and
                hasattr(subclass, 'write_to_table') and
                callable(subclass.write_to_table) and
                hasattr(subclass, 'provideEvidence') and
                callable(subclass.provideEvidence) or
                NotImplemented)

    @abc.abstractmethod
    def define_query(self, context: dict = None) -> str:
        """This is where the TODO

        Args:
            context (dict, optional): A dict where keys correspond to those given in context.json, values are provided
                dynamically by insights engine. E.g. if you specify in context.json, '{"customerCodes": [1]}' then this 
                gives users the option to specify any customer code they have access to as input to this insight.
                Defaults to None.

        Raises:
            NotImplementedError:  Will raise if subclasss doesn't implement this method.

        Returns:
            str: a valid SQL query.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def transform(self):
        raise NotImplementedError

    def provide_evidence(self):
        pass
