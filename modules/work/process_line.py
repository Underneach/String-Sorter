import re
from typing import Union, Tuple


def Process_Line(self, line) -> Tuple[Union[str, None], Union[str, None], bool]:
    try:
        if re.match(self.invalid_pattern, line):
            return None, None, True

        for request in self.search_requests:
            result = re.search(self.results[request]['compile_request'], line)
            if result:
                return request, result.group(1), False

        return None, None, False

    except Exception:
        return None, None, True
