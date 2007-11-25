import Webwidgets, sys, os, os.path

class WidgetTree(Webwidgets.Tree):
    class TreeModel(Webwidgets.TreeModel):
        root = None
        class Node(Webwidgets.TreeModelGroupingWrapperNode):
             class Node(Webwidgets.TreeModelNode):
                 def __init__(self, tree, parent = None, obj = None):
                      if obj is None:
                          obj = tree.root
                      Webwidgets.Tree.TreeModel.Node.__init__(
                           self, tree, parent, getattr(obj, '__name__', 'No root object'))
                      self.value = obj
                      self.updated = False
                      self.cache = Webwidgets.Utils.OrderedDict()

                 class SubNodes(object):
                     def __get__(self, instance, owner):
                         if not instance.updated:
                             instance.cache.clear()
                             if instance.value is not None:
                                 for name, value in instance.value.__dict__.iteritems():
                                     if issubclass(value, Webwidgets.Widget):
                                         instance.cache[name] = owner(
                                             instance.tree, instance, value)
                             instance.cache.order.sort()
                             instance.updated = True
                         return instance.cache
                 sub_nodes = SubNodes()

                 class Expandable(object):
                     def __get__(self, instance, owner):
                         return not instance.updated or len(instance.sub_nodes) > 0
                 expandable = Expandable()
