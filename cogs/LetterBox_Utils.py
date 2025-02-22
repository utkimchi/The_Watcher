from time import sleep as zzz
import random
import os
from os.path import join
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import typing
import discord
from discord.ext import commands

SLOW_ROLLING_TEST_MODE = True
SLOW_ROLLING_TEST_MODE_SPEED = 2

class addmovie(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bp = Path(__file__).parent.parent
        self.dotenv_path = join(bp, '.env')
        self.adblock_path = join(bp, 'AdBlock')
        self.lb_user = os.getenv("LB_USERNAME")
        self.lb_pass = os.getenv("LB_PASSWORD")
        self.usr1 = os.getenv("LB_USER_1")

        self.options = Options()
        #self.options.add_argument('--headless=new')
        self.options.add_argument('load-extension=' + self.adblock_path)
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--ignore-ssl-errors')

    async def login(self,driver):
        driver.get('https://letterboxd.com/sign-in/')
        element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='username']")))
        element = driver.find_element(By.XPATH, "//input[@name='username']")
        element.send_keys(self.lb_user)
        if SLOW_ROLLING_TEST_MODE:
            zzz(SLOW_ROLLING_TEST_MODE_SPEED)
        element = driver.find_element(By.XPATH, "//input[@name='password']")
        element.send_keys(self.lb_pass)
        if SLOW_ROLLING_TEST_MODE:
            zzz(SLOW_ROLLING_TEST_MODE_SPEED)
        element.submit()
        if SLOW_ROLLING_TEST_MODE:
            zzz(SLOW_ROLLING_TEST_MODE_SPEED)

        return driver, element


    @discord.app_commands.command(name="addmovie",description= "Add a Letterboxd link to our Kinosphere!")
    async def addmovie(self, interaction: discord.Interaction, movie_title: str, list: str = None):
            await interaction.response.defer()
            print("OPP")
            if list == None:
                list = 'Kinosphere'
            movie_hyph = os.path.basename(movie_title.rstrip('/'))
            mess = f"Gonna try to add {movie_hyph}..."
            asd = await interaction.followup.send(mess,wait=True)
            try:
                if 'letterboxd' not in movie_title:
                    return asd.edit_message("You need a link like ->> https://letterboxd.com/film/suspiria/")
                
                driver = webdriver.Chrome(options=self.options)
                await asd.edit(content="Logging in!")
                driver, element = await self.login(driver)
                print(movie_title)
                driver.get(movie_title)

                if SLOW_ROLLING_TEST_MODE:
                    zzz(SLOW_ROLLING_TEST_MODE_SPEED)

                element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.LINK_TEXT, "Add to lists…")))
                element = driver.find_element(By.LINK_TEXT, "Add to lists…")
                element.click()

                if SLOW_ROLLING_TEST_MODE:
                    zzz(SLOW_ROLLING_TEST_MODE_SPEED)

                await asd.edit(content="Cool list!")

                chosen_path = f"//label[contains(@class,'-added')][contains(@class,'list')]/span[@class='label']/span[contains(.,'{list}')]"
                click_path = f"//span[contains(.,'{list}')]"

                element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.LINK_TEXT, "New list…")))

                try:
                    element = driver.find_element(By.XPATH, chosen_path)
                    driver.quit()
                    return asd.edit("That movie already is on the list!")         
                except:
                    element = driver.find_element(By.XPATH, click_path)

                element.click()

                if SLOW_ROLLING_TEST_MODE:
                    zzz(SLOW_ROLLING_TEST_MODE_SPEED)
                    
                element.submit()

                if SLOW_ROLLING_TEST_MODE:
                    zzz(SLOW_ROLLING_TEST_MODE_SPEED)

                driver.quit()

                
                await asd.edit(content= f"You add yo movie {movie_hyph}. Congrats")
            except RuntimeError:
                driver.quit()
                await asd.edit(content= "sumtin wong")

    @discord.app_commands.command(name="delmovie",description= "Removie a Letterboxd link to our Kinosphere!")
    async def delmovie(self, interaction: discord.Interaction, movie_title: str, list: str = None):
            await interaction.response.defer()
            if list == None:
                list = 'Kinosphere'
            movie_hyph = os.path.basename(movie_title.rstrip('/'))
            mess = f"Gonna try to delete {movie_hyph}..."
            asd = await interaction.followup.send(mess,wait=True)


            try:
                if 'letterboxd' not in movie_title:
                    return asd.edit(content="You need a link like ->> https://letterboxd.com/film/suspiria/")
            
                driver = webdriver.Chrome(options=self.options)
                await asd.edit(content="Logging in!")
                driver, element = await self.login(driver)
                driver.get(movie_title)

                if SLOW_ROLLING_TEST_MODE:
                    zzz(SLOW_ROLLING_TEST_MODE_SPEED)


                element = driver.find_element(By.XPATH,"//div[@id='js-poster-col']//div[contains(@class,'film-poster')]")
                data_id = element.get_attribute('data-item-id')
                print(data_id)

                list_string = f"https://letterboxd.com/{self.lb_user.lower()}/list/{list.lower()}/edit"
                driver.get(list_string)

                if SLOW_ROLLING_TEST_MODE:
                    zzz(SLOW_ROLLING_TEST_MODE_SPEED)

                try:
                    element = driver.find_element(By.XPATH, "body[contains(@class, error) and contains(@class,message-dark)]")
                    driver.quit()
                    await asd.edit(content= "That List don't exist..")
                except:
                    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(@data-item-id,'{data_id}')]/following-sibling::span[@class='list-item-actions']/a")))
                    element.click()

                if SLOW_ROLLING_TEST_MODE:
                    zzz(SLOW_ROLLING_TEST_MODE_SPEED)

                element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, f"//a[@id='list-edit-save']")))
                element.click()

                driver.quit()
                await asd.edit(content=f"Deleted tha {movie_hyph}. Congrats")

            except RuntimeError:
                driver.quit()
                await asd.edit(content="sumtin wong")    

    @discord.app_commands.command(name="randomovie",description= "Get a random flick from our Kinosphere!")
    @discord.app_commands.choices(ourlists=[
        discord.app_commands.Choice(name="Kinosphere", value="kinosphere"),
        discord.app_commands.Choice(name="Triple C", value="ccc-ppp")
    ])
    
    async def randomovie(self, interaction: discord.Interaction, otherlistlink: str = None, ourlists: discord.app_commands.Choice[str] = None):
            print("THIS HAS BEEN RELOADED")
            await interaction.response.defer()

            if ourlists is not None:
                list_name = f'https://letterboxd.com/{self.usr1}/list/{ourlists.value}/'
            else:
                if otherlistlink == None:
                    otherlistlink = f'https://letterboxd.com/{self.lb_user.lower()}/list/kinosphere/'
                else:
                    list_name = otherlistlink

            list_hyph = os.path.basename(list_name.rstrip('/'))
            mess = f"Gonna try to find a random movie off {list_hyph}..."
            asd = await interaction.followup.send(mess,wait=True)
            try:
                if 'letterboxd' not in list_name:
                    return asd.edit(content="You need a link like ->> https://letterboxd.com/film/suspiria/")
            
                driver = webdriver.Chrome(options=self.options)
                driver.get(list_name)

                if SLOW_ROLLING_TEST_MODE:
                    zzz(SLOW_ROLLING_TEST_MODE_SPEED)

                try:
                    print("t")
                    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "a[@class='next']")))
                    print("Next")
                    pages = driver.find_elements(By.XPATH, "//li[contains(@class,'paginate-page')]//a")
                    print(pages)
                    pages = [p.get_text() for p in pages]
                    pnum = random.choice(pages)
                    if pnum != 1:
                        new_page = f"page/{str(pnum)}/"
                        new_page = list_name+new_page
                        driver.get(new_page)
                    if SLOW_ROLLING_TEST_MODE:
                        zzz(SLOW_ROLLING_TEST_MODE_SPEED)
                except:
                    await asd.edit(content="Small List!")

                elements = driver.find_elements(By.XPATH, "//ul[contains(@class, 'film-list') and contains(@class,'poster-list')]//li//div")
                slugs = [e.get_attribute('data-film-slug') for e in elements if e.get_attribute('data-film-slug') is not None]
                movie_slug = random.choice(slugs)
                random_page_link = f"https://letterboxd.com/film/{movie_slug}/"
                print(random_page_link)
                driver.quit()
                mess = f"Here ya go! {random_page_link}"
                await asd.edit(content=mess)
            except:
                driver.quit()
                await asd.edit(content="Couldn't finda friggin film..")

            
async def setup(bot):
    await bot.add_cog(addmovie(bot))

