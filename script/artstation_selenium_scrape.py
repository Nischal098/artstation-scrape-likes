import os
import time
from selenium import webdriver
import urllib.request

# Loads the driver in headless mode.
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options=options)

# Class used to get through artstation's block of spider header (or any other site's block, for that matter).
class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

def scrolldown(int):
	i = 0
	AMOUNTOFSCROLLDOWNATTEMPTS=int
	# Scrolls to the bottom of the page, ensuring that all images are loaded in.
	while i<AMOUNTOFSCROLLDOWNATTEMPTS :
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(0.5)
		i=i+1
	return

def links():
	links_to_images = driver.find_elements_by_class_name("project-image")

	# Initiates list
	links_list = []

	# Get all links to liked collections/artwork.
	for link in links_to_images:
	    links_list.append(link.get_attribute('href'))
	return links_list

def ensureAmountOfLikesCorrect():
	# Initiates the list of links to likes.
	links_list=links()
	# Gets the amount of likes.
	amountofFavourites=driver.find_element_by_xpath("//span[@class='counter-number']").text
	amountofFavourites=amountofFavourites.strip("()")
	amountofFavourites=int(amountofFavourites)
	# Scrolls down the page until all likes have been loaded into the list.
	while len(links_list)!=amountofFavourites:
		scrolldown(1)
		links_list=links()
	return links_list

def getUsername():
	# Requests user to put in their artstation username to get their likes.
	response=input("Please enter your artstation username: ")

	if response=="":
		print("No input, quitting")
		driver.quit()
		quit()

	return response

# Opens the webpage for likes.
opener = AppURLopener()
driver.get("https://www.artstation.com/"+getUsername()+"/likes")
print("Opened webpage")

links_list=ensureAmountOfLikesCorrect()

# Looks through the link_list for items.
for link in links_list:
    driver.get(link)

    # Finds the elements with the class artwork-image.
    images = driver.find_elements_by_xpath("//div[@class=\"artwork-image\"]/img")

    for image in images:
        src = image.get_attribute("src")
        # Strips the query on the right of the filename.
        filename = src.rstrip("1234567890?")
        # If else statement needed to get the filename, the path length is different depending on if it is a .gif file or not.
        if filename.endswith(".gif"):
            filename = filename[72:]
        else:
            filename = filename[69:]

        # Downloads the image to the folder which in the script is being run.
        opener.retrieve(src, filename)

print("Done downloading all the files")

# Quits the currently loaded driver, to ensure that no instance is left after finishing the script.
driver.quit()
quit()