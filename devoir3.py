#coding : utf-8

import csv, requests
from bs4 import BeautifulSoup

fichier="soundcloud.csv"

url1 = "https://soundcloud.com/people/directory/"

entetes = {
    "User-Agent":"Lina Heckenast, UQAM student data mining for a class"
}

letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9","_","-"]

n=0

urlBase = "https://soundcloud.com"

for letter in letters:
    url2 = url1 + letter
    #print(url2)
    #ici je créé l'ensemble des url de chaque lettre/chiffre/symbole, donc le premier niveau
    site = requests.get(url2, headers=entetes)

    #print(site.status_code)

    page = BeautifulSoup(site.text,"html.parser")
    #print(url2,page)
    links = page.find_all("li", class_="sc-truncate peopleDirectory__generatedContentListItem")
    #print(links)
    #ici je trouve l'élément dans lequel toutes les URL sont contenues pour chaque lettre/chiffre/symbole, soit le 2e niveau de liens
    
    for link in links:
        links1 = urlBase+link.find("a")["href"]
        #print(links1)
        
        sitelinks1 = requests.get(links1, headers=entetes)
        pagelinks1 = BeautifulSoup(sitelinks1.text,"html.parser")

        links2 = pagelinks1.find_all("li", class_="sc-truncate peopleDirectory__generatedContentListItem")
        #ici je trouve l'élément dans lequel toutes les URL sont contenues pour chaque 2e niveau de liens

        for link2 in links2:
            links3 = urlBase+link2.find("a")["href"]
            #print(links3)

            sitelinks3 = requests.get(links3, headers=entetes)
            pagelinks3 = BeautifulSoup(sitelinks3.text,"html.parser")

            links4 = pagelinks3.find_all("li", class_="sc-truncate peopleDirectory__generatedContentListItem")
            #ici je trouve l'élément dans lequel toutes les URL sont contenues pour chaque 3e niveau de liens, dans lequel les URL des users est contenu

            for link4 in links4:
                links5 = urlBase+link4.find("a")["href"]
                #print(links5)

                sitelinks5 = requests.get(links5, headers=entetes)
                pagelinks5 = BeautifulSoup(sitelinks5.text,"html.parser")

                links6 = pagelinks5.find_all("li", class_="sc-truncate peopleDirectory__generatedContentListItem")
                #ici je trouve l'élément dans lequel toutes les URL sont contenues pour chaque 4e niveau de lien, soit les URL des usagers

                for link6 in links6:
                    urlUsers = urlBase+link6.find("a")["href"]
                    #print(urlUsers)

                    siteurlUsers = requests.get(urlUsers, headers=entetes)
                    pageurlUsers = BeautifulSoup(siteurlUsers.text,"html.parser")

                    #À partir d'ici ça devrait fonctionner comme en haut, mais de ce que j'ai lu en ligne, il se pourrait que je ne sois pas 
                    #capable de moissonner l'info parce que ce serait des blocs de javascript qui envoient l'information
                    #en même temps, l'info est vraiment dans le code html du site, ce qui fait que je ne comprends pas trop. 
                    #en inspectant j'ai tout de même vu un path de JS, donc je me dis que tout est possible.

                    profile = pageurlUsers.find_all("div",class_="profileHeaderInfo__content sc-media-content")
                    #print(profile)

                    for info in profile:
                        n+=1
                        directory=list()
                        username = info.find("h3", class_="profileHeaderInfo__userName g-type-shrinkwrap-block g-type-shrinkwrap-large-primary")
                        name2 = info.find("h4", class_="profileHeaderInfo__additional g-type-shrinkwrap-block g-type-shrinkwrap-large-secondary")
                        #ici je ne savais pas comment différencier les deux
                        location = info.find("h4", class_="profileHeaderInfo__additional g-type-shrinkwrap-block g-type-shrinkwrap-large-secondary")
                        #print(n,username,name2,location)
                        
                        directory.append(username)
                        directory.append(name2)
                        directory.append(location)

                        mumble=open(fichier,"a")
                        rap=csv.writer(mumble)
                        rap.writerow(directory)

                    


                    
                