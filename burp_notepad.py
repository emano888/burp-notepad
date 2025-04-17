# -*- coding: utf-8 -*-
from burp import IBurpExtender, ITab
from java.awt import BorderLayout
from java.awt.datatransfer import DataFlavor
from javax.swing import JPanel, JTextArea, JButton, JScrollPane, JPopupMenu, JMenuItem
from threading import Thread, Lock
import ssl
import urllib2

class BurpExtender(IBurpExtender, ITab):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName("HTTP Notepad")

        # Create the UI components
        self.panel = JPanel(BorderLayout())
        self.text_area = JTextArea()
        self.send_button = JButton("Send Requests", actionPerformed=self.on_send_requests)

        # Create the right-click menu
        popup_menu = JPopupMenu()
        paste_item = JMenuItem("Paste URLs", actionPerformed=self.paste_urls)
        popup_menu.add(paste_item)

        self.text_area.setComponentPopupMenu(popup_menu)

        # Add components to panel
        self.panel.add(JScrollPane(self.text_area), BorderLayout.CENTER)
        self.panel.add(self.send_button, BorderLayout.SOUTH)

        # Register the tab
        callbacks.addSuiteTab(self)

    def getTabCaption(self):
        return "HTTP Notepad"

    def getUiComponent(self):
        return self.panel

    def on_send_requests(self, event):
        # Create a thread to handle sending requests
        thread = Thread(target=self.send_requests)
        thread.start()

    def send_requests(self):
        urls = self.text_area.getText().split('\n')
        threads = []
        results_lock = Lock()

        # Disable SSL certificate verification globally
        ssl._create_default_https_context = ssl._create_unverified_context

        def fetch_url(url):
            url = url.strip()
            if url:
                try:
                    print("Processing URL: {}".format(url))
                    
                    # Create request with custom User-Agent
                    req = urllib2.Request(url)
                    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0')

                    # Set up proxy
                    proxy_handler = urllib2.ProxyHandler({
                        'http': 'http://127.0.0.1:8080',
                        'https': 'http://127.0.0.1:8080'
                    })

                    opener = urllib2.build_opener(proxy_handler)

                    response = opener.open(req)
                    status_code = response.getcode()

                    with results_lock:
                        print("Response status: {} for URL: {}".format(status_code, url))
                except Exception as e:
                    with results_lock:
                        print("Error making request to {}: {}".format(url, e))

        for url in urls:
            thread = Thread(target=fetch_url, args=(url,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def paste_urls(self, event):
        clipboard = self.panel.getToolkit().getSystemClipboard()
        try:
            data = clipboard.getData(DataFlavor.stringFlavor)
            if data:
                self.text_area.append(data + '\n')
        except Exception as e:
            print("Error pasting data: {}".format(e))
