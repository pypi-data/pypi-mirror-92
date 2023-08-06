# -*- coding: utf-8 -*-

#Copyright (c) 2020 André Santos
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.


###############################################################################
# Imports
###############################################################################

from __future__ import print_function
from past.builtins import basestring
from builtins import range
from collections import namedtuple
import re

import networkx as nx

from .nx_patch import minimum_weight_full_matching


###############################################################################
# Globals
###############################################################################

def _noop(msg):
    pass

flog = _noop

INF = float("inf")


###############################################################################
# Helper Classes
###############################################################################

GraphData = namedtuple("GraphData",
    ("nodes", "parameters", "publishers", "subscribers",
     "clients", "servers", "setters", "getters"))

NodeAttrs = namedtuple("NodeAttrs",
    ("key", "rosname", "rostype", "traceability", "args", "remaps", "conditions",
     "publishers", "subscribers", "clients", "servers", "setters", "getters"))

ParamAttrs = namedtuple("ParamAttrs",
    ("key", "rosname", "rostype", "traceability", "value", "conditions"))

PubAttrs = namedtuple("PubAttrs",
    ("key", "rosname", "rostype", "traceability", "original_name",
     "queue_size", "latched", "conditions"))

SubAttrs = namedtuple("SubAttrs",
    ("key", "rosname", "rostype", "traceability", "original_name",
     "queue_size", "conditions"))

CliAttrs = namedtuple("CliSrvAttrs",
    ("key", "rosname", "rostype", "traceability", "original_name",
     "conditions"))

SrvAttrs = CliAttrs

SetAttrs = namedtuple("SetGetAttrs",
    ("key", "rosname", "rostype", "traceability", "original_name",
     "value", "conditions"))

GetAttrs = SetAttrs


Guard = namedtuple("Guard",
    ("package", "file", "line", "column", "statement"))

Location = namedtuple("Location", ("package", "file", "line", "column"))

Matching = namedtuple("Matching", ("matches", "missing", "spurious"))


###############################################################################
# Graph Matching
###############################################################################

def matching_by_name(config, truth, iface=None):
    return matching_by(config, truth, cost_rosname, iface=iface, t=3)

def matching_by_name_type(config, truth, iface=None):
    return matching_by(config, truth, cost_rosname_rostype, iface=iface, t=2*3)

def matching_by_name_type_loc(config, truth, iface=None):
    return matching_by(config, truth, cost_rosname_rostype_traceability,
        iface=iface, t=5*2*3)

def matching_by_loc(config, truth, iface=None):
    return matching_by(config, truth, cost_traceability_main, iface=iface, t=4)

def matching_by_loc_name(config, truth, iface=None):
    return matching_by(config, truth, cost_traceability_rosname,
        iface=iface, t=4*4)

def matching_by_loc_name_type(config, truth, iface=None):
    return matching_by(config, truth, cost_traceability_rosname_rostype,
        iface=iface, t=4*2*4)


def matching_by(config, truth, cost_function, iface=None, t=INF):
    global flog
    if iface is None:
        flog = _noop
    else:
        flog = iface.log_debug
    M_nodes = node_matching(config.nodes.enabled,
        truth["nodes"], cost_function, t=t)
    M_params = param_matching(config.parameters.enabled,
        truth["parameters"], cost_function, t=t)
    return GraphData(M_nodes, M_params,
        link_matching(M_nodes, "publishers", cost_function, t=t),
        link_matching(M_nodes, "subscribers", cost_function, t=t),
        link_matching(M_nodes, "clients", cost_function, t=t),
        link_matching(M_nodes, "servers", cost_function, t=t),
        link_matching(M_nodes, "setters", cost_function, t=t),
        link_matching(M_nodes, "getters", cost_function, t=t))


###############################################################################
# Matching Functions
###############################################################################

def node_matching(config_nodes, truth_nodes, cost_function, t=INF):
    lhs = [convert_haros_node(node) for node in config_nodes]
    rhs = [convert_truth_node(rosname, data)
           for rosname, data in truth_nodes.items()]
    return _matching(lhs, rhs, cost_function, t)

def param_matching(config_params, truth_params, cost_function, t=INF):
    lhs = [convert_haros_param(param) for param in config_params
           if param.launch is not None]
    rhs = []
    for rosname, data in truth_params.items():
        for param in convert_truth_params(rosname, data):
            rhs.append(param)
    return _matching(lhs, rhs, cost_function, t)

