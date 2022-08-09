def array_to_pages(array: list) -> dict:
    pages = {
        0: []
    }
    for element in array:
        last_page = list(pages)[-1]
        if len(pages[last_page]) == 5:
            pages[last_page + 1] = [element]
        else:
            pages[last_page].append(element)
    return pages
