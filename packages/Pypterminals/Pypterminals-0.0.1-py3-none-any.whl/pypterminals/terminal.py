import tkinter
import tkinter.scrolledtext
import tkinter.font
import threading
import traceback
import sys
AUTHOR = "binn@pigwow.cn"
NAME = "Pypterminals"
VERSION = "0.0.1"
PYPTERMINALS_THREAD_RUN_BEFORE = None #run before exec 运行前执行
PYPTERMINALS_THREAD_RUN_AFTER = None #run after exec 运行后执行
PYPTERMINALS_THREAD_RUN_ABNORMAL = None #runing abnormal exec 产生异常时执行
class Thread(threading.Thread):
    def run(self):
        global PYPTERMINALS_THREAD_RUN_BEFORE
        global PYPTERMINALS_THREAD_RUN_AFTER
        global PYPTERMINALS_THREAD_RUN_ABNORMAL
        try:
            if self._target:
                try:
                    if(PYPTERMINALS_THREAD_RUN_BEFORE):
                        PYPTERMINALS_THREAD_RUN_BEFORE()
                    self._target(*self._args, **self._kwargs)
                except:
                    sys.stderr.write("Exception in {} -> {}".format(self.__class__.__name__ , self.name))
                    traceback.print_exc()
                    if(PYPTERMINALS_THREAD_RUN_ABNORMAL):PYPTERMINALS_THREAD_RUN_ABNORMAL()
                else:
                    if(PYPTERMINALS_THREAD_RUN_AFTER):PYPTERMINALS_THREAD_RUN_AFTER()
        finally:
            # Avoid a refcycle if the thread is running a function with
            # an argument that has a member that points to the thread.
            del self._target, self._args, self._kwargs
