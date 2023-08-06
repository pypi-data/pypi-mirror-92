"""
    gitdata graph
"""

from itertools import chain
import gitdata
import gitdata.digester


class Node:
    """Graph Node"""

    def __init__(self, graph, uid):
        self.graph = graph
        self._uid = uid

    def add(self, relation, data):
        """Add a related data to a node"""
        uid = self.graph.add(data)
        self.graph.store.add([(self.uid, relation, uid)])
        return uid

    @property
    def uid(self):
        return self._uid

    def update(self, *args, **kwargs):
        """Update data related to a node"""
        for relation, data in dict(args, **kwargs).items():
            self.graph.store.remove(
                self.graph.triples((self.uid, relation, None))
            )
            self.add(relation, data)

    def delete(self):
        """Delete all facts related to a node"""
        self.graph.store.remove(
            self.graph.triples((self.uid, None, None))
        )

    def __getitem__(self, name):
        values = self.graph.triples((self.uid, name, None))
        return list(values)[0][-1] if values else None

    def __getattr__(self, name):
        for fact in self.graph.triples((self.uid, name, None)):
            o = fact[-1]
            facts = self.graph.triples((o, None, None))
            if facts:
                return Node(self.graph, o)
            return o


    def __str__(self):

        t = []

        for _, key, value in self.graph.triples((self.uid, None, None)):
            t.append('  {} {}: {!r}'.format(
                key,
                '.'*(20-len(key[:20])),
                value
            ))
        return '\n'.join([repr(self)] + t)

    def __repr__(self):
        name = "{}('{}')".format(
            self.__class__.__name__,
            self.uid
        )
        return name


class Graph:
    """Graph Result"""

    def __init__(self, graph, head):
        self.graph = graph
        self.head = head

    def triples(self, pattern=(None, None, None)):
        """return triples that match a pattern"""
        return self.graph.triples(pattern)

    def get(self, uid):
        """Get a node of the graph"""
        return Node(self, uid)

    def query(self, clauses):
        """Query the graph"""
        bindings = None
        for clause in clauses:
            bpos = {}
            qc = []
            for pos, x in enumerate(clause):
                if type(x) == str and (x.startswith('?') or x.startswith('_')):
                    qc.append(None)
                    bpos[x] = pos
                else:
                    qc.append(x)
            rows = list(self.triples((qc[0], qc[1], qc[2])))
            if bindings == None:
                # This is the first pass, everything matches
                bindings = []
                for row in rows:
                    binding = {}
                    for var, pos in bpos.items():
                        binding[var] = row[pos]
                    bindings.append(binding)
            else:
                # in subsequent passes, eliminate bindings that dont work
                newb = []
                for binding in bindings:
                    for row in rows:
                        validmatch = True
                        tempbinding = binding.copy()
                        for var, pos in bpos.items():
                            if var in tempbinding:
                                if tempbinding[var] != row[pos]:
                                    validmatch = False
                            else:
                                tempbinding[var] = row[pos]
                        if validmatch:
                            newb.append(tempbinding)
                bindings = newb
        return [
            dict(
                (k[1:], v)
                for k, v in b.items()
                if k[0] == '?'
            ) for b in bindings
        ]

    def find(self, *args, **kwargs):
        """Find nodes"""
        query = []
        for i in args:
            query.append(('?subject', i, '?'+i))
        for k, v in kwargs.items():
            query.append(('?subject', k, v))
        return [
            self.get(record['subject'])
            for record in self.query(query)
        ]

    def __call__(self, *args, **kwargs):
        return self.find(*args, **kwargs)

    def first(self, *args, **kwargs):
        """Find first node"""
        result = self.find(*args, **kwargs)
        if result:
            return result[0]

    def exists(self, *args, **kwargs):
        """Return True if specified nodes exist else return False"""
        return bool(self.first(*args, **kwargs))

    def __str__(self):
        """Human friendly string representation"""
        return '\n'.join(repr(triple) for triple in self.triples())

    def __repr__(self):
        pattern = (self.head, None, None)
        return 'Node({})'.format(
            ', '.join(
                '{}: {!r}'.format(*rec[1:])
                for rec in self.graph.triples(pattern)
            )
        )


class BaseGraph(Graph):
    """Graph attached to fact store"""

    def __init__(self, store, new_uid=gitdata.utils.new_uid):
        self.store = store
        self.digester = gitdata.digester.Digester(new_uid=new_uid)

    def add(self, data):
        """Add arbitrary data to the graph"""
        self.digester.store = []
        uid = self.digester.digest(data)
        self.store.add(self.digester.known)
        return Node(self, uid)

    def delete(self, pattern):
        """Delete all triples matching the pattern"""
        facts = self.triples(pattern)
        self.store.remove(facts)
        return 1

    def triples(self, pattern=(None, None, None)):
        """Find graph triples that match a pattern"""
        return self.store.triples(pattern)

    def clear(self):
        """Clear the graph"""
        return self.store.clear()

    def __len__(self):
        return len(self.store)