def link_matching(M_nodes, attr, cost_function, t=INF):
    M = Matching([], [], [])
    for node in M_nodes.missing:
        M.missing.extend(getattr(node, attr))
    for node in M_nodes.spurious:
        M.spurious.extend(getattr(node, attr))
    for node, gold in M_nodes.matches:
        lhs = getattr(node, attr)
        rhs = getattr(gold, attr)
        m = _matching(lhs, rhs, cost_function, t)
        M.matches.extend(m.matches)
        M.missing.extend(m.missing)
        M.spurious.extend(m.spurious)
    return M


def _matching(lhs, rhs, cost_function, t):
    if lhs and not rhs:
        return Matching([], [], list(lhs))
    if rhs and not lhs:
        return Matching([], list(rhs), [])
    if not lhs and not rhs:
        return Matching([], [], [])
    G = nx.Graph()
    top = []
    for v in rhs:
        G.add_node(v.key, data=v, bipartite=1)
        top.append(v.key)
    for u in lhs:
        G.add_node(u.key, data=u, bipartite=0)
        for v in rhs:
            weight = cost_function(u, v)
            G.add_edge(u.key, v.key, weight=weight)
    M = minimum_weight_full_matching(G, top_nodes=top)
    # The matching is returned as a dictionary such that
    #   M[u] == v if node u is matched to node v.
    # Unmatched nodes do not occur as a key.
    matched = []
    missed = []
    spurious = []
    for u in lhs:
        key = M.get(u.key)
        if key is None:
            spurious.append(u)
        else:
            v = G.nodes[key]["data"]
            weight = G[u.key][key]["weight"]
            if weight < t:
                matched.append((u, v))
            else:
                missed.append(v)
                spurious.append(u)
    for v in rhs:
        if v.key not in M:
            missed.append(v)
    return Matching(matched, missed, spurious)


###############################################################################
# Cost Functions
###############################################################################

# '/?/?' means both namespace and own name are unknown
# '/?' means the global namespace with own name unknown
def cost_rosname(u, v):
    if u.rosname == v.rosname:
        return 0
    try:
        expected = getattr(v, "original_name")
        alt = v.rosname
    except AttributeError:
        expected = v.rosname
        alt = None
    if "?" in u.rosname and rosname_match(u.rosname, expected, alt=alt):
        if u.rosname.count("?") > 1:
            return 2
        return 1
    return 3

def cost_rostype(u, v):
    if u.rostype == v.rostype:
        return 0
    #if u.rostype is None or "?" in u.rostype:
    #    return 1
    #return 2
    return 1

def cost_rosname_rostype(u, v):
    # rostype values in [0, 1]; behave as if in base 2
    return 2 * cost_rosname(u, v) + cost_rostype(u, v)

def cost_traceability(u, v):
    p = u.traceability
    g = v.traceability
    assert g.package is not None
    assert g.file is not None
    assert g.line is not None
    assert g.column is not None
    if p.package != g.package:
        return 4
    if p.file != g.file:
        return 3
    if p.line != g.line:
        return 2
    if p.column != g.column:
        return 1
    return 0

def cost_rosname_rostype_traceability(u, v):
    # traceability values in [0, 4]; behave as if in base 5
    cost = 2 * 5 * cost_rosname(u, v)
    cost = cost + 5 * cost_rostype(u, v)
    return cost + cost_traceability(u, v)


def cost_traceability_main(u, v):
    p = u.traceability
    g = v.traceability
    assert g.package is not None
    assert g.file is not None
    assert g.line is not None
    assert g.column is not None
    if p.package is None:
        return 8
    if p.package != g.package:
        return 8
    if p.file is None:
        return 4
    if p.file != g.file:
        return 4
    if p.line is None or p.column is None:
        return 3
    d_line = int(abs(g.line - p.line))
    d_col = int(abs(g.column - p.column))
    if d_line > 0:
        if d_line == 1:
            if not d_col:
                return 1
            return 2
        return 3
    elif d_col > 0:
        assert d_col > 0
        if d_col <= 8:
            return 1
        if d_col < 50:
            return 2
        return 3
    return 0

