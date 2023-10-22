#import <AVFoundation/AVFoundation.h>

void say(char* text) {
    NSString* string = [NSString stringWithFormat:@"%s", text];
    AVSpeechSynthesizer *synthesizer = [[AVSpeechSynthesizer alloc] init];  // init speaker
    AVSpeechUtterance *utterance = [[AVSpeechUtterance alloc] initWithString:string];  // init utterance
    [synthesizer speakUtterance:utterance];  // speak utterance
    CFRunLoopRunInMode(kCFRunLoopDefaultMode, 3.0, false);  // allow time for speaking to finish
}

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        say("I wish oranges came in purple.");
    }
    return 0;
}