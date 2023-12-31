#import <Foundation/Foundation.h>
#import <AddressBook/AddressBook.h>

NSString *getAddressBookFirstEntry() {
    ABAddressBook *addressBook = [ABAddressBook addressBook];  // get address book
    NSArray<ABRecord *> *people = [addressBook people];  // get people

    NSCAssert(people.count > 0, @"Address book is empty");  // check there are people
    
    ABRecord *person = people[0];  // get first person
    NSString *displayName = [person displayName]; // get person's display name
    return displayName;
}

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        NSLog(@"%@", getAddressBookFirstEntry());
    }
    return 0;
}