def cost_traceability_rosname(u, v):
    # values in [0, 3]; behave as if in base 4
    cost = 4 * cost_traceability_main(u, v)
    return cost + cost_rosname(u, v)

def cost_traceability_rosname_rostype(u, v):
    cost = 4 * 2 * cost_traceability_main(u, v)
    cost = cost + 2 * cost_rosname(u, v)
    return cost + cost_rostype(u, v)


###############################################################################
# HAROS Conversion Functions
###############################################################################

def convert_haros_node(node):
    if node._location:
        traceability = convert_haros_location(node._location)
    else:
        traceability = convert_haros_location2(node.location2)
    conditions = convert_haros_conditions(node.conditions)
    pubs = [convert_haros_pub(link) for link in node.publishers]
    subs = [convert_haros_sub(link) for link in node.subscribers]
    clients = [convert_haros_cli(link) for link in node.clients]
    servers = [convert_haros_srv(link) for link in node.servers]
    setters = [convert_haros_setter(link) for link in node.writes]
    getters = [convert_haros_getter(link) for link in node.reads]
    return NodeAttrs(id(node), node.id, node.type, traceability, node.argv,
        node.remaps, conditions, pubs, subs, clients, servers, setters, getters)

def convert_haros_param(param):
    assert param.launch is not None
    if param._location:
        traceability = convert_haros_location(param._location)
    else:
        traceability = convert_haros_location2(param.location2)
    conditions = convert_haros_conditions(param.conditions)
    return ParamAttrs(id(param), param.id, param.type, traceability,
        param.value, conditions)

def convert_haros_pub(link):
    if link.source_location:
        traceability = convert_haros_location(link.source_location)
    else:
        traceability = convert_haros_location2(link.location2)
    conditions = convert_haros_conditions(link.conditions)
    return PubAttrs(id(link), link.topic.id, link.type,
        traceability, link.rosname.full, link.queue_size, link.latched,
        conditions)

def convert_haros_sub(link):
    if link.source_location:
        traceability = convert_haros_location(link.source_location)
    else:
        traceability = convert_haros_location2(link.location2)
    conditions = convert_haros_conditions(link.conditions)
    return SubAttrs(id(link), link.topic.id, link.type,
        traceability, link.rosname.full, link.queue_size, conditions)

def convert_haros_cli(link):
    if link.source_location:
        traceability = convert_haros_location(link.source_location)
    else:
        traceability = convert_haros_location2(link.location2)
    conditions = convert_haros_conditions(link.conditions)
    return CliAttrs(id(link), link.service.id, link.type,
        traceability, link.rosname.full, conditions)

def convert_haros_srv(link):
    if link.source_location:
        traceability = convert_haros_location(link.source_location)
    else:
        traceability = convert_haros_location2(link.location2)
    conditions = convert_haros_conditions(link.conditions)
    return SrvAttrs(id(link), link.service.id, link.type,
        traceability, link.rosname.full, conditions)

def convert_haros_setter(link):
    if link.source_location:
        traceability = convert_haros_location(link.source_location)
    else:
        traceability = convert_haros_location2(link.location2)
    conditions = convert_haros_conditions(link.conditions)
    return SetAttrs(id(link), link.parameter.id, link.type,
        traceability, link.rosname.full, link.value, conditions)

def convert_haros_getter(link):
    if link.source_location:
        traceability = convert_haros_location(link.source_location)
    else:
        traceability = convert_haros_location2(link.location2)
    conditions = convert_haros_conditions(link.conditions)
    return GetAttrs(id(link), link.parameter.id, link.type,
        traceability, link.rosname.full, link.value, conditions)


def convert_haros_location(loc):
    if loc is None or loc.package is None:
        return Location(None, None, None, None)
    if loc.file is None:
        return Location(loc.package.name, None, None, None)
    return Location(loc.package.name, loc.file.full_name, loc.line, loc.column)

def convert_haros_location2(loc2):
    return Location(loc2.package, loc2.file, loc2.line, loc2.column)

def convert_haros_conditions(conditions):
    cfg = {}
    cur = cfg
    for condition in conditions:
        loc = convert_haros_location(condition.location)
        g = Guard(loc.package, loc.file, loc.line, loc.column,
                  condition.statement)
        new_cfg = {}
        cur[g] = new_cfg
        cur = new_cfg
    return cfg