class Terminal:
    '''A Tkinter Text widget that provides a scrolling display of console
        stderr and stdout.'''
    class __IORedirector__(object):
        '''A general class for redirecting I/O to this Text widget.'''
        def __init__(self, text_area):
            self.__text_area__ = text_area
    class __StdinRedirector__(__IORedirector__):
        def read(self):
            self.__text_area__.__std_print__(s)
    class __StdoutRedirector__(__IORedirector__):
        '''A class for redirecting stdout to this Text widget.'''
        def write(self, s):
            self.__text_area__.__std_print__(s)
    class __StderrRedirector__(__IORedirector__):
        '''A class for redirecting stderr to this Text widget.'''
        def write(self, str):
            self.__text_area__.__std_print__(str,True)
    __attribs__ = ("bg","fg",
                   "font_family","font_size",
                   "font_weight","font_slant",
                   "font_underline","font_strikeout")
    def __switch_weight__(self,weight:bool) -> str:
        """True to bold / False to normal"""
        return "bold" if(weight) else "normal"
    def __switch_slant__(self,slant:bool) -> str:
        """True to italic / False to roman"""
        return "italic" if(slant) else "roman"
    def __set_attrib__(self,s: str) -> list:
        """Set Tags & return encapsulated list data
        :param s: string
        :return: [{"tags":["f_red"...],"str":"out to terminal string"}]
        """
        """['','font_slant:True,fg:red...}}str','bg:green....}}str',...]"""
        result_list = []
        data_list = s.split("{{")
        # 细分组
        for i in data_list:
            result_dict = {"tags": [], "str": ""}
            """[''],['fg:red...','str']"""
            x = (i.split("}}"))
            if (len(x) == 1):
                result_dict["str"] = x[0]
            else:
                result_dict["str"] = x[1]
                """attrib:value 
                example:
                    -> [fg:red,bg:#fff,...]"""
                attrs = x[0].split(',')
                for a in attrs:
                    k,v = a.split(":")
                    """if fg in __attribs__"""
                    if(k in self.__attribs__):
                        if(k == "bg"):
                            self.term.tag_configure("b_" + v,background = v)
                            result_dict["tags"].append("b_" + v)
                        elif(k == "fg"):
                            self.term.tag_configure("f_" + v,foreground = v)
                            result_dict["tags"].append("f_" + v)
                        elif(k == "font_family"):
                            self.term.tag_configure(v,font = tkinter.font.Font(family=v))
                            result_dict["tags"].append(v)
                        elif(k == "font_size"):
                            self.term.tag_configure(v, font= tkinter.font.Font(size=int(v)))
                            result_dict["tags"].append(v)
                        elif(k == "font_weight"):
                            boolv = False if (v == "False" or v == "false") else True
                            self.term.tag_configure(self.__switch_weight__(boolv), font=tkinter.font.Font(
                                weight=self.__switch_weight__(boolv)
                            ))
                            result_dict["tags"].append(self.__switch_weight__(boolv))
                        elif(k == "font_slant"):
                            boolv = False if (v == "False" or v == "false") else True
                            self.term.tag_configure(self.__switch_slant__(boolv), font=tkinter.font.Font(
                                slant=self.__switch_slant__(boolv)
                            ))
                            result_dict["tags"].append(self.__switch_slant__(boolv))
                        elif(k == "font_underline"):
                            boolv = False if (v == "False" or v == "false") else True
                            if(boolv):
                                #self.term.tag_configure("underline",font = tkinter.font.Font(underline=True))
                                self.term.tag_configure("underline",underline = boolv)
                                result_dict["tags"].append("underline")
                            else:
                                self.term.tag_configure("n_underline", underline=boolv)
                                result_dict["tags"].append("n_underline")
                        elif(k == "font_strikeout"):
                            boolv = False if (v == "False" or v == "false") else True
                            if(boolv):
                                # self.term.tag_configure("overstrike",font = tkinter.font.Font(overstrike=True))
                                self.term.tag_configure("overstrike", overstrike=boolv)
                                result_dict["tags"].append("overstrike")
                            else:
                                self.term.tag_configure("n_overstrike", overstrike=boolv)
                                result_dict["tags"].append("n_overstrike")
                    else:
                    #    #pass
                    #    #self.win.destroy()
                        raise AssertionError("source str : {} -> {} \n argError unknown arg '{}' , It must be {}".format(s,a,k,self.__attribs__))
                    #print(self.term.tag_names())
            result_list.append(result_dict)
        return (result_list)
    def __get_text__(self,line:int,pb = False) -> str:
        """
        get cursor line text
        获得所在行的文本内容
        :param line: line number
        :param pb: include prompt? include(True) else (False)
        :return: string
        """
        if(pb):
            return self.term.get("{}.0".format(line),"{}.end".format(line))
        else:
            return self.term.get("{}.{}".format(line,self.__prompt_len__),"{}.end".format(line))
    def __del_text__(self,line:int,pb = False):
        """
        del cursor line text
        删除光标所在行的文本内容
        :param line: line number
        :param pb: include prompt? include(True) else (False)
        :return: string
        """
        if(pb):
            self.term.delete("{}.0".format(line), "{}.end".format(line))
        else:
            self.term.delete("{}.{}".format(line, self.__prompt_len__), "{}.end".format(line))
    def __select_bind__(self,event):
        self.term.mark_set('insert', 'end')
    def __mouse_bind__(self,event):
        self.term.mark_set('insert', '{}.end'.format(self.get_line_num()))
    def __key_bind__(self,event):
        if(self.shell):
            self.command["keycode"] = event.keycode
            self.command["keysym"] = str(event.keysym)
            self.command["text"] = self.__get_text__(self.get_cursor_line() - 1)
            if(event.keysym == "Return"):
                if(self.command["text"] == ""):self.__print_prompt__()
                command = self.__get_text__(self.get_cursor_line() - 1)
                if(command != ""):
                    if(command in self.history):
                        del(self.history[self.history.index(command)])
                    self.history.append(command)
                    if(self.shell_history_max == -1):pass
                    elif(len(self.history) > self.shell_history_max):
                        del(self.history[0])
                if(self.__command_func__):
                    self.__command_func__(self)
            elif (event.keysym == "BackSpace"):
                if(int(self.term.index("insert").split(".")[1]) < self.__prompt_len__):
                    self.term.insert("insert",self.prompt[-1])
            elif (event.keysym == "Prior" or event.keysym == "Next"):
                self.term.mark_set('insert', '{}.end'.format(self.get_line_num() + 1))
                #self.term.see('{}.end'.format(self.get_line_num() + 1))
            elif(event.keysym == "Home"):
                self.term.mark_set('insert', '{}.{}'.format(self.get_cursor_line(), self.__prompt_len__))
            elif(event.keysym == "Left" and self.get_cursor_char() < self.__prompt_len__):
                self.term.mark_set('insert', '{}.{}'.format(self.get_cursor_line(),self.__prompt_len__))
            elif(event.keysym == "Up"):
                """shell: press UP"""
                self.term.mark_set('insert', '{}.{}'.format(self.get_cursor_line() + 1,self.__prompt_len__))
                if (self.history):
                    """if have history 如果有历史记录"""
                    if(not self.__get_text__(self.get_cursor_line())):
                        """if prompt after no text 如果光标后面没有文本"""
                        self.term.insert("insert",self.history[-1])
                    else:
                        command = self.__get_text__(self.get_cursor_line())
                        if(command in self.history):
                            """如果光标的文本在历史记录中"""
                            self.__del_text__(self.get_cursor_line())
                            sub = self.history.index(command)
                            self.term.insert("insert", self.history[sub - 1])
                        else:
                            self.__del_text__(self.get_cursor_line())
                            self.term.insert("insert",self.history[-1])
            elif(event.keysym == "Down"):
                """shell: press DOWN"""
                if (self.history):
                    """if have history 如果有历史记录"""
                    if (not self.__get_text__(self.get_cursor_line())):
                        """if prompt after no text 如果光标后面没有文本"""
                        self.term.insert("insert", self.history[-1])
                    else:
                        command = self.__get_text__(self.get_cursor_line())
                        if (command in self.history):
                            """如果光标的文本在历史记录中"""
                            tmp_history = self.history[::-1]
                            self.__del_text__(self.get_cursor_line())
                            sub = tmp_history.index(command)
                            self.term.insert("insert", tmp_history[sub - 1])
                        else:
                            self.__del_text__(self.get_cursor_line())
                            self.term.insert("insert", self.history[-1])
        else:
            self.term.mark_set('insert', '{}.end'.format(self.get_line_num() + 1))
        self.__clear_buf__()
    def __clear__(self,event):
        self.clear()
    def __clear_buf__(self):
        if (self.get_line_num() > int(self.line_buf)):
            self.term.delete("1.0", "{}.0".format(self.get_line_num() + 1 - int(self.line_buf)))
    def __print_prompt__(self):
        if(self.prompt):
            s_list = self.__set_attrib__(str(self.prompt))
            state = self.term["state"]
            self.term["state"] = "normal"
            for i in s_list:
                self.term.insert("insert", i["str"], i["tags"])
            self.term["state"] = state
            self.__clear_buf__()
    def __get_prompt_str__(self):
        if(self.prompt):
            return "".join(
                list(map(lambda dic:dic["str"],self.__set_attrib__(self.prompt)))
                        )
    def clear(self):
        state = self.term["state"]
        self.term["state"] = "normal"
        self.term.delete("0.0", 'end')
        if(self.shell):
            self.__print_prompt__()
        self.term["state"] = state
    def get_line_num(self):
        """get line number"""
        return int(self.term.index("end-1c").split(".")[0])
    def get_cursor_line(self):
        return int(self.get_cursor_index()[0])
    def get_cursor_char(self):
        return int(self.get_cursor_index()[1])
    def get_cursor_index(self):
        return tuple(self.term.index("insert").split("."))
    def get_text(self,pb=False):
        return self.__get_text__(self.get_cursor_line(),pb)
    def command_event(self,func):
        """set key[Enter] event"""
        self.__command_func__ = func
    def set_exec_before(self,func):
        global PYPTERMINALS_THREAD_RUN_BEFORE
        PYPTERMINALS_THREAD_RUN_BEFORE = func
    def set_exec_after(self,func):
        global PYPTERMINALS_THREAD_RUN_AFTER
        PYPTERMINALS_THREAD_RUN_AFTER = func
    def set_exec_abnormal(self,func):
        global PYPTERMINALS_THREAD_RUN_ABNORMAL
        PYPTERMINALS_THREAD_RUN_ABNORMAL = func
    def set_stdout(self):
        sys.stdout = self.__stdout__
    def set_stderr(self):
        sys.stderr = self.__stderr__
    def __init__(self,func=None,**args):
        """Create terminal window.
        :param func: set run function
        :param args:
            -> title: set the window title
            -> line_width: set the maximum number of characters per line (default is Maximum screen WIDTH pixels / 18 - 2)
            -> line_height: set the number of visible lines of term (default is Maximum screen HEIGHT pixels / 38 - 2)
            -> line_buf: set line buf (default is "line_hight" * 30)
            -> bg: set the window background color(default "black")
            -> fg: set the window foreground color(default "white")
            -> cursor: set the window cursor(default "spider")
            -> term_cursor_width: set the terminal cursor width(default 1 pixel)
            -> term_cursor_color: set the terminal cursor color(default "white")
            -> shell: set keyboard input allowed(shell mode) (default False)
            -> shell_history_max: set the maximum history storage in shell mode (default 30).if set -1 infinite
            -> shell_stderr: set font&color attribs for STDERR (default {{fg:#FFFF00}})
            -> tool_window: create tool window (default False) if set True , window Z order top
            -> scrolled: enable or disable[True or False] (default False)
            -> font: set the window default font
                -> tuple(-- family:str,
                        -- size:int,
                        -- weight:bool, -> bold(True),normal(False)[default]
                        -- slant:bool, -> italic(True),normal(False)[default]
                        -- underline:bool -> underline(True),normal(False)[default]
                        -- strikeout:bool -> strikeout(True),normal(False)[default]
                        )
                -> example1: process_terminal = terminal.Terminal(font = (None,13,True))
                -> example2: process_terminal = terminal.Terminal(font = ("Helvetica",13,True,False,True,False))
            -> font_family: set default font-family (str)
            -> font_size: set default font-size (int)
            -> font_weight: set default font-weight:bool -> bold(True),normal(False)[default]
            -> font_slant: set default font-slant:bool -> italic(True),normal(False)[default]
            -> font_underline: set default font-underline:bool -> underline(True),normal(False)[default]
            -> font_strikeout: set default font-strikeout:bool -> strikeout(True),normal(False)[default]
            -> padding_x: set the distance between the two sides of the x-axis of the terminal window.
                default 1 pixel
            -> padding_y: set the distance between the two sides of the y-axis of the terminal window.
                default 3 pixel
            -> prompt: set the window prompt.
                -> example: process_terminal = terminal.Terminal(prompt:">>> ")
                -> a set color example: process_terminal = terminal.Terminal(prompt:"{{fg:red,bg:#737F7F}}>>> ")
                -> a set color&font example: process_terminal = terminal.Terminal(prompt:"{{fg:red,bg:#737F7F,font_underline:True}}>>> ")
        """
        self.win = tkinter.Tk()
        self.get_text_of_line = self.__get_text__
        """stdout and stderr """
        self.__stdout__ = Terminal.__StdoutRedirector__(self)
        self.__stderr__ = Terminal.__StderrRedirector__(self)
        """exec thread"""
        self.thread = None
        self.thread_is_alive = False
        self.thread_stop_cllback = None
        if(func):
            self.thread = Thread(target=func,args=(self,),name=NAME + "_exec_thread")
            self.thread.daemon = True
        """window config"""
        self.history = []
        self.shell_history_max = 30
        self.shell_stderr = "{{fg:#FFFF00}}"
        self.__command_func__ = None
        self.command = {"keycode":None,"keysym":"","text":""}
        self.title = NAME
        self.line_width = int(self.win.winfo_screenwidth() / 18 -2)
        self.line_height = int(self.win.winfo_screenheight() / 30 - 2)
        self.line_buf = self.line_height * 20
        self.bg = "black"
        self.fg = "white"
        self.cursor = "spider"
        self.term_cursor_width = 1
        self.term_cursor_color = "white"
        self.shell = False
        self.tool_window = True
        self.scrolled = False
        self.font = None
        self.__font__ = {}
        self.padding_x = 1
        self.padding_y = 3
        self.__config__ = {"relief": "flat",
                           "background": self.bg,
                           "foreground": self.fg,
                           "cursor": self.cursor,
                           "insertwidth": self.term_cursor_width,
                           "insertbackground": self.term_cursor_color,
                           "state": "disabled",  # False
                           "width": self.line_width,
                           "height": self.line_height,
                           }
        self.prompt = None
        self.__prompt_len__ = 0
        for k,v in args.items():
            if(k == "title"):self.title = v
            elif(k == "line_width"):self.__config__["width"] = self.line_width = v
            elif(k == "line_height"):self.__config__["height"] = self.line_height = v
            elif(k == "line_buf"):self.line_buf = v
            elif(k == "bg"):self.__config__["background"] = self.bg = v
            elif(k == "fg"):self.__config__["foreground"] = self.fg = v
            elif(k == "cursor"):self.__config__["cursor"] = self.cursor = v
            elif(k == "term_cursor_width"):self.__config__["insertwidth"] = self.term_cursor_width = v
            elif(k == "term_cursor_color"):self.__config__["insertbackground"] = self.term_cursor_color = v
            elif(k == "shell"):
                self.shell = v
                if(self.shell):self.__config__["state"] = "normal"
            elif(k == "shell_history_max"):self.shell_history_max = v
            elif(k == "tool_window"):self.tool_window = v
            elif(k == "scrolled"):self.scrolled = v
            elif(k == "font"):
                if(not type(v) is tuple):
                    win.destroy()
                    raise AssertionError("TypeError arg '{}' It must be tuple. but you did '{}' ".format(k,v))
                font_modal = ("family","size","weight","slant","underline","overstrike")
                tmp_dict = {}
                config_dict = {}
                for i in range(len(v)):
                    tmp_dict.update({font_modal[i]: v[i]})
                    if (font_modal[i] == "weight"):
                        """True to bold / False to normal"""
                        config_dict.update({font_modal[i]:self.__switch_weight__(v[i])})
                    elif (font_modal[i] == "slant"):
                        """True to italic / False to roman"""
                        config_dict.update({font_modal[i]:self.__switch_slant__(v[i])})
                    else:
                        config_dict.update({font_modal[i]:v[i]})
                ft = tkinter.font.Font(**config_dict)
                self.font = tmp_dict
                self.__config__["font"] = ft
            elif(k == "font_family"):
                self.__font__.update({"family":v})
            elif(k == "font_size"):
                self.__font__.update({"size":v})
            elif(k == "font_weight"):
                self.__font__.update({"weight": self.__switch_weight__(v)})
            elif(k == "font_slant"):
                self.__font__.update({"slant":self.__switch_slant__(v)})
            elif(k == "font_underline"):
                self.__font__.update({"underline": v})
            elif(k == "font_strikeout"):
                self.__font__.update({"overstrike": v})
            elif(k == "padding_x"):self.padding_x = v
            elif(k == "prompt"):self.prompt = v
        if(not self.font):
            self.__config__["font"] = tkinter.font.Font(**self.__font__)
        self.win.title(self.title)
        self.win["background"] = self.bg
        self.win["cursor"] = self.cursor
        self.win["relief"] = "flat"
        self.win.resizable(width=False, height=False)
        if(self.tool_window):
            self.win.wm_attributes('-topmost',True)
        self.win.attributes('-toolwindow', self.tool_window)
        if (self.scrolled): self.term = tkinter.scrolledtext.ScrolledText(self.win, **self.__config__)
        else:self.term = tkinter.Text(self.win, **self.__config__)
        self.term.pack(fill=tkinter.X,padx = self.padding_x,pady = self.padding_y)
        """get prompt string lenght"""
        if (self.prompt):
            for i in self.__set_attrib__(self.prompt):
                for k, v in i.items():
                    if (k == "str"):
                        self.__prompt_len__ += len(v)
            if(self.shell):self.__print_prompt__()
        self.win.bind("<Key>",self.__key_bind__)
        self.win.bind("<ButtonPress>", self.__mouse_bind__)
        self.win.bind("<B1-Motion>", self.__mouse_bind__)
        self.win.bind("<ButtonRelease>",self.__mouse_bind__)
        self.win.bind("<Control-Delete>",self.__clear__)
        self.win.bind("<<Selection>>",self.__select_bind__)
        self.term.focus_set()
        #self.__std_print__("{{fg:green}}7")
    def bind_clear_key(self,keys:str):
        self.win.bind(keys, self.__clear__)
    def close(self):
        self.win.destroy()
    def winloop(self):
        if(self.thread):
            #self.thread.start()
            self.thread.start()
            self.thread_is_alive = self.thread.is_alive()
            #print("exec", self.thread.is_alive())
        self.win.mainloop()
    def __std_print__(self,s:any,is_stderr = False):
        state = self.term["state"]
        self.term["state"] = "normal"
        if (is_stderr):s = self.shell_stderr + str(s)
        else:s = str(s)
        #stdout
        if(not is_stderr):
            if (self.shell and self.prompt and s != "\n"):
                if(self.get_cursor_line() == 1):
                    self.term.insert("insert", "\n")
                else:
                    line_str = self.__get_text__(self.get_cursor_line(),pb=True)
                    if (line_str == self.__get_prompt_str__()):
                        self.term.insert("insert", "\n")
            elif (not self.shell and self.prompt and s != "\n"):
                if (self.get_cursor_line() == 1):
                    self.__print_prompt__()
        #stderr
        else:
            line_str = self.__get_text__(self.get_cursor_line(),pb=True)
            if (line_str == self.__get_prompt_str__()):
                self.term.insert("insert", "\n")
        s_list = self.__set_attrib__(s)
        for i in  s_list:
            self.term.insert("insert", i["str"],i["tags"])
        if(not is_stderr):
            if (self.get_cursor_char() == 0):
                self.__print_prompt__()
        self.term["state"] = state
        self.__clear_buf__()
        self.term.see("end")

    def print(self, s: any, *kwargs, sep=' ', end='\n'):
        """print(s,...,sep = ' ',end = '\n')"""
        state = self.term["state"]
        self.term["state"] = "normal"
        self.term.mark_set("insert", "end")
        s_list = self.__set_attrib__(str(s))
        if (self.get_cursor_char() == 0): self.__print_prompt__()
        #if(self.prompt):
        #    if(self.shell):
        #        self.term.insert("insert", "\n")
        #    else:self.__print_prompt__()
        for i in s_list:
            self.term.insert("insert", i["str"], i["tags"])
        for kw in kwargs:
            self.term.insert("insert", sep)
            s_list = self.__set_attrib__(str(kw))
            for pkw in s_list:
                self.term.insert("insert", pkw["str"], pkw["tags"])
        self.term.insert("insert", end)
        #if (end == "\n" and self.shell):
        if (end == "\n"):self.__print_prompt__()
        self.term["state"] = state
        self.__clear_buf__()
        self.term.see("end")