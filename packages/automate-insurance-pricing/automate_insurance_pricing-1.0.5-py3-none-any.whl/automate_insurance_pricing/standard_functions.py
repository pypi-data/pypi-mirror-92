from datetime import date


def addYears(d, years):
    """ Gets a new date after adding a number of years to an initial date"""

    try:
    #Return same day of the current year        
        return d.replace(year = d.year + years)
    except ValueError:
    #If not same day, it will return other, i.e.  February 29 to March 1 etc.        
        return d + (date(d.year + years, 1, 1) - date(d.year, 1, 1))


def remove_words(word, **kwargs):
    """
        Replaces part of the word by another value \n \
        Arguments --> the word that has parts to be replaced, \n \
            the kwargs represent the parts of the word to replace and the value to use instead, \n \ 
            for example (first_replace=('variable', 'feature')) will make the function replace the word variable by feature \n \
        Returns --> the new word with the desired parts replaced
    """

    for word_to_remove in kwargs.values():
        word = word.replace(word_to_remove[0], word_to_remove[1])

    return word


def get_list_from_list(init_list, list_to_check, is_in_list=True):
    """ Generates a list from a initial one \n \
        Arguments --> init_list is the one we loop through, \n \
            list_to_check is the list that gathers the items to take or to remove, \n \
            is_in_list is the boolean indicating if items from list_to_check must be removed or kept from the initial list \n \
        Returns --> the new list
    """
    if isinstance(list_to_check, str) == True:
        list_to_keep = [element for element in init_list if list_to_check in element] if is_in_list == True else [element for element in init_list if list_to_check not in element]
    else:
        list_to_keep = [element for element in init_list if element in list_to_check] if is_in_list == True else [element for element in init_list if element not in list_to_check]

    return list_to_keep