###############################################################################
# Ground Truth Conversion Functions
###############################################################################

def convert_truth_node(rosname, data):
    rostype = data["node_type"]
    traceability = convert_truth_traceability(data["traceability"])
    args = data.get("args", "")
    remaps = data.get("remaps", {})
    conditions = convert_truth_conditions(data.get("conditions", ()))
    pubs = [convert_truth_pub(link) for link in data.get("publishers", ())]
    subs = [convert_truth_sub(link) for link in data.get("subscribers", ())]
    clients = [convert_truth_cli(link) for link in data.get("clients", ())]
    servers = [convert_truth_srv(link) for link in data.get("servers", ())]
    setters = [convert_truth_setter(link) for link in data.get("setters", ())]
    getters = [convert_truth_getter(link) for link in data.get("getters", ())]
    return NodeAttrs(id(data), rosname, rostype, traceability, args, remaps,
        conditions, pubs, subs, clients, servers, setters, getters)

def convert_truth_params(rosname, data):
    rostype = data.get("param_type")
    traceability = convert_truth_traceability(data["traceability"])
    value = data.get("default_value")
    conditions = convert_truth_conditions(data.get("conditions", ()))
    if rostype == "yaml" and isinstance(value, dict) and value:
        return _unfold_yaml(rosname, traceability, conditions, value)
    else:
        return (ParamAttrs(id(data), rosname, rostype, traceability, value,
            conditions),)

def convert_truth_pub(link):
    rosname = link["topic"]
    rostype = link["msg_type"]
    traceability = convert_truth_traceability(link["traceability"])
    original_name = link.get("original_name", rosname)
    queue_size = link["queue_size"]
    latched = link.get("latched", False)
    conditions = convert_truth_conditions(link.get("conditions", ()))
    return PubAttrs(id(link), rosname, rostype, traceability,
        original_name, queue_size, latched, conditions)

def convert_truth_sub(link):
    rosname = link["topic"]
    rostype = link["msg_type"]
    traceability = convert_truth_traceability(link["traceability"])
    original_name = link.get("original_name", rosname)
    queue_size = link["queue_size"]
    conditions = convert_truth_conditions(link.get("conditions", ()))
    return SubAttrs(id(link), rosname, rostype, traceability,
        original_name, queue_size, conditions)

def convert_truth_cli(link):
    rosname = link["service"]
    rostype = link["srv_type"]
    traceability = convert_truth_traceability(link["traceability"])
    original_name = link.get("original_name", rosname)
    conditions = convert_truth_conditions(link.get("conditions", ()))
    return CliAttrs(id(link), rosname, rostype, traceability,
        original_name, conditions)

def convert_truth_srv(link):
    rosname = link["service"]
    rostype = link["srv_type"]
    traceability = convert_truth_traceability(link["traceability"])
    original_name = link.get("original_name", rosname)
    conditions = convert_truth_conditions(link.get("conditions", ()))
    return SrvAttrs(id(link), rosname, rostype, traceability,
        original_name, conditions)

def convert_truth_setter(link):
    rosname = link["parameter"]
    rostype = link["param_type"]
    traceability = convert_truth_traceability(link["traceability"])
    original_name = link.get("original_name", rosname)
    value = link.get("value")
    conditions = convert_truth_conditions(link.get("conditions", ()))
    return SetAttrs(id(link), rosname, rostype, traceability,
        original_name, value, conditions)

def convert_truth_getter(link):
    rosname = link["parameter"]
    rostype = link["param_type"]
    traceability = convert_truth_traceability(link["traceability"])
    original_name = link.get("original_name", rosname)
    value = link.get("default_value")
    conditions = convert_truth_conditions(link.get("conditions", ()))
    return GetAttrs(id(link), rosname, rostype, traceability,
        original_name, value, conditions)


def convert_truth_traceability(traceability):
    if traceability is None:
        return Location(None, None, None, None)
    return Location(traceability["package"], traceability["file"],
        traceability["line"], traceability["column"])

def convert_truth_conditions(paths):
    cfg = {}
    for path in paths:
        r = cfg
        for c in path:
            g = Guard(c["package"], c["file"], c["line"], c["column"],
                      c["statement"])
            s = r.get(g)
            if s is None:
                s = {}
                r[g] = s
            r = s
    return cfg

