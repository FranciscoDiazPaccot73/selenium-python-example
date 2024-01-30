from flask import Flask, jsonify
from flask_restful import Api, Resource
from bs4 import BeautifulSoup
from selenium import webdriver
import logging
import time

app = Flask(__name__)
api = Api(app)

class Utils:
  def logger_warning(text):
    print(text)
    logging.warning(text)

  def logger_error(text):
    print(text)
    logging.error(text)

class ServerLive(Resource):
   def get(self):
    Utils.logger_warning(f"Your server is working well!")
    return jsonify({"message": f"Your server is working well!"})

class TestRoute(Resource):
  def get(self):
    driver = None
    startTime = time.time()
    Utils.logger_warning(f"starting execution: {startTime}")
    try:
      url = 'https://www.franciscodiazpaccot.dev/blog/en/python-selenium-example'
      chrome_options = webdriver.ChromeOptions()
      chrome_options.add_argument('--no-sandbox')
      chrome_options.add_argument('--headless=new')
      chrome_options.add_argument('--ignore-certificate-errors')
      chrome_options.add_argument('--disable-dev-shm-usage')
      chrome_options.add_argument('--disable-extensions')
      chrome_options.add_argument('--disable-gpu')
      chrome_options.add_argument('--blink-settings=imagesEnabled=false')
      chrome_options.add_argument("--start-maximized")
      chrome_options.add_argument('--log-level=DEBUG') 
      driver = webdriver.Chrome(options=chrome_options)
      print(f"Init request after: {time.time() - startTime}")
      Utils.logger_error(f"Init request after: {time.time() - startTime}")
      try:
        driver.get(url)
      except Exception as err:
        Utils.logger_error(f"ERROR GETTING URL: {url} - {str(err)}")

      Utils.logger_warning(f'get to {url} completed after: {time.time() - startTime}')
      content = driver.page_source
      soup = BeautifulSoup(content, 'html.parser')
      title = soup.title.string
      finishExecution = time.time() - startTime
      print(f"Fully load elem: {finishExecution}")
      Utils.logger_warning(f"Finish after: {finishExecution}")

      return jsonify({"title": title})
    except Exception as err:
      Utils.logger_error(f"Error: {str(err)}")
      return jsonify({"Error": f"Something went wrong! {str(err)}"})
    finally:
      Utils.logger_error(f"total execution time: {time.time() - startTime}")
      if driver:
        driver.quit()


api.add_resource(ServerLive, "/")
api.add_resource(TestRoute, "/test")

if __name__ == "__main__":
  app.run(debug=True)