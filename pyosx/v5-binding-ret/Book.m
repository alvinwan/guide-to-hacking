#import <Foundation/Foundation.h>
#import <AddressBook/AddressBook.h>

const char *getAddressBookFirstEntry() {
    ABAddressBook *addressBook = [ABAddressBook addressBook];  // get address book
    NSArray<ABRecord *> *people = [addressBook people];  // get people

    NSCAssert(people.count > 0, @"Address book is empty");  // check there are people
    
    ABRecord *person = people[0];  // get first person
    NSString *displayName = [person displayName]; // get person's display name
    return [displayName UTF8String];
}

// This below main function is optional. This is useful if you'd like to debug
// and ensure that the above function operates correctly. This way, you can
// run the `getAddressBookFirstEntry` function in Objective-C, independent of
// the Python binding code.
//
// If you *do decide to write the below function for testing, note that we had
// to wrap the `getAddressBookFirstEntry`'s returned string with an ObjC
// NSString before logging.
int main(int argc, const char * argv[]) {
    @autoreleasepool {
        NSString *string = [[NSString alloc] initWithUTF8String: getAddressBookFirstEntry()];
        NSLog(@"%@", string);
    }
    return 0;
}