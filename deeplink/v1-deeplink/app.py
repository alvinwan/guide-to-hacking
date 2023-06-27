import webview

if __name__ == '__main__':
    window = webview.create_window('Hello world', 'https://alvinwan.com/blog')
    webview.start()