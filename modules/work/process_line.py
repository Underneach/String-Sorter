import re


def Process_Line(self, line) -> (str, str, bool) or (None, None, bool):

    try:

        if len(line) > 200 or 'UNKOWN' in line:
            return None, None, True

        for request in self.search_requests:
            result = re.search(self.results[request]['compile_request'], line)

            if result:
                extracted_data = result.group(1)
                return request, extracted_data, False
            else:
                return None, None, False

    except Exception as e:
        print(e)
        return None, None, True
