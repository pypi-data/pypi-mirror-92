import terminal
import multiprocessing
import time
def test():
    term = terminal.Terminal(func = thread_test,
                             tool_window = True,
                             shell=True,
                             shell_history_max=-1,
                             font_size=20,
                             scrolled = False,
                          prompt="[{{fg:#FFFF00,font_family:Arial,font_size:13}}Arial{{fg:white}}]")
    term.set_stdout()
    term.set_stderr()
    print("test")
    term.print("test")
    print("test")
    term.command_event(run_command)
    term.set_exec_before(before)
    term.set_exec_after(after)
    term.set_exec_abnormal(abnormal)
    term.winloop()
def thread_test(term):
    for i in range(3):
        print(i)
        term.print(i)
        raise BaseException("test abnormal")
def run_command(term):
    command_dict={"clear":"term.clear()",
                  "show history":"print(term.history)",
                  "show title":"print(term.title)",
                  "version":"print(terminal.NAME,terminal.VERSION)",
                  "":"pass"}
    command = term.command
    if(command["keycode"] == 13):
        if(command["text"] in command_dict):
            exec(command_dict.get(command["text"]))
        else:
            print("command",command["text"],"not found.")
def before():
    print("Thread execution before...")
def after():
    print("Thread execution completed...")
def abnormal():
    print("Thread execution abnormal...")
if __name__ == "__main__":
    p = multiprocessing.Process(target=test)
    p.start()
