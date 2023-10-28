import colorama

from modules.work.process_line import Process_Line


def Process_Lines(self, lines, pool, progress_bar, file_path):
    try:
        self.jobs_list = pool.starmap(Process_Line, [(self, line) for line in lines])
        check_lines = len(lines)
        progress_bar.update(check_lines)
        self.checked_lines += check_lines
    except Exception as e:
        print(f'[{colorama.Fore.LIGHTRED_EX}-{colorama.Style.RESET_ALL}] {colorama.Fore.LIGHTBLUE_EX}{file_path}{colorama.Style.RESET_ALL} : Ошибка пула процессоров : {colorama.Fore.LIGHTRED_EX}{str(e)}{colorama.Style.RESET_ALL}')
