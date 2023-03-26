# Import the required modules
from selenium import webdriver
from browsermobproxy import Server
import time
import json


# Main Function
if __name__ == "__main__":

	# Enter the path of bin folder by
	# extracting browsermob-proxy-2.1.4-bin
	path_to_browsermobproxy = "C:\\Users\\anshi\\Downloads\\browsermob-proxy-2.1.4\\bin\\"

	# Start the server with the path and port 8090
	server = Server(path_to_browsermobproxy
					+ "browsermob-proxy.bat", options={'port': 8090})
	server.start()

	# Create the proxy with following parameter as true
	proxy = server.create_proxy(params={"trustAllServers": "true"})

	# Create the webdriver object and pass the arguments
	options = webdriver.ChromeOptions()

	# Chrome will start in Headless mode
	options.add_argument('headless')

	# Ignores any certificate errors if there is any
	options.add_argument("--ignore-certificate-errors")

	# Setting up Proxy for chrome
	options.add_argument("--proxy-server={0}".format(proxy.proxy))

	# Startup the chrome webdriver with executable path and
	# the chrome options as parameters.
	driver = webdriver.Chrome(executable_path="C:/chromedriver.exe",
							chrome_options=options)

	# Create a new HAR file of the following domain
	# using the proxy.
	proxy.new_har("exactspace.co/")

	# Send a request to the website and let it load
	driver.get("https://exactspace.co/")

	# Write it to a HAR file.
	with open("exactspace_network_log1.har", "w", encoding="utf-8") as f:
		f.write(json.dumps(proxy.har))

	print("Quitting Selenium WebDriver")
	driver.quit()

	# Read HAR File and parse it using JSON
	# to find the urls containing images.
	har_file_path = "network_log1.har"
	with open(har_file_path, "r", encoding="utf-8") as f:
		logs = json.loads(f.read())
		
# Parse the JSON object to get status code counts
status_codes = [entry['response']['status'] for entry in logs['log']['entries']]
total_count = len(status_codes)
two_xx_count = status_codes.count(200) + status_codes.count(201) + status_codes.count(202) + status_codes.count(204)
four_xx_count = status_codes.count(400) + status_codes.count(401) + status_codes.count(403) + status_codes.count(404) + status_codes.count(422)
five_xx_count = status_codes.count(500) + status_codes.count(502) + status_codes.count(503) + status_codes.count(504)

# Print the counts to console
print(f'Total Status Code Count: {total_count}')
print(f'Total 2XX Status Code Count: {two_xx_count}')
print(f'Total 4XX Status Code Count: {four_xx_count}')
print(f'Total 5XX Status Code Count: {five_xx_count}')

# Save the counts to a text file
with open('status_code_counts.txt', 'w') as output_file:
    output_file.write(f'Total Status Code Count: {total_count}\n')
    output_file.write(f'Total 2XX Status Code Count: {two_xx_count}\n')
    output_file.write(f'Total 4XX Status Code Count: {four_xx_count}\n')
    output_file.write(f'Total 5XX Status Code Count: {five_xx_count}\n')

print('Status code counts saved to status_code_counts.txt')
