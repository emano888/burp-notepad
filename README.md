# 📝 HTTP Notepad for Burp Suite

HTTP Notepad is a simple Burp Suite extension that adds a custom tab where you can paste a list of URLs and send HTTP requests through Burp’s proxy with a single click.

## 🔧 Features

- Add a list of URLs (one per line)
- Send all requests through Burp Suite’s proxy
- Use clipboard with right-click → Paste URLs
- Designed for quick testing, automation, and recon

## 💡 How It Works

- All HTTP requests use `http://127.0.0.1:8080` as a proxy
- Multithreaded request handling
- Output shown in Burp's Extender console
 
## 📸 Preview

![HTTP Notepad Preview](preview.png)

The image displays the user interface of the **HTTP Notepad** tab within Burp Suite, featuring:

- A **large text area** where users can paste or type multiple URLs (one per line).
- A **"Send Requests"** button at the bottom to trigger HTTP requests.
- A **right-click context menu** with an option labeled **"Paste URLs"**, allowing users to paste links directly from the clipboard.
- Sample URLs shown in the notepad, such as:


The interface is simple and focused, allowing quick dispatch of HTTP requests through Burp's proxy for inspection and analysis.

## 📦 Installation

1. Build the Jython extension if needed.
2. Load the `.py` file inside Burp → Extender → Extensions → Add.
3. Select **Extension type: Python**.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

