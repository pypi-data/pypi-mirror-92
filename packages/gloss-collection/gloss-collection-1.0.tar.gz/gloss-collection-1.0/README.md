# gloss-collection
Gloss (short for glossary) is a different kind of dictionary.
All values also automatically become keys and so can be looked
up in the Gloss to find its corresponding 'key'. This makes it
easy to lookup and maintain one-to-one relationships such as a
label to a certain magnitude.

As both the key and value are gettable items from the Gloss and
are indistinguishable once added, `term` is the preferred name
for items in a Gloss, and a `term pair` is the 1-1 mapping each
term belongs to.

Gloss is a MutableMapping and supports all the same methods
that `dict` does.

## Examples
```python
from gloss import Gloss

example = Gloss()
example["stdin"] = 0
example.update({"stdout": 1, "stderr": 2})
print(example)
#Gloss({"stdin": 0, "stdout": 1, "stderr": 2})
print(example[1], "goes to" example["stderr"])
#stdout goes to 2
example[3] = "config.toml"
example[1] = "shell pipe"
print(example)
#Gloss({"stdin": 0, "stderr": 2, "config.toml": 3, "shell pipe": 1})
print([fd_or_desc for fd_or_desc in example])
#["stdin", "stderr", "config.toml", "shell pipe", 0, 1, 2 , 3]
```

## Shouldn't I just use an enum?
Great thought! You can, and often should, use an
[Enum](https://docs.python.org/3/library/enum.html) for these
sorts of relationsips. Besides being built in to Python, Enums
are probably faster and more space efficient. However, some
limitations of Enums solved by Gloss are:

* enum members are static. They are defined all at once in the
class and their values cannot change. A Gloss on the other hand
can be added to, altered, even have members deleted or popped,
all at runtime
* Accessing Enum member namess and their values are differnt
operations. Looking up a member by name is done with either dot
dereference or getitem; looking up a member by value is done
with a call. With a Gloss you don't have to know which side of
the mapping your key is on (if there even is a distinction to the
mapping), it is all done by getitem
* One side of an enum mapping must be a string. Because member
names are attributes they must follow Python identifier naming
rules. In a Gloss, all keys may be any hashable object

## Shouldn't I just use a dict?
While the classic dict solves some of limitations of using an Enum,
primarily being mutable at runtime, looking up any value is O(n) and
therefore so is updating, deleting, poping, etc that value. In a
Gloss searching for any value is O(1) time, and updating that value
(for example chaning the key it maps to) can be done in a single
operation.
