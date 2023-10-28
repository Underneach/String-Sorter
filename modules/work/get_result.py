import colorama


def Get_result(self) -> None:  # Получаем результаты работы процессов

    for job in self.jobs_list:
        try:
            request, extracted_data, string_type = job
            if request and extracted_data is not None:
                self.results[request]['extracted_data'].append(extracted_data)
            elif string_type is True:
                self.invalid_lines += 1
        except Exception as e:
            print(e)
        '''
        except Exception as e:
            print(f'[{colorama.Fore.LIGHTRED_EX}-{colorama.Style.RESET_ALL}] Ошибка получения данных : {colorama.Fore.LIGHTRED_EX}{str(e)}{colorama.Style.RESET_ALL}')
        '''
