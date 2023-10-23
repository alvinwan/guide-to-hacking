#import <AVFoundation/AVFoundation.h>

void say(char* text) {  // accept C-style string
    NSString* string = [NSString stringWithFormat:@"%s", text];  // wrap in ObjC-style string
    AVSpeechSynthesizer *synthesizer = [[AVSpeechSynthesizer alloc] init];  // init speaker
    AVSpeechUtterance *utterance = [[AVSpeechUtterance alloc] initWithString:string];  // init utterance
    [synthesizer speakUtterance:utterance];  // speak utterance
    CFRunLoopRunInMode(kCFRunLoopDefaultMode, 3.0, false);  // allow time for speaking to finish
}

// This below main function is optional. This is useful if you'd like to debug
// and ensure that the above function operates correctly. This way, you can
// run the `getAddressBookFirstEntry` function in Objective-C, independent of
// the Python binding code.
//
// If you *do decide to write the below function for testing, note that instead
// of passing an NSString to the `say` function (denoted by a string prefixed
// with an @, like @"I wish ..."), we passed a normal C-style string without the
// @ prefix.
int main(int argc, const char * argv[]) {
    @autoreleasepool {
        say("I wish oranges came in purple.");
    }
    return 0;
}