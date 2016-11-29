from collections import OrderedDict

class OrderedDictWithPrepend(OrderedDict):
    """
    Extends OrderedDict functionality by adding 'prepend' method.
    Format is: <instance>.prepend(_key, value)
    """
    def prepend(self, key, value, dict_setitem=dict.__setitem__):
        # Python3
        try:
            self.update({key:value})
            self.move_to_end(key,last=False)
            
        # Python2
        except:
            root = self._OrderedDict__root
            first = root[1]

            if key in self:
                link = self._OrderedDict__map[key]
                link_prev, link_next, _ = link
                link_prev[1] = link_next
                link_next[0] = link_prev
                link[0] = root
                link[1] = first
                root[1] = first[0] = link
            else:
                root[1] = first[0] = self._OrderedDict__map[key] = [root, first, key]
                dict_setitem(self, key, value)