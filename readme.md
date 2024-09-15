# Project README: Selenium WebDriver and BrowserMob Proxy HAR File Analysis

## Overview

This project demonstrates how to capture and analyze network traffic (HAR files) from websites using Selenium WebDriver and BrowserMob Proxy. The code fetches a website's network data, parses it, and provides a detailed analysis of HTTP status codes from the captured traffic. The data is saved in both HAR (HTTP Archive) format and a simple text report summarizing status codes (2XX, 4XX, and 5XX).

## Prerequisites

Before running the project, ensure the following dependencies and tools are installed and properly configured:

1. **Python**: Ensure that Python 3.x is installed.
2. **BrowserMob Proxy**: Download BrowserMob Proxy from the official repository:
   - Download Link: [BrowserMob Proxy GitHub](https://github.com/lightbody/browsermob-proxy/releases)
   - Extract the `browsermob-proxy-2.1.4-bin` folder to your local machine.
3. **Google Chrome**: The code uses the Chrome browser in headless mode, so ensure you have Chrome installed.
4. **Chrome WebDriver**: Download the Chrome WebDriver that matches your Chrome version from [ChromeDriver Downloads](https://sites.google.com/a/chromium.org/chromedriver/downloads) and place it in a known location (e.g., `C:/chromedriver.exe`).
5. **Python Packages**:
   - `selenium`
   - `browsermob-proxy`

   Install these using `pip`:

   ```bash
   pip install selenium browsermob-proxy
   ```

## Project Structure

```plaintext
root/
│
├── browsermob-proxy-2.1.4/          # BrowserMob Proxy directory
│   └── bin/
│       └── browsermob-proxy.bat     # Proxy server executable
├── exactspace_network_log1.har      # Captured HAR file from the website
├── network_log1.har                 # Intermediate HAR file
├── status_code_counts.txt           # Status code analysis report
├── har_parser.py                    # Main Python script
├── README.md                        # This documentation
└── chromedriver.exe                 # ChromeDriver executable
```

## Configuration and Setup

1. **BrowserMob Proxy Setup**:
   - After downloading and extracting BrowserMob Proxy, ensure the `browsermob-proxy.bat` file is accessible.
   - The `path_to_browsermobproxy` variable in the script should point to the `bin` folder inside the extracted BrowserMob Proxy folder.

   Example:

   ```python
   path_to_browsermobproxy = "C:\\path\\to\\browsermob-proxy-2.1.4\\bin\\"
   ```

2. **Chrome WebDriver Setup**:
   - Set the path to the Chrome WebDriver executable (`C:/chromedriver.exe`) in the script:

   ```python
   driver = webdriver.Chrome(executable_path="C:/chromedriver.exe", chrome_options=options)
   ```

## How to Run the Project

1. Download or clone the project repository.
2. Ensure you have set the correct paths for BrowserMob Proxy and ChromeDriver in the script.
3. Run the Python script using the command below:

   ```bash
   python har_parser.py
   ```

4. The script will:
   - Start the BrowserMob Proxy on port 8090.
   - Create a proxy server that captures HTTP traffic.
   - Launch Chrome in headless mode.
   - Visit the target website (`https://exactspace.co/`) and capture network requests.
   - Save the HAR data into a `.har` file.
   - Parse the HAR file and count status codes (2XX, 4XX, 5XX).
   - Save the status code analysis into a `status_code_counts.txt` file.

## Output

1. **HAR File**: 
   The `.har` file will contain all network requests and responses made while the website loaded.

   Example HAR file structure:

   ```json
   {
     "log": {
       "entries": [
         {
           "request": {
             "url": "https://example.com"
           },
           "response": {
             "status": 200
           }
         }
       ]
     }
   }
   ```

2. **Status Code Counts**: 
   After parsing the HAR file, the script outputs the following counts in the console and saves them to `status_code_counts.txt`:

   ```plaintext
   Total Status Code Count: X
   Total 2XX Status Code Count: X
   Total 4XX Status Code Count: X
   Total 5XX Status Code Count: X
   ```

## Key Sections of the Code

1. **Starting BrowserMob Proxy**:

   ```python
   server = Server(path_to_browsermobproxy + "browsermob-proxy.bat", options={'port': 8090})
   server.start()
   proxy = server.create_proxy(params={"trustAllServers": "true"})
   ```

   This sets up the proxy server to capture network traffic.

2. **Configuring Selenium WebDriver**:

   ```python
   options = webdriver.ChromeOptions()
   options.add_argument('headless')
   options.add_argument("--ignore-certificate-errors")
   options.add_argument("--proxy-server={0}".format(proxy.proxy))
   ```

   This configures Chrome to run in headless mode and directs traffic through the proxy.

3. **Capturing HAR File**:

   ```python
   proxy.new_har("exactspace.co/")
   driver.get("https://exactspace.co/")
   ```

   This captures the traffic data into a HAR file while loading the website.

4. **Analyzing Status Codes**:

   ```python
   status_codes = [entry['response']['status'] for entry in logs['log']['entries']]
   ```

   This parses the HAR file to count different HTTP response codes.

## Important Notes

- **Headless Mode**: The Chrome browser runs in headless mode, meaning there is no graphical user interface (GUI). This is useful for automated tasks like scraping and testing.
- **Error Handling**: Ensure proper error handling in case of network timeouts, website unavailability, or proxy configuration issues.
- **BrowserMob Proxy**: The project uses `browsermob-proxy-2.1.4`. If using a different version, paths and commands might change slightly.

## Future Improvements

- **Additional Analysis**: Extend the HAR file analysis to include content types, request durations, or other useful metrics.
- **Support for Multiple Browsers**: Add support for other browsers like Firefox using the Selenium WebDriver.
- **Exception Handling**: Implement better exception handling and logging for production-level usage.
