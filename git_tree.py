# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import json


class GitTree(object):

  def __init__(self, data_path, load=True):
    self.c = {}  # node -> list of children,
    self.p = {}
    self.data_path = data_path
    self.node_names = []
    if load:
      self._load()

  def _create_node_by_index(self, node_i):
    # create children and parent
    if not node_i in self.c:
      self.c[node_i] = []
    if not node_i in self.p:
      self.p[node_i] = -1

  def _create_node(self, node_name):
    node_i = -1
    for i in range(len(self.node_names)):
      if self.node_names[i] is None:
        # add it here
        node_i = i
        if node_name is None:
          self.node_names[i] = i
        else:
          self.node_names[i] = node_name
        break
    if node_i == -1:
      node_i = len(self.node_names)
      if node_name is None:
        self.node_names.append(node_i)
      else:
        self.node_names.append(node_name)
    self._create_node_by_index(node_i)
    return node_i

  def get_next_node_i(self):
    for i in range(len(self.node_names)):
      if self.node_names[i] is None:
        return i
    return len(self.node_names)

  def create_node(self, node_name):
    node_i = self._create_node(node_name)
    self._save()
    return node_i

  def set_node_name(self, index, name):
    self.node_names[index] = name
    self._save()

  def _add_edge(self, p, c):
    self.c[p].append(c)
    self.p[c] = p

  def _get_node_index(self, node_index_or_name):
    if isinstance(node_index_or_name, int):
      return node_index_or_name
    return self.node_names.index(node_index_or_name)

  def add_edge(self, p, c):
    self._add_edge(self._get_node_index(p), self._get_node_index(c))
    self._save()

  def get_parent(self, node_i_or_name):
    node_i = self._get_node_index(node_i_or_name)
    return self.p[node_i]

  def get_subedges(self, node_i):
    result = []
    for child in self.c[node_i]:
      result.append([node_i, child])
      result.extend(self.get_subedges(child))
    return result

  def move_one_edge(self, node_i_or_name, new_parent_i_or_name):
    node_i = self._get_node_index(node_i_or_name)
    new_parent_i = self._get_node_index(new_parent_i_or_name)
    #handle old parent
    old_parent = self.p[node_i]
    if old_parent >= 0:
      self.c[old_parent].remove(node_i)

    #handle new parent
    self.p[node_i] = new_parent_i
    if new_parent_i >= 0:
      self.c[new_parent_i].append(node_i)

    # handle old children
    for child in self.c[node_i]:
      self.p[child] = -1

    # reset new children
    self.c[node_i] = []
    self._save()

  def remove_node_by_index(self, node_i):
    self.move_one_edge(node_i, -1)
    self.p.pop(node_i)
    self.c.pop(node_i)
    self.node_names[node_i] = None
    self._save()

  def remove_node_by_name(self, node_name):
    node_i = self.node_names.index(node_name)
    if node_i >= 0:
      self.remove_node_by_index(node_i)

  def get_all_edges(self):
    result = []
    for node_i in self.c.keys():
      if self.p[node_i] == -1:
        # root node_i
        result.extend(self.get_subedges(node_i))
    return result

  def pprint(self, cb, current_node_name=None):

    for node_i in self.c.keys():
      if self.p[node_i] == -1:
        # root node_i
        self._pprint_tree(node_i, cb, current_node_name=current_node_name)

  def _pprint_tree(self,
                   node_i,
                   node_display_cb,
                   file=None,
                   _prefix="",
                   _last=True,
                   current_node_name=None):
    node_name = self.node_names[node_i]
    display_name = node_display_cb(node_name)
    if node_name.isnumeric() and int(node_name) == node_i:
      # don't show node name if it is same as the index
      display_prefix = ""
    else:
      display_prefix = "[%s]" % node_name
    msg = display_prefix + " : " + display_name
    if node_name == current_node_name:
      msg += "  <==============="

    print(
        _prefix, "`- " if _last else "|- ", node_i, " ", msg, sep="", file=file)
    _prefix += "   " if _last else "|  "
    child_count = len(self.c[node_i])
    for i, child in enumerate(self.c[node_i]):
      _last = i == (child_count - 1)
      self._pprint_tree(child, node_display_cb, file, _prefix, _last,
                        current_node_name)

  def _save(self):
    data = {"node_names": self.node_names, "edges": self.get_all_edges()}
    with open(self.data_path, "w") as fout:
      json.dump(data, fout)

  def _load(self):
    if not os.path.exists(self.data_path):
      self.node_names.append("master")
      self._save()

    with open(self.data_path) as fin:
      data = json.load(fin)
      self.node_names = data["node_names"]
      for node_i, node_name in enumerate(self.node_names):
        if node_name is None:
          continue
        self._create_node_by_index(node_i)
      for edge in data["edges"]:
        self._add_edge(edge[0], edge[1])

  def get_node_name(self, node_index):
    return self.node_names[node_index]
