import webview
import sys

if __name__ == '__main__':
    window = webview.create_window(str(sys.argv[1:]), 'https://alvinwan.com/blog')
    webview.start()