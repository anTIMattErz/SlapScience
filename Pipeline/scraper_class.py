"""
Driver class to scrape pages on soundcloud.
Class object will be the string with the url. Class functions will be used to 
"""

class Sc_scraper:

	# Class object is the url to scrape. The constructor can take attributes to generate
	# different types of urls. For charts, if url string is charts, then uses attributes
	# to generate url.
	def __init__(self, url_string , url_type_artist_name = None, genre = None, country = None):
		
		if url_string == "charts":
			url = "https://soundcloud.com/charts/"
			self.url = url + url_type_artist_name + "?genre=" + genre + "&country=" + country
		elif url_string =="artist":
			url = 'https://soundcloud.com'
			self.url = url + url_type_artist_name + "/tracks"
		else:
			self.url = str(url_string)
	
	
	# Simple print string url
	def print_url(self):
		
		print(self.url)
		
		return
	
	# Deconstruct the url back to the parameters.Will be used as part of the chart scraper
	# Outputs tuple of url_type, genre, country. These will be inputs for variables in df
	def deconstruct_charts_url(self):
	
		attributes = re.split('https://soundcloud.com/charts/', self.url)[1]
		
		url_type = re.split('\?genre=', attributes)[0]
		
		split1 = re.split('\?genre=', attributes)[1]
		
		split2 = re.split('&country=', split1)
		
		genre = split2[0]
		
		country = split2[1]
		
		return url_type, genre, country
		
	
	# Takes url of charts website and scrapes in catalogue type df -> see catalogue class
	def chart_scraper(self, run_number):
	
		# url of soundcloud page to scrape + read from page using urllib
		content = urllib.request.urlopen(self.url).read()
		url_type, genre, country = self.deconstruct_charts_url()
		run_time = datetime.datetime.now()
		
		# lists to pack with data
		song_url_list = []# list containing song url soundcloud extensions
		song_name_list = []# list containing song names as the appear on site
		artist_url_list = []# list containing artist url soundcloud extensions
		artist_name_list = []# list containing artist url as appear on site
		
		# cycle variable for loop
		i = 0 # track if song (=0) or artist (=1)
		
		# parse out article sections and pattern with second headers (h2) and 'a' child
		only_tags_with_h2 = SoupStrainer("article")
		
		soup = BeautifulSoup(content,
							 "html.parser",
							 parse_only=only_tags_with_h2)\
							 .select('h2 > a')
		
		# append scraped data to respective lists
		for article in soup:
		
			if i == 0 :
				column_name = "song"
				song_url_list.append(str(article.get('href', '/')))
				song_name_list.append(str(article.text))
				i = i + 1
			else:
				column_name = "artist"
				artist_url_list.append(str(article.get('href', '/')))
				artist_name_list.append(str(article.text))
				i = i - 1
		
		# dictionary of data scrapedo on page
		df = {"artist_url":artist_url_list, 
			  "artist_name" : artist_name_list,
			  "song_url" : song_url_list,
			  "song_name" : song_name_list,
			  "country" : country,
			  "genre" : genre,
			  "playlist_type" : url_type,
			  "run_date" : run_time,
			  "playlist": self.url,
			  "runID": run_number}
		
		#generate data frame
		data = pd.DataFrame(df, 
							columns = [
							"artist_url", "artist_name",
							"song_url", "song_name",
							"country", "genre",
							"playlist_type","run_date",
							"playlist", "runID"
							])
										   
		data.index = data.index + 1# chart num from 0 to 1
		
		return data
		
		
	# Open headless Chrome browser for lazy page scraping
	def open_artist_page(self):
		
		driver.get(self.url)
		
		return
	
	
	# TO Scroll all the way to the bottom of lazy loading page
	def scrolling(self):
		
		WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.lazyLoadingList__list")))
    
        # scrolling to the bottom of the page
		lazy_soundList_loaded = 0
		loaded_songs = len(driver.find_elements_by_class_name('soundList__item'))
		except_count = 0
		
		while lazy_soundList_loaded == 0:# waits for the "paging-eof" class to appear when list is loaded
		
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
			try:
				WebDriverWait(driver, 2).until((lambda x: len(driver.find_elements_by_class_name('soundList__item'))!= loaded_songs))
                
         # couldn't figure out how to get it to break when it finds the eof element, just catching timeout instead
			except TimeoutException:
				except_count += 1
				if except_count == 2:
					break
			loaded_songs = len(driver.find_elements_by_class_name('soundList__item'))
			lazy_soundList_loaded = len(driver.find_elements_by_class_name('paging-eof'))
			
		return
		
	
	# To collect data from artist track page using selenium	
	def collect_artist_info(self):
	
		# Grab elements in the page
		item_path = "//*[@class='userMain__content']//li[@class='soundList__item']"
		followers_path = "//a[@class='infoStats__statLink sc-link-light']"
    
		song_list = []
		artist_list = []
		publish_date_list = []
		comment_list = []
		plays_list = []
		likes_list = []
		repost_list = []
        
		for item in  driver.find_elements_by_xpath(item_path):
            
		# Pull Song Name
			song_name = item.find_element_by_class_name('soundTitle__username').text
            
		# Pull Artist Name
			artist_name = item.find_element_by_class_name('soundTitle__title').text
            
		# Pull Publich Date 
			publish_date = datetime.datetime.strptime(
			item.find_element_by_class_name('relativeTime')
			.get_attribute('datetime')
			.replace('T',':')[0:-5],
			'%Y-%m-%d:%H:%M:%S')

        # Pull Likes
			try:
				likes = item.find_element_by_class_name('sc-button-like').text
			except NoSuchElementException:
				likes = "Like"
        
        # Pull Reposts
			try:
				reposts = item.find_element_by_class_name('sc-button-repost').text
			except NoSuchElementException:
				likes = "Repost"
            
        # Pull plays and comments
			stats = item.find_elements_by_class_name('sc-ministats-item')
			num_stats = len(stats)
            
			if num_stats == 0:
				plays, comments = 0, 0
                
			elif num_stats == 1:
				plays = int((re.split(" " ,stats[0].get_attribute('title'))[0]).replace(',',''))
				comments = 0
            
			else:
				for stat in stats:
					plays = int((re.split(" " ,stats[0].get_attribute('title'))[0]).replace(',',''))
					comments = int((re.split(" " ,stats[1].get_attribute('title'))[0]).replace(',',''))
                     
			song_list.append(song_name)
			artist_list.append(artist_name)
			publish_date_list.append(publish_date)
			likes_list.append(likes)
			repost_list.append(reposts)
			plays_list.append(plays)
			comment_list.append(comments)
        
		artist_followers = int((re.split(" " ,driver.find_element_by_xpath(followers_path)\
                                         .get_attribute('title'))[0]).replace(',',''))
        
		run_time = datetime.datetime.now()
		
		print()
		print(self.url)
		print('songs: ' + str(len(song_list)))
		print('artists: '+ str(len(artist_list)))
		print('plays: '+ str(len(plays_list)))
		print('comments: ' + str(len(comment_list)))
		print('likes: ' + str(len(likes_list)))
		print('reposts: ' + str(len(repost_list)))
	
	
		artist_data = {'song_name': song_list,
                       'artist_name': artist_list,
                       'publish_date': publish_date_list,
                       'plays': plays_list,
                       'comments':comment_list,
                       'likes': likes_list,
                       'repost': repost_list,
                       'artist_followers': artist_followers,
                       'run_date': run_time}
        
        
      
		artist_df = pd.DataFrame(artist_data)
		
		return artist_df
	
	
	# To Print and create empty data frame if there is nothing in the opened page		
	def non_existent_artist(self):
		
		print("artist does not exist")
		artist_df = pd.DataFrame()
		
		return artist_df
	
	
	# To open page, collect data or return empty df if artsit changed url or deleted page
	def artist_scraper(self):
	
		self.open_artist_page()
		
		try:
			self.scrolling()
			
			artist_df = self.collect_artist_info()
			
		except TimeoutException:
			artist_df = self.non_existent_artist()
			
		return artist_df
		
		
	
	