###############################################################################
# Helper Functions
###############################################################################

def rosname_match(rosname, expected, alt=None):
    parts = []
    prev = "/"
    n = len(rosname)
    i = 0
    assert n > 1 and rosname[0] == "/"
    for j in range(1, n):
        if rosname[j] == "?":
            assert prev != "?"
            if prev == "/":
                if j == n - 1: # self._name.endswith("/?")
                    # end, whole part for sure
                    parts.append(rosname[i:j])
                    parts.append("(.+?)")
                elif rosname[j+1] == "/": # "/?/"
                    # start and middle, whole parts
                    parts.append(rosname[i:j-1])
                    parts.append("(/.+?)?")
                else: # "/?a", optional part
                    parts.append(rosname[i:j])
                    parts.append("(.*?)")
            else: # "a?/", "a?a", "/a?", optional part
                parts.append(rosname[i:j])
                parts.append("(.*?)")
            i = j + 1
        prev = rosname[j]
    if i < n:
        parts.append(rosname[i:])
    parts.append("$")
    pattern = "".join(parts)
    m = re.match(pattern, expected)
    if not m and alt:
        return re.match(pattern, alt)
    return m


def _unfold_yaml(rosname, traceability, conditions, data):
    assert isinstance(data, dict) and len(data) > 0
    flog("unfold yaml for {!r}: {}".format(rosname, data))
    params = []
    stack = [("", rosname, data)]
    while stack:
        ns, key, value = stack.pop()
        name = _ns_join(key, ns)
        if not isinstance(value, dict):
            flog("create inner param {!r}: {!r}".format(name, value))
            params.append(ParamAttrs(name, name,
                _param_type(value), traceability, value, conditions))
        else:
            for key, other in value.items():
                flog("delegate yaml param (ns={!r}, name={!r})".format(name, key))
                stack.append((name, key, other))
    return params

def _ns_join(name, ns):
    """Dumb version of name resolution to mimic ROS behaviour."""
    if name.startswith("~") or name.startswith("/"):
        return name
    if ns == "~":
        return "~" + name
    if not ns:
        return name
    if ns[-1] == "/":
        return ns + name
    return ns + "/" + name

def _param_type(value):
    if value is None:
        return None
    if value is True or value is False:
        return "bool"
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "double"
    if isinstance(value, basestring):
        return "str"
    return "yaml"

###############################################################################
# Test Functions
###############################################################################

def _print_name_type_loc_costs(tests):
    for u, v, desc in tests:
        print(desc, cost_rosname_rostype_traceability(u, v))

if __name__ == "__main__":
    loc1 = Location("pkg", "file", 1, 1)
    loc2 = Location("pkg2", "file", 1, 1)
    loc3 = Location("pkg", "file2", 1, 1)
    loc4 = Location("pkg", "file", 2, 1)
    loc5 = Location("pkg", "file", 1, 2)
    loc6 = Location("pkg", "file", 1, None)
    loc7 = Location("pkg", "file", None, None)
    loc8 = Location("pkg", None, None, None)
    loc9 = Location(None, None, None, None)

    S = namedtuple("MinAttrs", ("rosname", "rostype", "traceability"))
    s1 = S("/a", "T", loc1)

    TESTS = (
        (s1, s1, "(-,-,-)"),
        (S("/a", "T", loc9), s1, "(-,-,?)"),
        (S("/a", None, loc1), s1, "(-,?,-)"),
        (S("/a", None, loc9), s1, "(-,?,?)"),
        (S("/?", "T", loc1), s1, "(?,-,-)"),
        (S("/?", "T", loc9), s1, "(?,-,?)"),
        (S("/?", None, loc1), s1, "(?,?,-)"),
        (S("/?", None, loc9), s1, "(?,?,?)"),
        (S("/a", "T", loc2), s1, "(-,-,x)"),
        (S("/a", "X", loc1), s1, "(-,x,-)"),
        (S("/a", "X", loc2), s1, "(-,x,x)"),
        (S("/b", "T", loc1), s1, "(x,-,-)"),
        (S("/b", "T", loc2), s1, "(x,-,x)"),
        (S("/b", "X", loc9), s1, "(x,x,-)"),
        (S("/b", "X", loc2), s1, "(x,x,x)"),
    )

    _print_name_type_loc_costs(TESTS)
