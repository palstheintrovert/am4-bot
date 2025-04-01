from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from datetime import datetime
import os

class AM4Bot():
    
    def __init__(self):
        # Initialize Chrome options
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')  # Run in headless mode for server
        
        # Initialize driver with WebDriver Manager
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        self.driver.implicitly_wait(10)

    
    def login(self):
        try:
            print(f"{self.current_time()} - Attempting login...")
            
            # Go to website
            self.driver.get('https://www.airlinemanager.com/')
            sleep(2)
            
            # Click login button
            fb_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Log in")]'))
            )
            fb_btn.click()
            sleep(2)
    
            # Enter credentials
            username_in = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="lEmail"]'))
            )
            username_in.send_keys(os.getenv('AM4_EMAIL', 'YOUR_EMAIL'))  # Use environment variable or default
            
            pw_in = self.driver.find_element(By.XPATH, '//*[@id="lPass"]')
            pw_in.send_keys(os.getenv('AM4_PASSWORD', 'YOUR_PASSWORD'))  # Use environment variable or default
            sleep(1)
    
            # Click login button
            login_btn = self.driver.find_element(By.XPATH, '//*[@id="btnLogin"]')
            login_btn.click() 
            sleep(4)
            
            # Close popup if exists
            try:
                close_btn = self.driver.find_element(By.XPATH, '//*[@id="flightInfo"]/div[4]/span')
                close_btn.click()
            except:
                pass
                
            print(f"{self.current_time()} - Login successful")
            
        except Exception as e:
            print(f"Login failure: {str(e)}")
            raise
    
    def fuel_check(self):
        try:
            print(f"{self.current_time()} - Checking fuel...")
            
            # Click fuel button
            fuel_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "fuel") and contains(text(), "Fuel")]'))
            )
            fuel_btn.click()
            sleep(2)
            
            # Get fuel price
            fuel_price = self.driver.find_element(By.XPATH, '//*[@id="fuelMain"]/div/div[1]/span[2]/b').text
            fuel_price = int(fuel_price.replace("$ ", "").replace(",", ""))
            
            # Get remaining fuel
            fuel_remaining = int(self.driver.find_element(By.XPATH, '//*[@id="holding"]').text.replace(",", ""))
            
            print(f"Current fuel price: ${fuel_price:,}, Remaining: {fuel_remaining:,} lbs")
            
            if fuel_price <= 400 or fuel_remaining <= 8_000_000:
                # Buy fuel
                fuel_amount = self.driver.find_element(By.XPATH, '//*[@id="amountInput"]')
                fuel_amount.clear()
                fuel_amount.send_keys("15000000")
                sleep(1)
                
                fuel_buy = self.driver.find_element(By.XPATH, '//*[@id="fuelMain"]/div/div[7]/div/button[2]')
                fuel_buy.click()
                sleep(2)
                
                # Verify purchase
                new_amount = int(self.driver.find_element(By.XPATH, '//*[@id="holding"]').text.replace(",", ""))
                if new_amount > fuel_remaining:
                    print(f"Purchased fuel at ${fuel_price:,}")
                else:
                    print("Not enough money to buy fuel")
            
            # Close panel
            self.driver.find_element(By.XPATH, '//*[@id="popup"]/div/div/div[1]/div/span').click()
            
        except Exception as e:
            print(f"Fuel check error: {str(e)}")
            self.close_popups()
    
    def CO2_check(self):
        try:
            print(f"{self.current_time()} - Checking CO2...")
            
            # Click fuel button first
            self.driver.find_element(By.XPATH, '//div[contains(@class, "fuel")]').click()
            sleep(1)
            
            # Switch to CO2 tab
            co2_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "CO₂")]'))
            )
            co2_btn.click()
            sleep(2)
            
            # Get CO2 price
            co2_price = int(self.driver.find_element(By.XPATH, '//*[@id="co2Main"]/div/div[2]/span[2]/b').text.replace("$ ", ""))
            
            # Get remaining CO2
            co2_remaining = int(self.driver.find_element(By.XPATH, '//*[@id="holding"]').text.replace(",", ""))
            
            print(f"Current CO2 price: ${co2_price:,}, Remaining: {co2_remaining:,} lbs")
            
            if co2_price <= 104 or co2_remaining <= 1_000_000:
                # Buy CO2
                co2_amount = self.driver.find_element(By.XPATH, '//*[@id="amountInput"]')
                co2_amount.clear()
                co2_amount.send_keys("8000000")
                sleep(1)
                
                co2_buy = self.driver.find_element(By.XPATH, '//*[@id="co2Main"]/div/div[8]/div/button[2]')
                co2_buy.click()
                sleep(2)
                
                # Verify purchase
                new_amount = int(self.driver.find_element(By.XPATH, '//*[@id="holding"]').text.replace(",", ""))
                if new_amount > co2_remaining:
                    print(f"Purchased CO2 at ${co2_price:,}")
                else:
                    print("Not enough money to buy CO2")
            
            # Close panel
            self.driver.find_element(By.XPATH, '//*[@id="popup"]/div/div/div[1]/div/span').click()
            
        except Exception as e:
            print(f"CO2 check error: {str(e)}")
            self.close_popups()
    
    def depart_all(self):
        try:
            print(f"{self.current_time()} - Departing flights...")
            
            # Click status button
            status_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Status")]'))
            )
            status_btn.click()
            sleep(2)
            
            # Filter landed flights
            landed_btn = self.driver.find_element(By.XPATH, '//button[contains(text(), "Landed")]')
            landed_btn.click()
            sleep(2)
            
            # Depart all
            depart_all_btn = self.driver.find_element(By.XPATH, '//*[@id="listDepartAll"]/div/button[2]')
            depart_all_btn.click()
            sleep(4)
            
            print("Flights departed")
            
        except Exception as e:
            print(f"Departure error: {str(e)}")
            self.close_popups()
    
    def bulk_repair(self):
        try:
            print(f"{self.current_time()} - Checking repairs...")
            
            # Click maintenance button
            maint_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Maintenance")]'))
            )
            maint_btn.click()
            sleep(2)
            
            # Click planes tab
            planes_btn = self.driver.find_element(By.XPATH, '//button[contains(text(), "Planes")]')
            planes_btn.click()
            sleep(2)
            
            # Click bulk repair
            bulk_btn = self.driver.find_element(By.XPATH, '//button[contains(text(), "Bulk")]')
            bulk_btn.click()
            sleep(2)
            
            # Select repair option
            select = self.driver.find_element(By.XPATH, '//select')
            select.click()
            sleep(1)
            
            option = self.driver.find_element(By.XPATH, '//option[contains(text(), "Aircraft needing")]')
            option.click()
            sleep(1)
            
            # Confirm repair
            repair_btn = self.driver.find_element(By.XPATH, '//button[contains(text(), "Repair")]')
            repair_btn.click()
            sleep(2)
            
            print("Aircrafts sent for repair")
            
        except Exception as e:
            print(f"Repair error: {str(e)}")
            self.close_popups()
    
    def close_popups(self):
        try:
            self.driver.find_element(By.XPATH, '//*[@id="flightInfo"]/div[4]/span').click()
        except:
            pass
        
        try:
            self.driver.find_element(By.XPATH, '//*[@id="popup"]/div/div/div[1]/div/span').click()
        except:
            pass
    
    def current_time(self):
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    def run(self):
        try:
            self.login()
            
            while True:
                # Run checks every 30 minutes
                if datetime.now().minute % 30 == 0:
                    self.fuel_check()
                    self.CO2_check()
                
                # Depart flights every 5 minutes
                if datetime.now().minute % 5 == 0:
                    self.depart_all()
                
                # Run repairs every 6 hours
                if datetime.now().hour % 6 == 0 and datetime.now().minute == 0:
                    self.bulk_repair()
                
                print(f"{self.current_time()} - Waiting...")
                sleep(60)  # Check every minute
                
        except Exception as e:
            print(f"Fatal error: {str(e)}")
        finally:
            self.driver.quit()

if __name__ == "__main__":
    bot = AM4Bot()
    bot.run()