class AbstractGraph:
    """Abstract Graph"""

    uid = None

    def triples(self, pattern=(None, None, None)):
        """return triples that match a pattern"""
        return []

    @property
    def facts(self):
        return self.triples()

    def successors(self):
        query = [
            (self.uid, None, '?successor'),
            ('?successor', None, None),
        ]
        uids = [n['successor'] for n in self.query(query)]
        print(uids)
        # print(NewNode(self, '2'))
        return [NewNode(self, uid) for uid in uids]

    def query(self, clauses):
        """Query the graph"""
        bindings = None
        for clause in clauses:
            bpos = {}
            qc = []
            for pos, x in enumerate(clause):
                if type(x) == str and (x.startswith('?') or x.startswith('_')):
                    qc.append(None)
                    bpos[x] = pos
                else:
                    qc.append(x)
            rows = list(self.triples((qc[0], qc[1], qc[2])))
            if bindings == None:
                # This is the first pass, everything matches
                bindings = []
                for row in rows:
                    binding = {}
                    for var, pos in bpos.items():
                        binding[var] = row[pos]
                    bindings.append(binding)
            else:
                # in subsequent passes, eliminate bindings that dont work
                newb = []
                for binding in bindings:
                    for row in rows:
                        validmatch = True
                        tempbinding = binding.copy()
                        for var, pos in bpos.items():
                            if var in tempbinding:
                                if tempbinding[var] != row[pos]:
                                    validmatch = False
                            else:
                                tempbinding[var] = row[pos]
                        if validmatch:
                            newb.append(tempbinding)
                bindings = newb
        return [
            dict(
                (k[1:], v)
                for k, v in b.items()
                if k[0] == '?'
            ) for b in bindings
        ]

    def find(self, *args, **kwargs):
        """Find nodes"""
        query = []
        for i in args:
            query.append(('?subject', i, '?'+i))
        for k, v in kwargs.items():
            query.append(('?subject', k, v))
        return [
            self.get(record['subject'])
            for record in self.query(query)
        ]

    def first(self, *args, **kwargs):
        """Find first node"""
        result = self.find(*args, **kwargs)
        if result:
            return result[0]

    def exists(self, *args, **kwargs):
        """Return True if specified nodes exist else return False"""
        return bool(self.first(*args, **kwargs))

    def get(self, uid):
        # def get(self, uid):
        return NewNode(self, uid)

    def __str__(self):
        """Human friendly string representation"""
        return '\n'.join(repr(triple) for triple in self.triples())

    def __repr__(self):
        pattern = (self.head, None, None)
        return 'Node({})'.format(
            ', '.join(
                '{}: {!r}'.format(*rec[1:])
                for rec in self.graph.triples(pattern)
            )
        )

    def __iter__(self):
        return iter(self.facts)

    def __len__(self):
        """return number of facts in graph"""
        return len(self.store)

class NewNode(AbstractGraph):

    def __init__(self, graph, uid):
        self.graph = graph
        self.uid = uid
        self.store = graph.store

    def add(self, relation, data):
        """Add a related data to a node"""
        uid = self.graph.add(data)
        self.graph.store.add([(self.uid, relation, uid)])
        return uid

    def __getattr__(self, name):
        q = self.triples((self.uid, name, None))
        if q:
            return q[0][2]

    # def __getitem__(self, name):
    #     values = self.graph.triples((self.uid, name, None))
    #     return list(values)[0][-1] if values else None

    # def __str__(self):
    #     pattern = (self.uid, None, None)

    #     name = '{}({})'.format(
    #         self.__class__.__name__,
    #         self.uid
    #     )
    #     t = []

    #     for _, key, value in self.graph.triples(pattern):
    #         t.append('  {} {}: {!r}'.format(
    #             key,
    #             '.'*(20-len(key[:20])),
    #             value
    #         ))
    #     return '\n'.join([name] + t)

    def triples(self, pattern=(None, None, None)):
        """Find graph triples that match a pattern"""
        query = [
            pattern,
            (self.uid, None, '?successor'),
            ('?successor', None, None),
        ]
        uids = [n['successor'] for n in self.graph.query(query)]
        triples = self.graph.triples
        return [triple for uid in uids for triple in triples((uid, None, None))]

        # print(uids)
        # print(NewNode(self, '2'))
        # return [NewNode(self, uid) for uid in uids]

        # return self.graph.triples(pattern)


class NewGraph(AbstractGraph):

    def __init__(self, store, new_uid=gitdata.utils.new_uid):
        self.store = store
        self.new_uid = new_uid
        self.uid = 'root'

    # def get(self, uid):
    #     """Get a node of the graph"""
    #     return


    def ingest(self, data):
        """Ingest arbitrary data to the graph"""
        digester = gitdata.digester.Digester(new_uid=self.new_uid)
        uid = digester.digest(data)
        self.store.add(digester.known)
        self.store.add([('root', 'includes', uid)])
        return NewNode(self, uid)


    def add(self, data):
        """Add arbitrary data to the graph"""
        digester = gitdata.digester.Digester(new_uid=self.new_uid)
        uid = digester.digest(data)
        self.store.add(digester.known)
        self.store.add([('root', 'includes', uid)])
        return NewNode(self, uid)


    # def delete(self, data):
    #     """Purge arbitrary from the graph"""
    #     digester = gitdata.digester.Digester(new_uid=gitdata.utils.new_uid_placeholder)
    #     uid = digester.digest(data)
    #     print(digester.known)
    #     print(self.query(digester.known))
    #     print(self.query([('?test', 'name', 'Sally')]))
    #     # self.store.add(digester.known)
    #     # self.store.add([('root', 'includes', uid)])
    #     # return NewNode(self, uid)

    def triples(self, pattern=(None, None, None)):
        """Find graph triples that match a pattern"""
        return self.store.triples(pattern)

