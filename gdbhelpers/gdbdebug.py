#
# gdb helper commands and functions for Linux kernel debugging
#
#  Proc Kernel information reader
#
# Copyright (c) 2016 Linaro Ltd
#
# Authors:
#  Kieran Bingham <kieran.bingham@linaro.org>
#
# This work is licensed under the terms of the GNU GPL version 2.
#

import gdb

from gdbhelpers import utils
thread_info = utils.CachedType("struct thread_info")

def print_thread_list_item(item):
    gdb.write('Thread: '
              '{num} ({pid},{lwp},{tid})\n'.format(
                  num=item['num'],
                  pid=item['ptid']['pid'],
                  lwp=item['ptid']['lwp'],
                  tid=item['ptid']['tid']
              ))

def print_thread_list(head):
    if (head.type == thread_info.get_type().pointer()):
        head = head.dereference()
    #elif (head.type != thread_info.get_type()):
    #    raise gdb.GdbError('argument must be of type (struct thread_info [*])')
    c = head
    try:
        gdb.write("Starting with: {}\n".format(c))
    except gdb.MemoryError:
        gdb.write('head is not accessible\n')
        return
    while c.address:
        print_thread_list_item(c)
        c = c['next'].dereference()




class GDBThreadList(gdb.Command):
    """ Iterate the struct thread_info thread_list.
    Show gdb-threads created for the inferior
    """

    def __init__(self):
        super(GDBThreadList, self).__init__("gdb-threadlist", gdb.COMMAND_DATA)

    def invoke(self, arg, from_tty):
        gdb.write("thread_list: \n")
        print_thread_list(gdb.parse_and_eval("thread_list"))

GDBThreadList()
