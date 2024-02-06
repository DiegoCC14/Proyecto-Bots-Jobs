from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime
import json


class Text_Voice_bot():
	
	driver = None

	def __init__( self ):
		options = webdriver.ChromeOptions()
		options.add_argument("--window-size=750,800")
		self.driver = webdriver.Chrome( options=options )
		

	def close_driver( self ):
		if self.driver is not None:
			self.driver.quit()
		self.driver = None

	def get_jobs_Accenture( self , lista_palabras_claves , data_url , fuente_job ):
		
		list_all_jobs_accenture = []
		for palabra_clave in lista_palabras_claves:	
			
			try:

				try:
					self.driver.get( f'https://www.accenture.com/{data_url}/careers/jobsearch?jk={palabra_clave}&sb=1&vw=0&is_rj=0&pg=1' )
					WebDriverWait( self.driver , 5).until(
						EC.visibility_of_element_located( ( By.XPATH , './/select[ contains( @id , "jobsearchblock-paginationxs-01-" ) ]' ) )
					)
					list_options_pages = self.driver.find_elements( By.XPATH , './/select[ contains( @id , "jobsearchblock-paginationxs-01-") ]/option' )
				except:
					list_options_pages = [1]
				
				list_jobs = []
				for num_page in range( 1,len(list_options_pages)+1 ):
					self.driver.get( f'https://www.accenture.com/{data_url}/careers/jobsearch?jk={palabra_clave}&sb=1&vw=0&is_rj=0&pg={num_page}' )
					
					WebDriverWait( self.driver , 10).until(
						EC.visibility_of_element_located( ( By.XPATH , './/div[ @class="cmp-teaser card" ]' ) )
					)
					list_divs_jobs = self.driver.find_elements( By.XPATH , './/div[ @class="cmp-teaser card" ]' )
					for div_job in list_divs_jobs:
						title_job = div_job.find_element( By.XPATH , './/h3[ @class="cmp-teaser__title" ]' ).text
						url_job = div_job.find_element( By.XPATH , './a' ).get_attribute('href')
						for palabra in lista_palabras_claves:
							if palabra.lower() in title_job.lower(): 
								list_jobs.append( { 'titulo' : title_job , 'fuente': fuente_job , 'url' : url_job} )

			except:
				list_jobs = []

			list_all_jobs_accenture += list_jobs

		return list_all_jobs_accenture

if __name__ == "__main__":

	bot_Voice = Text_Voice_bot()
	
	lista_ubicasiones = [
		{ 'fuente_job':'Accenture - Argentina' , 'data_url' : 'ar-es' },
		{ 'fuente_job':'Accenture - Chile' , 'data_url' : 'cl-es' },
		{ 'fuente_job':'Accenture - Colombia' , 'data_url' : 'co-es' },
		{ 'fuente_job':'Accenture - Mexico' , 'data_url' : 'mx-es' },
		{ 'fuente_job':'Accenture - España' , 'data_url' : 'es-es' }
	]
	for ubicasion in lista_ubicasiones:
		lista_palabras_claves = ['Developer',"Devops",'QA','Desarrollador','Software']

		list_jobs_accenture = bot_Voice.get_jobs_Accenture( lista_palabras_claves , ubicasion['data_url'] , ubicasion['fuente_job'] )
		
		list_job_sin_repeticiones = []
		for job in list_jobs_accenture:
			if job not in list_job_sin_repeticiones:
				list_job_sin_repeticiones.append( job )

		with open( f'Jobs/{datetime.now().strftime("%Y-%m-%d")}_{ubicasion["fuente_job"]}.json' , 'w' ) as file_json:
			json.dump( list_job_sin_repeticiones , file_json)
		
	bot_Voice.close_driver()