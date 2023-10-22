from AddressBook import ABAddressBook


def get_address_book_first_entry():
    book = ABAddressBook.sharedAddressBook()  # get address book
    people = book.people()  # get people

    assert people.count() > 0, "Address book is empty"  # check there are people

    person = people[0]  # get first person
    display = person.displayName()  # get person's display name
    return display


if __name__ == '__main__':
    print(get_address_book_first_entry())