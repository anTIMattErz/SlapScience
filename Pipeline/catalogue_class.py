"""
Class to organize catalogues of artists.
These are just pandas dataframes in standard format.
"""
class Catalogue:

	#Class object catalogue is a pandas dataframe -> self.catalogue.
	#run the constructor with nothing specified and it will generate
	#an empty catalogue dataframes with standard columns.
	def __init__(self, artist_catalogue = None):
		if artist_catalogue is None:
			self.catalogue = pd.DataFrame([], columns = [
							 'artist_url',
                             'artist_name',
                             'song_url',
                             'song_name',
                             'country',
                             'genre',
                             'playlist_type',
                             'run_date',
                             'playlist',
                             'runID'])
		else:
			self.catalogue = artist_catalogue
		
	
	#To print the dataframe
	def print_catalogue(self):
		
		pd.set_option('display.max_columns', None)
		
		print(self.catalogue)
		
		return
	
	#takes in catalogue, retuns tuple of max run_id and next run_id	
	def run_id_gen(self):
	
		max_run_id = self.catalogue['runID'].max()
		next_run_id = max_run_id + 1

		return max_run_id, next_run_id
	
	#concatenates to Catalogue objects vertically (Sql union)
	def union_catalogue(self, other):
	
		catalogue = Catalogue(pd.concat([self.catalogue, other.catalogue]))

		return catalogue
	
	#To rename index the catalogue based on given string variable
	def rename_index(self, string):
		
		re_named_data = Catalogue(self.catalogue\
				.rename_axis(string))
				
		return re_named_data
	
	#To add index or replace index of catalogue. Drop index replaces index
	def re_index_catalogue(self, drop = None):
		if drop is None:
			re_indexed_data = Catalogue(self.catalogue\
					.reset_index()\
					.rename_axis('index'))
		else:
			re_indexed_data = Catalogue(self.catalogue\
					.reset_index(drop = True)\
					.rename_axis('index'))
				
		return re_indexed_data
	
	#To save data to CSV based on working directory
	def save_data(self, file_name):
	
		file_to_save = self.catalogue
		
		file_to_save.to_csv(file_name)
		
		print('FILE SAVED TO DISK')
		
		return