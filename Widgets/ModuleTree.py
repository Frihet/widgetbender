import Webwidgets, sys, os, os.path

class ModuleTree(Webwidgets.Tree):
     class TreeModel(Webwidgets.TreeModel):
         class Node(Webwidgets.TreeModelGroupingWrapperNode):
             class Node(Webwidgets.TreeModelNode):
                 def __init__(self, tree, parent = None, mod = None):
                      assert mod != ''
                      if mod is None:
                           name = 'Modules'
                      else:
                           name = mod.__name__.split('.')[-1]
                      Webwidgets.Tree.TreeModel.Node.__init__(
                           self, tree, parent, name)
                      self.value = mod
                      self.updated = False
                      self.cache = {}

                 class SubNodes(object):
                     def __get__(self, instance, owner):
                         path = []
                         if instance.value is None:
                             path = sys.path
                         elif hasattr(instance.value, '__path__'):
                             path = instance.value.__path__
                         module_prefix = ''
                         if instance.value is not None:
                             module_prefix = instance.value.__name__ + '.'
                         for pth in path:
                             try:
                                 stat_info = os.stat(pth)
                             except:
                                 continue
                             if (   pth not in instance.cache
                                 or stat_info.st_mtime != instance.cache[pth]['stat_info'].st_mtime):
                                 files = []
                                 try:
                                     files = os.listdir(pth)
                                 except:
                                     pass
                                 mods = []
                                 for file in files:
                                     mod, ext = os.path.splitext(file)
                                     if ext in ('.py', '.wwml'):
                                         mods.append(mod)
                                     elif mod and not ext:
                                         filepth = os.path.join(pth, file)
                                         if os.path.isdir(filepth):
                                             mods.append(mod)
                                 modules_nodes = Webwidgets.Utils.OrderedDict()
                                 for mod in mods:
                                     try:
                                         sub_module = Webwidgets.Utils.load_class(
                                             module_prefix + mod)
                                     except:
                                         pass
                                     else:
                                         modules_nodes[mod] = owner(
                                             instance.tree, instance, sub_module)
                                 instance.cache[pth] = {
                                     'stat_info': stat_info,
                                     'modules': modules_nodes}
                         instance.updated = True

                         res = Webwidgets.Utils.OrderedDict()
                         for cached in instance.cache.itervalues():
                             res.update(cached['modules'])
                         res.order.sort()

                         return res
                 sub_nodes = SubNodes()

                 class Expandable(object):
                     def __get__(self, instance, owner):
                         return not instance.updated or len(instance.sub_nodes) > 0
                 expandable = Expandable()
