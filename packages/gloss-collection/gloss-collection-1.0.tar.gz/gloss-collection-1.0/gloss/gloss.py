from itertools import chain
from typing import (
    Dict,
    Hashable,
    ItemsView,
    Iterable,
    Iterator,
    KeysView,
    Mapping,
    Tuple,
    ValuesView,
    overload,
)

TermType = Hashable


class Gloss(Dict[TermType, TermType]):
    """Gloss[ary] is a symetric 1-1 mapping of terms (keys)

    As such both terms (the key and the value) must be hashable, all
    terms are indexable, and an update any one will affect its mapped
    term as an index.
    Although terms are hashable, they are not necessarily unique
    (although no more than two copies can be present).
    Insertion order is not guaranteed to be preserved in any python version.
    """

    class NoValue:
        pass

    @overload
    def __init__(self, __t: Mapping[TermType, TermType], **kwargs: TermType) -> None:
        ...

    @overload
    def __init__(
        self, __t: Iterable[Tuple[TermType, TermType]], **kwargs: TermType
    ) -> None:
        ...

    @overload
    def __init__(self, **kwargs: TermType) -> None:
        ...

    def __init__(self, *args, **kwargs) -> None:  # type: ignore
        self.data: Dict[TermType, TermType] = {}
        self.atad: Dict[TermType, TermType] = {}
        for term, pair in dict(*args, **kwargs).items():
            self[term] = pair

    def __setitem__(self, term: TermType, pair: TermType) -> None:
        if not isinstance(pair, Hashable):
            raise TypeError("unhashable type: {}".format(type(pair)))
        if term in self.atad:
            del self.data[self.atad[term]]
            del self.atad[term]
        if pair in self.data:
            del self.atad[self.data[pair]]
            del self.data[pair]
        if term in self.data:
            del self.atad[self.data[term]]
        if pair in self.atad:
            del self.data[self.atad[pair]]
        self.data[term] = pair
        self.atad[pair] = term

    def __getitem__(self, term: TermType) -> TermType:
        if term in self.data:
            return self.data[term]
        return self.atad[term]

    def __delitem__(self, term: TermType) -> None:
        if term in self.data:
            del self.atad[self.data[term]]
            del self.data[term]
        else:
            del self.data[self.atad[term]]
            del self.atad[term]

    def __contains__(self, term: TermType) -> bool:
        return term in self.data or term in self.atad

    def __iter__(self) -> Iterator[TermType]:
        for term in chain(self.data, self.atad):
            yield term

    def __len__(self) -> int:
        return 2 * len(self.data)

    def __repr__(self) -> str:
        return "Gloss({})".format(repr(self.data))

    def clear(self) -> None:
        self.data.clear()
        self.atad.clear()

    def copy(self) -> "Gloss":
        return Gloss(self)

    def get(self, term: TermType, default: TermType = None) -> TermType:
        if term in self.data:
            return self.data[term]
        elif term in self.atad:
            return self.atad[term]
        return default

    def items(self) -> ItemsView[TermType, TermType]:
        return ItemsView(self)

    def keys(self) -> KeysView[TermType]:
        return KeysView(self)

    terms = keys

    def pop(self, term: TermType, default: TermType = NoValue) -> TermType:
        if term in self.data:
            pair = self.data.pop(term)
            del self.atad[pair]
            return pair
        if default is self.NoValue:
            pair = self.atad.pop(term)
        else:
            pair = self.atad.pop(term, default)
        if pair in self.data:
            del self.data[pair]
        return pair

    def popitem(self) -> Tuple[TermType, TermType]:
        term, pair = self.data.popitem()
        del self.atad[pair]
        return term, pair

    def setdefault(self, term: TermType, default: TermType = None) -> TermType:
        if term in self.data:
            return self.data[term]
        elif term in self.atad:
            return self.atad[term]
        self.__setitem__(term, default)
        return self.data[term]

    @overload
    def update(self, __t: Mapping[TermType, TermType], **kwargs: TermType) -> None:
        ...

    @overload
    def update(
        self, __t: Iterable[Tuple[TermType, TermType]], **kwargs: TermType
    ) -> None:
        ...

    @overload
    def update(self, **kwargs: TermType) -> None:
        ...

    def update(self, *args, **kwargs) -> None:  # type: ignore
        for term, pair in dict(*args, **kwargs).items():
            self[term] = pair

    def values(self) -> ValuesView[TermType]:
        return ValuesView(self)
