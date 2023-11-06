from chardet.universaldetector import UniversalDetector


def Get_encoding(self, file_path: str) -> str:
    detector = UniversalDetector()

    try:
        with open(file_path, 'rb') as file:
            for line in file:
                detector.feed(line)
                if detector.done:
                    break
            detector.close()
            return detector.result['encoding']
    except Exception as e:
        print(f'[{colorama.Fore.LIGHTRED_EX}-{colorama.Style.RESET_ALL}] {colorama.Fore.LIGHTBLUE_EX}{file_path}{colorama.Style.RESET_ALL} : Ошибка определения кодировки : {colorama.Fore.LIGHTRED_EX}{str(e)}{colorama.Style.RESET_ALL}')
        return 'utf-8'
